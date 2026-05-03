import argparse
import configparser
import logging
import os
import sqlite3
import sys
import time
from datetime import datetime, timezone, timedelta

import yt_dlp
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger("hololive-dl-yt-video")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Download Hololive members' YouTube videos"
    )
    parser.add_argument(
        "config_file_path",
        nargs="?",
        default="hololive-dl-yt-video.ini",
        help="Path to config INI file (default: hololive-dl-yt-video.ini)",
    )
    return parser.parse_args()


DEFAULT_CONFIG_CONTENT = """[general]
sqlite_file_path = hololive-dl-yt-video.sqlite3
task_timezone = Asia/Taipei
sync_yt_video_task_cron_schedule = */5 * * * *
sync_yt_video_task_timeout_minutes = 5
sync_yt_video_task_max_video_minutes = 10
sync_yt_video_task_cooldown_minutes = 1440
dl_yt_video_task_cron_schedule = * * * * *
dl_yt_video_task_timeout_minutes = 5
dl_yt_video_task_output_folder_path = downloads
"""


def parse_config(config_file_path):
    if not os.path.exists(config_file_path):
        logger.info("Config file '%s' not found, creating with defaults", config_file_path)
        try:
            with open(config_file_path, "w", encoding="utf-8") as f:
                f.write(DEFAULT_CONFIG_CONTENT)
            logger.info("Created default config file at '%s'", config_file_path)
        except OSError as e:
            logger.error("Failed to create config file '%s': %s", config_file_path, e)
            sys.exit(1)

    config = configparser.ConfigParser()
    try:
        config.read(config_file_path, encoding="utf-8")
    except configparser.Error as e:
        logger.error("Failed to parse config file '%s': %s", config_file_path, e)
        sys.exit(1)

    general = config["general"] if "general" in config else {}

    settings = {
        "sqlite_file_path": general.get("sqlite_file_path", "hololive-dl-yt-video.sqlite3"),
        "task_timezone": general.get("task_timezone", "Asia/Taipei"),
        "sync_yt_video_task_cron_schedule": general.get(
            "sync_yt_video_task_cron_schedule", "*/5 * * * *"
        ),
        "sync_yt_video_task_timeout_minutes": int(
            general.get("sync_yt_video_task_timeout_minutes", "5")
        ),
        "sync_yt_video_task_max_video_minutes": int(
            general.get("sync_yt_video_task_max_video_minutes", "10")
        ),
        "sync_yt_video_task_cooldown_minutes": int(
            general.get("sync_yt_video_task_cooldown_minutes", "1440")
        ),
        "dl_yt_video_task_cron_schedule": general.get(
            "dl_yt_video_task_cron_schedule", "* * * * *"
        ),
        "dl_yt_video_task_timeout_minutes": int(
            general.get("dl_yt_video_task_timeout_minutes", "5")
        ),
        "dl_yt_video_task_output_folder_path": general.get(
            "dl_yt_video_task_output_folder_path", "downloads"
        ),
    }
    return settings


def init_sqlite_db(sqlite_file_path):
    if os.path.exists(sqlite_file_path):
        logger.info("SQLite DB already exists at '%s'", sqlite_file_path)
        return
    logger.info("Creating SQLite DB at '%s'", sqlite_file_path)
    try:
        conn = sqlite3.connect(sqlite_file_path)
        conn.close()
        logger.info("SQLite DB created successfully")
    except sqlite3.Error as e:
        logger.error("Failed to create SQLite DB at '%s': %s", sqlite_file_path, e)
        sys.exit(1)


def connect_sqlite_db(sqlite_file_path):
    try:
        conn = sqlite3.connect(sqlite_file_path)
        logger.info("Connected to SQLite DB at '%s'", sqlite_file_path)
        return conn
    except sqlite3.Error as e:
        logger.error("Failed to connect to SQLite DB at '%s': %s", sqlite_file_path, e)
        sys.exit(1)


HOLOLIVE_CHANNEL_COLUMNS = {
    "channel_id": "TEXT PRIMARY KEY",
    "talent_name": "TEXT",
    "updated_at": "TEXT",
    "status": "TEXT",
}


