"""
任務處理系統 - Runner

這個模組實現了一個基於檔案系統的任務處理系統，包含 Publisher 和 Subscriber 兩種角色：
- Publisher: 從待處理目錄 (todo) 移動任務到處理中目錄 (doing)
- Subscriber: 從處理中目錄執行任務，並根據結果移動到完成或失敗目錄

系統使用檔案鎖定機制來確保任務不會被多個 worker 同時處理。
"""

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
from typing import Optional, List

# ============================================================================
# 設定 logging (會在 Config.__init__ 中重新配置)
# ============================================================================
logger = logging.getLogger(__name__)

# ============================================================================
# 配置結構
# ============================================================================
class Config:
    """
    配置類，儲存所有系統設定值

    這個類別負責讀取和驗證配置文件，並提供所有必要的配置參數給系統使用。
    """
    def __init__(self, config_path: str):
        """
        初始化配置物件

        Args:
            config_path: 配置檔案路徑

        Raises:
            ValueError: 如果配置檔案缺少必要的區段
            FileNotFoundError: 如果 OpenCode 執行檔不存在
        """
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        # 驗證必要的區段
        required_sections = ["task", "runner"]
        for section in required_sections:
            if not self.config.has_section(section):
                raise ValueError(f"Missing required section in {config_path}: [{section}]")

        # 讀取 task 設定
        self.base_dir_name = self.config["task"].get("base_dir_name", "task")
        self.todo_dir_name = self.config["task"].get("todo_dir_name", "todo")
        self.doing_dir_name = self.config["task"].get("doing_dir_name", "doing")
        self.done_dir_name = self.config["task"].get("done_dir_name", "done")
        self.failed_dir_name = self.config["task"].get("failed_dir_name", "failed")
        self.log_dir_name = self.config["task"].get("log_dir_name", ".logs")
        self.lock_dir_name = self.config["task"].get("lock_dir_name", ".locks")
        self.timezone = self.config["task"].get("timezone", "Asia/Taipei")
        self.opencode_exe = self.config["task"]["opencode_exe"]

        # 驗證 OPENCODE_EXE 是否存在
        if not Path(self.opencode_exe).exists():
            raise FileNotFoundError(f"OpenCode executable not found: {self.opencode_exe}")

        # 讀取 runner 設定
        self.runner_log_dir_name = self.config["runner"].get("log_dir_name", "log")
        self.publisher_count = int(self.config["runner"].get("publisher_count", 1))
        self.publisher_heartbeat_secs = float(self.config["runner"].get("publisher_heartbeat_secs", 60))
        self.subscriber_count = int(self.config["runner"].get("subscriber_count", 1))
        self.subscriber_heartbeat_secs = float(self.config["runner"].get("subscriber_heartbeat_secs", 60))

        # 計算目錄路徑
        root_dir = Path(os.getenv("PAINTING_GOBLIN_DIR"))
        self.base_dir = root_dir / self.base_dir_name
        self.todo_dir = self.base_dir / self.todo_dir_name
        self.doing_dir = self.base_dir / self.doing_dir_name
        self.done_dir = self.base_dir / self.done_dir_name
        self.failed_dir = self.base_dir / self.failed_dir_name
        self.log_dir = self.base_dir / self.log_dir_name
        self.lock_dir = self.base_dir / self.lock_dir_name
        self.runner_log_dir = root_dir / self.runner_log_dir_name

        # 確保所有必要的資料夾都存在
        for d in [self.todo_dir, self.doing_dir, self.done_dir, self.failed_dir, self.log_dir, self.lock_dir, self.runner_log_dir]:
            d.mkdir(parents=True, exist_ok=True)

        # 設置 logging
        # 清除現有的 handlers
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        # 配置 root logger
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)-5s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(self.runner_log_dir / "runner.log", encoding="utf-8")
            ],
            force=True  # 強制重新配置，即使已經有 handlers
        )

        # 重新獲取 logger 以確保使用新的配置
        global logger
        logger = logging.getLogger(__name__)

# ============================================================================
# 工具函數
# ============================================================================

# 任務檔案副檔名設定
task_file_extension: str = ".md"

