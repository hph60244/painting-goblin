import re
import os
import sys
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
from typing import Optional, List, Tuple, Dict, Any

# ============================================================================
# 設定 logging
# ============================================================================
logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-5s | %(name)s:%(funcName)s:%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('runner.log', encoding='utf-8')
    ]
)

# ============================================================================
# 配置結構
# ============================================================================
class Config:
    """配置類，儲存所有設定值"""
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        # 驗證必要的區段
        required_sections = ["task", "publisher", "subscriber"]
        for section in required_sections:
            if not self.config.has_section(section):
                raise ValueError(f"Missing required section in {config_path}: [{section}]")

        # 讀取 task 設定
        self.base_dir_name = self.config["task"].get("base_dir_name", "base")
        self.todo_dir_name = self.config["task"].get("todo_dir_name", "todo")
        self.doing_dir_name = self.config["task"].get("doing_dir_name", "doing")
        self.done_dir_name = self.config["task"].get("done_dir_name", "done")
        self.failed_dir_name = self.config["task"].get("failed_dir_name", "failed")
        self.log_dir_name = self.config["task"].get("log_dir_name", ".logs")
        self.lock_dir_name = self.config["task"].get("lock_dir_name", ".locks")
        self.timezone = self.config["task"].get("timezone", "UTC")
        self.opencode_exe = self.config["task"].get("opencode_exe", "")

        # 驗證 OPENCODE_EXE 是否存在
        if not Path(self.opencode_exe).exists():
            raise FileNotFoundError(f"OpenCode executable not found: {self.opencode_exe}")

        # 讀取 publisher 設定
        self.publisher_count = int(self.config["publisher"].get("count", 1))
        self.publisher_heartbeat_secs = float(self.config["publisher"].get("heartbeat_secs", 60))

        # 讀取 subscriber 設定
        self.subscriber_count = int(self.config["subscriber"].get("count", 1))
        self.subscriber_heartbeat_secs = float(self.config["subscriber"].get("heartbeat_secs", 60))

        # 計算目錄路徑
        self.base_dir = Path(os.getenv("PAINTING_GOBLIN_DIR")) / self.base_dir_name
        self.todo_dir = self.base_dir / self.todo_dir_name
        self.doing_dir = self.base_dir / self.doing_dir_name
        self.done_dir = self.base_dir / self.done_dir_name
        self.failed_dir = self.base_dir / self.failed_dir_name
        self.log_dir = self.base_dir / self.log_dir_name
        self.lock_dir = self.base_dir / self.lock_dir_name

        # 確保資料夾存在
        for d in [self.todo_dir, self.doing_dir, self.done_dir, self.failed_dir, self.log_dir, self.lock_dir]:
            d.mkdir(parents=True, exist_ok=True)

# ============================================================================
# 工具函數
# ============================================================================
def get_oldest_file(folder: Path) -> Optional[Path]:
    """
    取得資料夾中最舊的檔案（根據修改時間）

    Args:
        folder: 要搜尋的資料夾路徑

    Returns:
        最舊的檔案路徑，如果資料夾為空則返回 None
    """
    try:
        files = sorted(folder.iterdir(), key=lambda f: f.stat().st_mtime)
        return files[0] if files else None
    except (OSError, PermissionError) as e:
        logger.debug(f"無法讀取資料夾 {folder}: {e}")
        return None

def strip_time_stamp(file_name: str) -> str:
    """
    移除檔案名稱中的時間戳記

    Args:
        file_name: 原始檔案名稱

    Returns:
        移除時間戳記後的檔案名稱
    """
    pattern = r'\.(?:[BE]\d{17})'
    name, ext = os.path.splitext(file_name)
    new_name = re.sub(pattern, '', name) + ext
    return new_name

def add_timestamp(file_path: Path, datetime_prefix: str, timezone: str) -> str:
    """
    為檔案名稱添加時間戳記

    Args:
        file_path: 原始檔案路徑
        datetime_prefix: 時間戳記前綴（例如："B" 表示開始，"E" 表示結束）
        timezone: 時區設定

    Returns:
        添加時間戳記後的檔案名稱
    """
    now = datetime.now(ZoneInfo(timezone))
    ts = now.strftime(datetime_prefix + "%Y%m%d%H%M%S%f")[:-3]
    return f"{file_path.stem}.{ts}{file_path.suffix}"