def init_hololive_channel_table(conn):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='hololive_channel'"
    )
    if cursor.fetchone():
        logger.info("hololive_channel table already exists")
        return
    logger.info("Creating hololive_channel table")
    try:
        cursor.execute(
            "CREATE TABLE hololive_channel ("
            "channel_id TEXT PRIMARY KEY, "
            "talent_name TEXT, "
            "updated_at TEXT, "
            "status TEXT"
            ")"
        )
        conn.commit()
        logger.info("hololive_channel table created successfully")
    except sqlite3.Error as e:
        logger.error("Failed to create hololive_channel table: %s", e)
        sys.exit(1)


def validate_hololive_channel_table(conn):
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(hololive_channel)")
    columns = {row[1]: row[2] for row in cursor.fetchall()}
    expected = {"channel_id", "talent_name", "updated_at", "status"}
    if not expected.issubset(columns.keys()):
        missing = expected - set(columns.keys())
        logger.error(
            "hololive_channel table missing columns: %s. Found: %s",
            missing,
            list(columns.keys()),
        )
        sys.exit(1)
    logger.info("hololive_channel table validation passed")


DL_YT_VIDEO_TASK_COLUMNS = {
    "video_id": "TEXT PRIMARY KEY",
    "channel_id": "TEXT",
    "video_name": "TEXT",
    "updated_at": "TEXT",
    "status": "TEXT",
}


def init_dl_yt_video_task_table(conn):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='dl_yt_video_task'"
    )
    if cursor.fetchone():
        logger.info("dl_yt_video_task table already exists")
        return
    logger.info("Creating dl_yt_video_task table")
    try:
        cursor.execute(
            "CREATE TABLE dl_yt_video_task ("
            "video_id TEXT PRIMARY KEY, "
            "channel_id TEXT, "
            "video_name TEXT, "
            "updated_at TEXT, "
            "status TEXT"
            ")"
        )
        conn.commit()
        logger.info("dl_yt_video_task table created successfully")
    except sqlite3.Error as e:
        logger.error("Failed to create dl_yt_video_task table: %s", e)
        sys.exit(1)


def validate_dl_yt_video_task_table(conn):
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(dl_yt_video_task)")
    columns = {row[1]: row[2] for row in cursor.fetchall()}
    expected = {"video_id", "channel_id", "video_name", "updated_at", "status"}
    if not expected.issubset(columns.keys()):
        missing = expected - set(columns.keys())
        logger.error(
            "dl_yt_video_task table missing columns: %s. Found: %s",
            missing,
            list(columns.keys()),
        )
        sys.exit(1)
    logger.info("dl_yt_video_task table validation passed")


def init_output_folder(folder_path):
    if os.path.exists(folder_path):
        logger.info("Output folder already exists at '%s'", folder_path)
        return
    logger.info("Creating output folder at '%s'", folder_path)
    try:
        os.makedirs(folder_path, exist_ok=True)
        logger.info("Output folder created successfully")
    except OSError as e:
        logger.error("Failed to create output folder at '%s': %s", folder_path, e)
        sys.exit(1)


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def get_task_connection(sqlite_file_path):
    return connect_sqlite_db(sqlite_file_path)