def find_task_files(folder: Path, lock_dir: Path, locked: bool) -> List[Path]:
    """
    在指定資料夾中尋找任務檔案，並根據鎖定狀態進行篩選

    Args:
        folder: 要搜尋的資料夾路徑
        lock_dir: 檔案鎖定目錄，用於檢查檔案是否被鎖定
        locked: 是否要尋找已鎖定的檔案 (True) 或未鎖定的檔案 (False)

    Returns:
        List[Path]: 符合條件的任務檔案路徑列表
    """
    try:
        task_files = [
            f for f in folder.iterdir()
            if f.is_file() and f.suffix.lower() == task_file_extension
        ]
        result_files = []
        for task_file in task_files:
            lock_file = build_lock_file_path(task_file, lock_dir)
            if locked == lock_file.exists():
                result_files.append(task_file)
        return result_files
    except Exception as e:
        logger.error(f"取得任務檔案列表時發生未預期錯誤: {e}")
        return []

def get_oldest_unlocked_task_file(folder: Path, lock_dir: Path) -> Optional[Path]:
    """
    取得資料夾中最舊的任務檔案（根據修改時間），並篩選沒被上鎖的檔案

    Args:
        folder: 要搜尋的資料夾路徑
        lock_dir: 檔案鎖定目錄，用於檢查檔案是否被鎖定

    Returns:
        最舊的未鎖定任務檔案路徑，如果資料夾中沒有符合條件的檔案則返回 None
    """
    try:
        task_files = find_task_files(folder, lock_dir, False)

        if not task_files:
            logger.debug(f"資料夾 {folder} 中沒有 {task_file_extension} 檔案")
            return None

        # 根據修改時間排序，取得最舊的檔案
        oldest_file = min(task_files, key=lambda f: f.stat().st_mtime)
        logger.debug(f"在資料夾 {folder} 中找到最舊的未鎖定 {task_file_extension} 檔案: {oldest_file.name}")
        return oldest_file

    except (OSError, PermissionError) as e:
        logger.warning(f"無法讀取資料夾 {folder}: {e}")
        return None
    except Exception as e:
        logger.error(f"取得最舊檔案時發生未預期錯誤: {e}")
        return None

def strip_time_stamp(file_name: str) -> str:
    """
    移除檔案名稱中的時間戳記

    Args:
        file_name: 原始檔案名稱

    Returns:
        移除時間戳記後的檔案名稱
    """
    pattern = r"\.(?:[BE]\d{14})"
    name, ext = os.path.splitext(file_name)
    new_name = re.sub(pattern, "", name) + ext
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
    ts = now.strftime(datetime_prefix + "%Y%m%d%H%M%S")
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

def build_lock_file_path(task_file: Path, lock_dir: Path) -> Path:
    """
    根據任務檔案路徑和鎖定目錄生成對應的鎖定檔案路徑

    Args:
        task_file: 任務檔案路徑
        lock_dir: 鎖定檔案目錄

    Returns:
        Path: 鎖定檔案路徑
    """
    return lock_dir / f"{task_file.name}.lock"

