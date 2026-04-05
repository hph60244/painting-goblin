import re
import os
import time
import tempfile
import shutil
import logging
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from threading import Thread
from filelock import FileLock, Timeout
import subprocess
import configparser
from typing import Optional, List, Tuple

# ----------------------------
# 讀取設定檔
# ----------------------------
config = configparser.ConfigParser()
config.read("config.ini")

required_sections = ["task", "publisher", "subscriber"]
for section in required_sections:
    if not config.has_section(section):
        raise ValueError(f"Missing required section in config.ini: [{section}]")

required_task_keys = ["base_dir", "todo_dir", "doing_dir", "done_dir", "failed_dir", "lock_dir", "opencode_exe"]
for key in required_task_keys:
    if key not in config["task"]:
        raise ValueError(f"Missing required key in [task] section: {key}")

BASE_DIR = Path(config["task"]["base_dir"])
TODO_DIR = BASE_DIR / config["task"]["todo_dir"]
DOING_DIR = BASE_DIR / config["task"]["doing_dir"]
DONE_DIR = BASE_DIR / config["task"]["done_dir"]
FAILED_DIR = BASE_DIR / config["task"]["failed_dir"]
LOCK_DIR = BASE_DIR / config["task"]["lock_dir"]
TIMEZONE = config["task"].get("timezone", "UTC")
OPENCODE_EXE = config["task"]["opencode_exe"]

# 驗證 OPENCODE_EXE 是否存在
if not Path(OPENCODE_EXE).exists():
    raise FileNotFoundError(f"OpenCode executable not found: {OPENCODE_EXE}")

PUBLISHER_SLEEP_INTERVAL = float(config["publisher"].get("sleep_interval", 1))
SUBSCRIBER_COUNT = int(config["subscriber"].get("count", 1))
SUBSCRIBER_SLEEP_INTERVAL = float(config["subscriber"].get("sleep_interval", 1))