def sync_yt_video_task(sqlite_file_path, timeout_minutes, max_video_minutes, cooldown_minutes):
    conn = get_task_connection(sqlite_file_path)
    cursor = conn.cursor()
    now = now_iso()
    try:
        cursor.execute(
            "UPDATE hololive_channel SET status='FAILED', updated_at=? "
            "WHERE status='STARTED' AND datetime(updated_at) < datetime(?, '-' || ? || ' minutes')",
            (now, now, timeout_minutes),
        )
        conn.commit()
        if cursor.rowcount > 0:
            logger.info("Marked %d timed-out sync tasks as FAILED", cursor.rowcount)

        cursor.execute("SELECT channel_id FROM hololive_channel WHERE status='STARTED'")
        if cursor.fetchone():
            logger.info("A sync task is already running, skipping this cycle")
            conn.close()
            return

        cursor.execute(
            "SELECT channel_id, talent_name FROM hololive_channel "
            "WHERE status IN ('COMPLETED', 'FAILED') "
            "AND datetime(updated_at) < datetime(?, '-' || ? || ' minutes') "
            "ORDER BY updated_at ASC LIMIT 1",
            (now, cooldown_minutes),
        )
        row = cursor.fetchone()
        if not row:
            logger.info("No channel needs syncing")
            conn.close()
            return

        channel_id, talent_name = row
        cursor.execute(
            "UPDATE hololive_channel SET status='STARTED', updated_at=? WHERE channel_id=?",
            (now, channel_id),
        )
        conn.commit()

        try:
            ydl_opts = {
                "quiet": True,
                "extract_flat": True,
                "ignoreerrors": True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(
                    f"https://www.youtube.com/channel/{channel_id}/videos",
                    download=False,
                )

            if not info or "entries" not in info:
                logger.warning("No entries found for channel %s", channel_id)
                mark_sync_failed(conn, cursor, channel_id)
                conn.close()
                return

            entries = info.get("entries", [])
            entries.reverse()

            new_tasks = 0
            for entry in entries:
                if entry is None:
                    continue
                duration = entry.get("duration") or 0
                if duration > max_video_minutes * 60:
                    continue
                video_id = entry.get("id")
                if not video_id:
                    continue
                current_now = now_iso()
                cursor.execute(
                    "INSERT OR IGNORE INTO dl_yt_video_task (video_id, channel_id, video_name, updated_at, status) "
                    "VALUES (?, ?, '', ?, 'FAILED')",
                    (video_id, channel_id, current_now),
                )
                if cursor.rowcount > 0:
                    new_tasks += 1
            conn.commit()
            logger.info("Created %d new download tasks for channel %s", new_tasks, channel_id)

            cursor.execute(
                "UPDATE hololive_channel SET status='COMPLETED', updated_at=? WHERE channel_id=?",
                (now_iso(), channel_id),
            )
            conn.commit()
            logger.info(
                "Sync completed for channel %s (%s)", channel_id, talent_name
            )
        except Exception as e:
            logger.error("Sync task failed for channel %s: %s", channel_id, e)
            mark_sync_failed(conn, cursor, channel_id)
    finally:
        conn.close()


def mark_sync_failed(conn, cursor, channel_id):
    now = now_iso()
    cursor.execute(
        "UPDATE hololive_channel SET status='FAILED', updated_at=? WHERE channel_id=?",
        (now, channel_id),
    )
    conn.commit()


def dl_yt_video_task(
    sqlite_file_path, timeout_minutes, output_folder_path
):
    conn = get_task_connection(sqlite_file_path)
    cursor = conn.cursor()
    now = now_iso()
    try:
        cursor.execute(
            "UPDATE dl_yt_video_task SET status='FAILED', updated_at=? "
            "WHERE status='STARTED' AND datetime(updated_at) < datetime(?, '-' || ? || ' minutes')",
            (now, now, timeout_minutes),
        )
        conn.commit()
        if cursor.rowcount > 0:
            logger.info("Marked %d timed-out download tasks as FAILED", cursor.rowcount)

        cursor.execute("SELECT video_id FROM dl_yt_video_task WHERE status='STARTED'")
        if cursor.fetchone():
            logger.info("A download task is already running, skipping this cycle")
            conn.close()
            return

        cursor.execute(
            "SELECT t.video_id, t.channel_id, h.talent_name FROM dl_yt_video_task t "
            "LEFT JOIN hololive_channel h ON t.channel_id = h.channel_id "
            "WHERE t.status IN ('COMPLETED', 'FAILED') "
            "ORDER BY t.updated_at ASC LIMIT 1"
        )
        row = cursor.fetchone()
        if not row:
            logger.info("No video needs downloading")
            conn.close()
            return

        video_id, channel_id, talent_name = row
        cursor.execute(
            "UPDATE dl_yt_video_task SET status='STARTED', updated_at=? WHERE video_id=?",
            (now, video_id),
        )
        conn.commit()

        try:
            talent_folder = talent_name if talent_name else channel_id
            output_path = os.path.join(output_folder_path, talent_folder)
            os.makedirs(output_path, exist_ok=True)
            template = os.path.join(output_path, "%(title)s.%(ext)s")

            ydl_opts = {
                "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "outtmpl": template,
                "quiet": True,
                "ignoreerrors": True,
                "merge_output_format": "mp4",
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(
                    f"https://www.youtube.com/watch?v={video_id}", download=True
                )

            video_title = info.get("title", video_id) if info else video_id
            video_filename = f"{video_title}.mp4"

            now_complete = now_iso()
            cursor.execute(
                "UPDATE dl_yt_video_task SET status='COMPLETED', video_name=?, updated_at=? WHERE video_id=?",
                (video_filename, now_complete, video_id),
            )
            conn.commit()
            logger.info(
                "Downloaded video %s to %s", video_id, os.path.join(output_path, video_filename)
            )
        except Exception as e:
            logger.error("Download task failed for video %s: %s", video_id, e)
            now_fail = now_iso()
            cursor.execute(
                "UPDATE dl_yt_video_task SET status='FAILED', updated_at=? WHERE video_id=?",
                (now_fail, video_id),
            )
            conn.commit()
    finally:
        conn.close()


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main():
    setup_logging()
    args = parse_args()
    config_file_path = args.config_file_path
    settings = parse_config(config_file_path)

    sqlite_file_path = settings["sqlite_file_path"]
    task_timezone = settings["task_timezone"]
    sync_cron = settings["sync_yt_video_task_cron_schedule"]
    sync_timeout = settings["sync_yt_video_task_timeout_minutes"]
    sync_max_video = settings["sync_yt_video_task_max_video_minutes"]
    sync_cooldown = settings["sync_yt_video_task_cooldown_minutes"]
    dl_cron = settings["dl_yt_video_task_cron_schedule"]
    dl_timeout = settings["dl_yt_video_task_timeout_minutes"]
    output_folder = settings["dl_yt_video_task_output_folder_path"]

    init_sqlite_db(sqlite_file_path)
    conn = connect_sqlite_db(sqlite_file_path)
    init_hololive_channel_table(conn)
    validate_hololive_channel_table(conn)
    init_dl_yt_video_task_table(conn)
    validate_dl_yt_video_task_table(conn)
    conn.close()

    init_output_folder(output_folder)

    scheduler = BackgroundScheduler(timezone=task_timezone)

    sync_cron_parts = sync_cron.strip().split()
    if len(sync_cron_parts) == 5:
        scheduler.add_job(
            sync_yt_video_task,
            CronTrigger(
                minute=sync_cron_parts[0],
                hour=sync_cron_parts[1],
                day=sync_cron_parts[2],
                month=sync_cron_parts[3],
                day_of_week=sync_cron_parts[4],
            ),
            args=[sqlite_file_path, sync_timeout, sync_max_video, sync_cooldown],
            id="sync_yt_video_task",
            replace_existing=True,
        )
        logger.info(
            "Registered sync_yt_video_task with cron schedule: %s", sync_cron
        )

    dl_cron_parts = dl_cron.strip().split()
    if len(dl_cron_parts) == 5:
        scheduler.add_job(
            dl_yt_video_task,
            CronTrigger(
                minute=dl_cron_parts[0],
                hour=dl_cron_parts[1],
                day=dl_cron_parts[2],
                month=dl_cron_parts[3],
                day_of_week=dl_cron_parts[4],
            ),
            args=[sqlite_file_path, dl_timeout, output_folder],
            id="dl_yt_video_task",
            replace_existing=True,
        )
        logger.info(
            "Registered dl_yt_video_task with cron schedule: %s", dl_cron
        )

    scheduler.start()
    logger.info("Scheduler started. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down scheduler...")
        scheduler.shutdown(wait=False)
        logger.info("Scheduler stopped.")


if __name__ == "__main__":
    main()