# ============================================================================
# Publisher
# ============================================================================
def publisher(file_path: Path, todo_dir: Path, doing_dir: Path, lock_dir: Path, subscriber_count: int, timezone: str) -> None:
    """
    移動單個任務從 todo_dir 到 doing_dir

    Args:
        file_path: 要移動的任務檔案路徑
        todo_dir: 待處理任務目錄
        doing_dir: 處理中任務目錄
        lock_dir: 檔案鎖定目錄，用於檢查檔案是否被鎖定
        subscriber_count: 訂閱者數量（用於檢查是否忙碌）
        timezone: 時區設定
    """
    doing_task_files = find_task_files(doing_dir, lock_dir, True)
    doing_file_count = len(doing_task_files)
    if doing_file_count >= subscriber_count:
        logger.debug(f"[Publisher] 所有 subscriber 都忙碌中，doing_dir 有 {doing_file_count} 個任務檔案")
        return

    logger.info(f"[Publisher] 開始移動任務: {file_path.name}")
    try:
        clean_name = strip_time_stamp(file_path.name)
        dest = doing_dir / add_timestamp(Path(clean_name), "B", timezone)
        if move_file_safely(file_path, dest, "[Publisher]"):
            logger.info(f"[Publisher] 移動任務成功: {file_path.name}")
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
            task_file = get_oldest_unlocked_task_file(todo_dir, lock_dir)
            if task_file:
                lock_file = build_lock_file_path(task_file, lock_dir)
                try:
                    with FileLock(str(lock_file), timeout=0):
                        publisher(task_file, todo_dir, doing_dir, lock_dir, subscriber_count, timezone)
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

    # 開啟日誌檔案以附加模式寫入，確保所有輸出都被記錄
    with open(log_file, "a", encoding="utf-8") as f:
        try:
            # 執行 OpenCode 命令來處理任務
            result = subprocess.run(
                [opencode_exe, "run", "Execute this task. Only read the files specifically mentioned.", "--file", str(file_path)],
                check=True, cwd=doing_dir, stdout=f, stderr=f,
            )

            # 任務成功執行，移動到完成目錄並添加結束時間戳記
            dest = done_dir / add_timestamp(file_path, "E", timezone)
            logger.info(f"[Subscriber] 執行任務成功: {file_path.name}")
            move_file_safely(file_path, dest, "[Subscriber]")

        except subprocess.CalledProcessError as e:
            # OpenCode 命令執行失敗，移動到失敗目錄
            logger.error(f"[Subscriber] 執行任務失敗: {file_path.name}, {e}")
            dest = failed_dir / file_path.name
            move_file_safely(file_path, dest, "[Subscriber]")

        except Exception as e:
            # 其他未預期的錯誤，移動到失敗目錄
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
            task_file = get_oldest_unlocked_task_file(doing_dir, lock_dir)
            if task_file:
                lock_file = build_lock_file_path(task_file, lock_dir)
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
    主程式入口點：啟動任務處理系統

    這個函數負責：
    1. 啟動指定數量的 publisher worker 執行緒
    2. 啟動指定數量的 subscriber worker 執行緒
    3. 監控系統執行狀態，等待中斷訊號

    Args:
        config: 配置物件，包含所有系統設定
    """
    logger.info("[Runner] 任務處理系統啟動")

    threads: List[Thread] = []

    # 啟動多個 publisher worker 執行緒
    for i in range(config.publisher_count):
        t = Thread(
            target=publisher_worker,
            args=(
                config.todo_dir, config.doing_dir, config.lock_dir,
                config.subscriber_count, config.timezone, config.publisher_heartbeat_secs
            ),
            daemon=True,
            name=f"PublisherWorker{i}"
        )
        t.start()
        threads.append(t)
        logger.info(f"[Runner] 啟動: {t.name}")

    # 啟動多個 subscriber worker 執行緒
    for i in range(config.subscriber_count):
        t = Thread(
            target=subscriber_worker,
            args=(
                config.doing_dir, config.lock_dir, config.log_dir,
                config.opencode_exe, config.done_dir, config.failed_dir,
                config.timezone, config.subscriber_heartbeat_secs
            ),
            daemon=True,
            name=f"SubscriberWorker{i}"
        )
        t.start()
        threads.append(t)
        logger.info(f"[Runner] 啟動: {t.name}")

    logger.info("[Runner] 系統已啟動，按 Ctrl+C 結束")

    try:
        # 主執行緒持續執行，等待中斷訊號
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("[Runner] 收到中斷訊號，正在關閉...")
    except Exception as e:
        logger.error(f"[Runner] 主程式發生未預期錯誤: {e}")
    finally:
        logger.info("[Runner] 任務處理系統關閉完成")


if __name__ == "__main__":
    """
    程式進入點：當此檔案被直接執行時啟動任務處理系統

    使用方式：
        python runner.py [config_file_path]

    參數：
        config_file_path: 可選的配置檔案路徑，預設為 "config.ini"
    """
    # 讀取命令列參數，如果沒有提供則使用預設配置檔案
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.ini"

    # 建立配置物件並啟動系統
    config = Config(config_path)
    runner(config)