def move_file_safely(src: Path, dest: Path, log_prefix: str) -> bool:
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
        logger.debug(f"{log_prefix} 移動: {src.name}, {dest.name}")
        return True
    except (OSError, PermissionError, shutil.Error) as e:
        logger.error(f"{log_prefix}移動檔案失敗: {src}, {dest}, {e}")
        return False

# ============================================================================
# Publisher
# ============================================================================
def publisher(file_path: Path, todo_dir: Path, doing_dir: Path, subscriber_count: int, timezone: str) -> None:
    """
    移動單個任務從 todo_dir 到 doing_dir

    Args:
        file_path: 要移動的任務檔案路徑
        todo_dir: 待處理任務目錄
        doing_dir: 處理中任務目錄
        subscriber_count: 訂閱者數量（用於檢查是否忙碌）
        timezone: 時區設定
    """
    doing_file_count = len(list(doing_dir.iterdir()))
    if doing_file_count >= subscriber_count:
        logger.debug(f"[Publisher] 所有 subscriber 都忙碌中，doing_dir 有 {doing_file_count} 個檔案")
        return

    logger.info(f"[Publisher] 開始移動任務: {file_path.name}")
    try:
        clean_name = strip_time_stamp(file_path.name)
        dest = doing_dir / add_timestamp(Path(clean_name), "B", timezone)
        if move_file_safely(file_path, dest, "[Publisher]"):
            logger.error(f"[Publisher] 移動任務成功: {file_path.name}")
    except Exception as e:
        logger.error(f"[Publisher] 移動任務發生未預期錯誤: {file_path.name}, {e}")

def publisher_worker(todo_dir: Path, doing_dir: Path, lock_dir: Path, subscriber_count: int, timezone: str, publisher_heartbeat_secs: float) -> None:
    """
    Publisher worker: 持續從 todo_dir 移動任務到 doing_dir

    Args:
        todo_dir: 待處理任務目錄
        doing_dir: 處理中任務目錄
        lock_dir: 檔案鎖定目錄
        subscriber_count: 訂閱者數量
        timezone: 時區設定
        publisher_heartbeat_secs: 心跳間隔秒數（當沒有任務時等待的時間）
    """
    while True:
        try:
            task_file = get_oldest_file(todo_dir)
            if task_file:
                lock_file = lock_dir / f"{task_file.name}.lock"
                try:
                    with FileLock(str(lock_file), timeout=0):
                        publisher(task_file, todo_dir, doing_dir, subscriber_count, timezone)
                except Timeout:
                    logger.debug(f"[PublisherWorker] 檔案鎖定超時: {lock_file}")
            else:
                logger.debug("[PublisherWorker] todo_dir 中沒有待執行的任務")
        except KeyboardInterrupt:
            logger.info("[PublisherWorker] 收到中斷訊號，正在關閉...")
            break
        except Exception as e:
            logger.error(f"[PublisherWorker] 發生錯誤: {e}")
            time.sleep(publisher_heartbeat_secs)

# ============================================================================
# Subscriber
# ============================================================================
def subscriber(file_path: Path, log_dir: Path, opencode_exe: str, doing_dir: Path, done_dir: Path, failed_dir: Path, timezone: str) -> None:
    """
    執行單個任務

    Args:
        file_path: 任務檔案路徑
        log_dir: 日誌目錄
        opencode_exe: OpenCode 執行檔路徑
        doing_dir: 處理中任務目錄
        done_dir: 已完成任務目錄
        failed_dir: 失敗任務目錄
        timezone: 時區設定
    """
    logger.info(f"[Subscriber] 開始執行任務: {file_path.name}")
    log_file = log_dir / f"{file_path.name}.log"
    with open(log_file, "a", encoding="utf-8") as f:
        try:
            result = subprocess.run(
                [opencode_exe, "run", "Execute this task", "--file", str(file_path)],
                check=True, cwd=doing_dir, stdout=f, stderr=f,
            )
            # 任務成功，移動到完成目錄
            dest = done_dir / add_timestamp(file_path, "E", timezone)
            logger.error(f"[Subscriber] 執行任務成功: {file_path.name}")
            move_file_safely(file_path, dest, "[Subscriber]")
        except subprocess.CalledProcessError as e:
            logger.error(f"[Subscriber] 執行任務失敗: {file_path.name}, {e}")
            dest = failed_dir / file_path.name
            move_file_safely(file_path, dest, "[Subscriber]")
        except Exception as e:
            logger.error(f"[Subscriber] 執行任務發生未預期錯誤: {file_path.name}, {e}")
            dest = failed_dir / file_path.name
            move_file_safely(file_path, dest, "[Subscriber]")