# 確保資料夾存在
for d in [TODO_DIR, DOING_DIR, DONE_DIR, FAILED_DIR, LOCK_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ----------------------------
# 設定 logging
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('runner.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# ----------------------------
# 工具函數
# ----------------------------
def get_oldest_file(folder: Path) -> Optional[Path]:
    """取得資料夾中最舊的檔案（根據修改時間）"""
    try:
        files = sorted(folder.iterdir(), key=lambda f: f.stat().st_mtime)
        return files[0] if files else None
    except (OSError, PermissionError) as e:
        logger.warning(f"無法讀取資料夾 {folder}: {e}")
        return None

def strip_time_stamp(file_name: str) -> str:
    """移除檔案名稱中的時間戳記"""
    pattern = r'\.(?:[BE]\d{17})'
    name, ext = os.path.splitext(file_name)
    new_name = re.sub(pattern, '', name) + ext
    return new_name

def add_timestamp(file_path: Path, datetime_prefix: str) -> str:
    """為檔案名稱添加時間戳記"""
    now = datetime.now(ZoneInfo(TIMEZONE))
    ts = now.strftime(datetime_prefix + "%Y%m%d%H%M%S%f")[:-3]
    return f"{file_path.stem}.{ts}{file_path.suffix}"

def move_file_safely(src: Path, dest: Path, log_prefix: str = "") -> bool:
    """
    安全地移動檔案，包含錯誤處理和日誌記錄

    Args:
        src: 來源檔案路徑
        dest: 目標檔案路徑
        log_prefix: 日誌前綴

    Returns:
        bool: 移動是否成功
    """
    try:
        shutil.move(str(src), str(dest))
        logger.info(f"{log_prefix}移動 {src.name} -> {dest.name}")
        return True
    except (OSError, PermissionError, shutil.Error) as e:
        logger.error(f"{log_prefix}移動檔案失敗 {src} -> {dest}: {e}")
        return False

def write_error_log(error_msg: str, dest_file: Path) -> None:
    """寫入錯誤日誌到檔案"""
    log_file = dest_file.parent / f"{dest_file.name}.log"
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            timestamp = datetime.now(ZoneInfo(TIMEZONE)).isoformat()
            f.write(f"{timestamp} - {error_msg}\n")
        logger.info(f"錯誤日誌已寫入: {log_file}")
    except (OSError, PermissionError) as e:
        logger.error(f"無法寫入錯誤日誌 {log_file}: {e}")

# ----------------------------
# Publisher
# ----------------------------
def publisher() -> None:
    """從 TODO_DIR 移動任務到 DOING_DIR"""
    # 檢查是否有空閒的 subscriber
    doing_files = list(DOING_DIR.iterdir())
    if len(doing_files) >= SUBSCRIBER_COUNT:
        logger.debug(f"[Publisher] 所有 subscriber 都忙碌中，DOING_DIR 有 {len(doing_files)} 個檔案")
        return

    # 檢查 TODO_DIR 裡面是否有要執行的任務檔案
    task_file = get_oldest_file(TODO_DIR)
    if not task_file:
        logger.debug("[Publisher] TODO_DIR 中沒有待處理的任務")
        return

    lock_file = LOCK_DIR / f"{task_file.name}.lock"
    try:
        with FileLock(str(lock_file), timeout=0.1):
            if not task_file.exists():
                logger.debug(f"[Publisher] 任務檔案鎖定前被取走: {task_file}")
                return

            clean_name = strip_time_stamp(task_file.name)
            dest = DOING_DIR / add_timestamp(Path(clean_name), "B")

            if not move_file_safely(task_file, dest, "[Publisher] "):
                logger.error(f"[Publisher] 移動任務失敗: {task_file.name}")
    except Timeout:
        logger.debug(f"[Publisher] 檔案鎖定超時: {lock_file}")
    except Exception as e:
        logger.error(f"[Publisher] 發生未預期錯誤: {e}")

# ----------------------------
# Subscriber
# ----------------------------
def execute_task(file_path: Path) -> None:
    """執行單個任務"""
    lock_file = LOCK_DIR / f"{file_path.name}.lock"
    try:
        with FileLock(str(lock_file), timeout=0.1):
            if not file_path.exists():
                logger.warning(f"任務檔案不存在: {file_path}")
                return

            logger.info(f"開始執行任務: {file_path.name}")

            try:
                # 在臨時目錄中執行任務
                with tempfile.TemporaryDirectory() as tmpdir:
                    tmp_task = Path(tmpdir) / file_path.name
                    shutil.copy(str(file_path), str(tmp_task))

                    logger.debug(f"在臨時目錄執行: {tmpdir}")
                    result = subprocess.run(
                        [OPENCODE_EXE, "run", "Execute this task", "--file", str(tmp_task)],
                        check=True,
                        cwd=tmpdir,
                        capture_output=True
                    )
                    stdout_text = result.stdout.decode("utf-8", errors="replace")
                    logger.debug(f"任務執行輸出: {stdout_text[:200]}...")
                    if result.stderr:
                        stderr_text = result.stderr.decode("utf-8", errors="replace")
                        logger.warning(f"任務執行錯誤輸出: {stderr_text[:200]}...")

                # 任務成功，移動到完成目錄
                dest = DONE_DIR / add_timestamp(file_path, "E")
                if move_file_safely(file_path, dest, "[Subscriber] "):
                    logger.info(f"任務完成: {file_path.name} -> {dest.name}")
                else:
                    logger.error(f"移動完成任務失敗: {file_path.name}")

            except subprocess.CalledProcessError as e:
                error_msg = f"任務執行失敗 (exit code {e.returncode}): {e}"
                logger.error(error_msg)
                if e.stdout:
                    logger.debug(f"失敗任務的輸出: {e.stdout[:500]}")
                if e.stderr:
                    logger.debug(f"失敗任務的錯誤: {e.stderr[:500]}")

                # 任務失敗，移動到失敗目錄
                dest = FAILED_DIR / file_path.name
                write_error_log(error_msg, dest)
                if not move_file_safely(file_path, dest, "[Subscriber] "):
                    logger.error(f"移動失敗任務失敗: {file_path.name}")

            except Exception as e:
                error_msg = f"任務執行發生未預期錯誤: {e}"
                logger.error(error_msg)

                # 任務失敗，移動到失敗目錄
                dest = FAILED_DIR / file_path.name
                write_error_log(error_msg, dest)
                if not move_file_safely(file_path, dest, "[Subscriber] "):
                    logger.error(f"移動失敗任務失敗: {file_path.name}")

    except Timeout:
        logger.debug(f"檔案鎖定超時: {lock_file}")
    except Exception as e:
        logger.error(f"execute_task 發生未預期錯誤: {e}")

def subscriber_worker() -> None:
    """Subscriber worker: 持續從 DOING_DIR 取得並執行任務"""
    logger.info("Subscriber worker 啟動")
    while True:
        try:
            task_file = get_oldest_file(DOING_DIR)
            if task_file:
                execute_task(task_file)
            else:
                logger.debug("DOING_DIR 中沒有待執行的任務")

            time.sleep(SUBSCRIBER_SLEEP_INTERVAL)
        except KeyboardInterrupt:
            logger.info("Subscriber worker 收到中斷訊號，結束")
            break
        except Exception as e:
            logger.error(f"Subscriber worker 發生錯誤: {e}")
            time.sleep(SUBSCRIBER_SLEEP_INTERVAL)  # 避免錯誤循環

# ----------------------------
# 主程式
# ----------------------------
def main() -> None:
    """主程式入口點"""
    logger.info("=" * 50)
    logger.info("任務處理系統啟動")
    logger.info(f"配置: {SUBSCRIBER_COUNT} 個 subscriber, publisher 間隔: {PUBLISHER_SLEEP_INTERVAL}s")
    logger.info(f"目錄結構: TODO={TODO_DIR}, DOING={DOING_DIR}, DONE={DONE_DIR}, FAILED={FAILED_DIR}")
    logger.info("=" * 50)

    # 啟動多個 subscriber worker
    threads: List[Thread] = []
    for i in range(SUBSCRIBER_COUNT):
        t = Thread(target=subscriber_worker, daemon=True, name=f"Subscriber-{i+1}")
        t.start()
        threads.append(t)
        logger.info(f"啟動 subscriber worker: {t.name}")

    logger.info("系統已啟動，按 Ctrl+C 結束")

    try:
        while True:
            publisher()
            time.sleep(PUBLISHER_SLEEP_INTERVAL)
    except KeyboardInterrupt:
        logger.info("收到中斷訊號，正在關閉系統...")
    except Exception as e:
        logger.error(f"主程式發生未預期錯誤: {e}")
    finally:
        logger.info("系統關閉完成")

if __name__ == "__main__":
    main()
