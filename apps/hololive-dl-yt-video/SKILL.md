---
name: hololive-dl-yt-video
description: Download Hololive members' YouTube videos with scheduled syncing and downloading. Uses apscheduler for cron-based scheduling, yt-dlp for video extraction/download, and SQLite for task tracking. Use when asked to download Hololive videos, sync YouTube channels, or set up automated video downloading for VTuber content.
---

# hololive-dl-yt-video

Downloads Hololive members' YouTube videos using scheduled tasks. Syncs channel video lists and downloads new videos automatically.

## Usage

```bash
python hololive-dl-yt-video.py [config_file_path]
```

- `config_file_path` - Path to INI config file (default: `hololive-dl-yt-video.ini`). Auto-created with defaults if missing.

## Config File (`hololive-dl-yt-video.ini`)

```ini
[general]
sqlite_file_path = hololive-dl-yt-video.sqlite3
task_timezone = Asia/Taipei
sync_yt_video_task_cron_schedule = */5 * * * *
sync_yt_video_task_timeout_minutes = 5
sync_yt_video_task_max_video_minutes = 10
sync_yt_video_task_cooldown_minutes = 1440
dl_yt_video_task_cron_schedule = * * * * *
dl_yt_video_task_timeout_minutes = 5
dl_yt_video_task_output_folder_path = downloads
verify_dl_yt_video_task_cron_schedule = 0 0 * * *
```

## How It Works

1. **sync_yt_video_task** (cron: `*/5 * * * *`): For each channel in `hololive_channel`, fetches video list from YouTube, creates download tasks (under 10 min videos only).
2. **dl_yt_video_task** (cron: `* * * * *`): Downloads one pending video at a time to `downloads/<talent_name>/<title>.mp4`.
3. **verify_dl_yt_video_task** (cron: `0 0 * * *`): Checks completed downloads daily, marks tasks as FAILED if files are missing or invalid.

## Adding a Channel

```sql
INSERT INTO hololive_channel (channel_id, talent_name, updated_at, status)
VALUES ('UCqm3BQLlJfvkTsX_hvm0UmA', 'tsunomaki-watame', '2000-01-01 00:00:00', 'FAILED');
```

## Requirements

- Python 3.8+
- APScheduler >= 3.10
- yt-dlp >= 2023.0
- pytz >= 2023.0