def subscriber_worker(doing_dir: Path, lock_dir: Path, log_dir: Path, opencode_exe: str, done_dir: Path, failed_dir: Path, timezone: str, subscriber_heartbeat_secs: float) -> None:
    """
    Subscriber worker: 持續從 doing_dir 取得並執行任務

    Args:
        doing_dir: 處理中任務目錄
        lock_dir: 檔案鎖定目錄
        log_dir: 日誌目錄
        opencode_exe: OpenCode 執行檔路徑
        done_dir: 已完成任務目錄
        failed_dir: 失敗任務目錄
        timezone: 時區設定
        subscriber_heartbeat_secs: 心跳間隔秒數（當沒有任務時等待的時間）
    """
    while True:
        try:
            task_file = get_oldest_file(doing_dir)
            if task_file:
                lock_file = lock_dir / f"{task_file.name}.lock"
                try:
                    with FileLock(str(lock_file), timeout=0):
                        subscriber(task_file, log_dir, opencode_exe, doing_dir, done_dir, failed_dir, timezone)
                except Timeout:
                    logger.debug(f"[SubscriberWorker] 檔案鎖定超時: {lock_file}")
            else:
                logger.debug("[SubscriberWorker] doing_dir 中沒有待執行的任務")
            time.sleep(subscriber_heartbeat_secs)
        except KeyboardInterrupt:
            logger.info("[SubscriberWorker] 收到中斷訊號，正在關閉...")
            break
        except Exception as e:
            logger.error(f"[SubscriberWorker] 發生錯誤: {e}")
            time.sleep(subscriber_heartbeat_secs)

# ============================================================================
# 主程式
# ============================================================================
def runner(config: Config) -> None:
    """
    主程式入口點

    Args:
        config: 配置物件，包含所有系統設定
    """
    # 讀取配置
    logger.info("[Runner] 任務處理系統啟動")

    threads: List[Thread] = []

    # 啟動多個 publisher worker
    for i in range(config.publisher_count):
        t = Thread(
            target=publisher_worker,
            args=(
                config.todo_dir, config.doing_dir, config.lock_dir, config.subscriber_count, config.timezone, config.publisher_heartbeat_secs
            ),
            daemon=True,
            name=f"PublisherWorker{i}"
        )
        t.start()
        threads.append(t)
        logger.info(f"[Runner] 啟動: {t.name}")

    # 啟動多個 subscriber worker
    for i in range(config.subscriber_count):
        t = Thread(
            target=subscriber_worker,
            args=(
                config.doing_dir, config.lock_dir, config.log_dir, config.opencode_exe, config.done_dir, config.failed_dir, config.timezone, config.subscriber_heartbeat_secs
            ),
            daemon=True,
            name=f"SubscriberWorker{i}"
        )
        t.start()
        threads.append(t)
        logger.info(f"[Runner] 啟動: {t.name}")

    logger.info("[Runner] 系統已啟動，按 Ctrl+C 結束")

    try:
        # 主執行緒等待所有 worker 執行緒
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("[Runner] 收到中斷訊號，正在關閉...")
    except Exception as e:
        logger.error(f"[Runner] 主程式發生未預期錯誤: {e}")
    finally:
        logger.info("[Runner] 任務處理系統關閉完成")

if __name__ == "__main__":
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.ini"
    config = Config(config_path)
    runner(config)
