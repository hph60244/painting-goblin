"""
任務處理系統 - Runner

基於檔案系統的任務處理系統，包含 Publisher 和 Subscriber 兩種角色：
- Publisher: 從待處理目錄移動任務到處理中目錄
- Subscriber: 執行任務並根據結果移動到完成或失敗目錄

使用檔案鎖定機制確保任務不會被多個 worker 同時處理。
"""

import re
import os
import sys
import time
import shutil
import logging
import uuid
import base64
from pathlib import Path
from threading import Thread
from filelock import FileLock, Timeout
import subprocess
import configparser
from typing import List, Optional, Tuple

# ============================================================================
# 設定 logging (會在 Config.__init__ 中重新配置)
# ============================================================================
logger = logging.getLogger(__name__)

# ============================================================================
# 配置結構
# ============================================================================
class Config:
    """系統配置類，讀取和驗證配置文件"""
    def __init__(self, config_path: str):
        """初始化配置物件"""
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        # 驗證必要的區段
        required_sections = ["task", "runner"]
        for section in required_sections:
            if not self.config.has_section(section):
                raise ValueError(f"Missing required section in {config_path}: [{section}]")

        # 讀取 task 設定
        self.base_dir_name = self.config["task"].get("base_dir_name", "tasks")
        self.todo_dir_name = self.config["task"].get("todo_dir_name", "todo")
        self.doing_dir_name = self.config["task"].get("doing_dir_name", "doing")
        self.done_dir_name = self.config["task"].get("done_dir_name", "done")
        self.failed_dir_name = self.config["task"].get("failed_dir_name", "failed")
        self.log_dir_name = self.config["task"].get("log_dir_name", ".logs")
        self.lock_dir_name = self.config["task"].get("lock_dir_name", ".locks")
        self.opencode_exe = self.config["task"]["opencode_exe"]

        # 驗證 OPENCODE_EXE 是否存在
        if not Path(self.opencode_exe).exists():
            raise FileNotFoundError(f"OpenCode executable not found: {self.opencode_exe}")

        # 讀取 runner 設定
        self.runner_log_dir_name = self.config["runner"].get("log_dir_name", "logs")
        self.publisher_count = int(self.config["runner"].get("publisher_count", 1))
        self.publisher_heartbeat_sec = float(self.config["runner"].get("publisher_heartbeat_sec", 60))
        self.subscriber_count = int(self.config["runner"].get("subscriber_count", 1))
        self.subscriber_heartbeat_sec = float(self.config["runner"].get("subscriber_heartbeat_sec", 60))
        self.monitor_timeout_sec = float(self.config["runner"].get("monitor_timeout_sec", 60))
        self.monitor_terminate_sec = float(self.config["runner"].get("monitor_terminate_sec", 5))
        self.monitor_heartbeat_sec = float(self.config["runner"].get("monitor_heartbeat_sec", 5))

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
            format="%(asctime)s | %(levelname)-5s | %(message)s",
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
TASK_FILE_EXTENSION: str = ".md"
UUID_PATTERN = re.compile(r"\.[A-Za-z0-9_-]{22}$")

def try_lock(lock_file: str) -> Optional[FileLock]:
    """非阻塞方式嘗試取得檔案鎖"""
    lock = FileLock(lock_file)
    try:
        lock.acquire(timeout=0)  # timeout=0 表示非阻塞模式
        return lock
    except Timeout:
        return None

def release_lock(lock: FileLock) -> None:
    """釋放檔案鎖"""
    if lock.is_locked:
        lock.release()

def build_lock_file_path(task_file: Path, lock_dir: Path) -> Path:
    """根據任務檔案路徑生成對應的鎖定檔案路徑"""
    return lock_dir / f"{task_file.name}.lock"

def find_task_files(folder: Path, log_prefix: str) -> Optional[List[Path]]:
    """在指定資料夾中尋找任務檔案"""
    try:
        task_files = [
            f for f in folder.iterdir()
            if f.is_file() and f.suffix.lower() == TASK_FILE_EXTENSION
        ]
        return task_files
    except Exception as e:
        logger.error(f"{log_prefix} 取得任務檔案列表時發生未預期錯誤: {e}")
        return None

def get_oldest_task_file_lock(folder: Path, lock_dir: Path, log_prefix: str) -> Optional[Tuple[Path, FileLock]]:
    """取得資料夾中最舊的未鎖定任務檔案"""
    try:
        task_files = find_task_files(folder, log_prefix)

        if not task_files:
            logger.debug(f"{log_prefix} 資料夾 {folder} 中找不到任務檔案")
            return None

        # 根據修改時間排序
        sorted_task_files = sorted(task_files, key=lambda p: p.stat().st_mtime)

        # 取得最舊的未鎖定檔案
        for sorted_task_file in sorted_task_files:
            lock = try_lock(build_lock_file_path(sorted_task_file, lock_dir))
            if lock:
                return (sorted_task_file, lock)

        return None
    except (OSError, PermissionError) as e:
        logger.warning(f"{log_prefix} 無法讀取資料夾 {folder}: {e}")
        return None
    except Exception as e:
        logger.error(f"{log_prefix} 取得最舊檔案時發生未預期錯誤: {e}")
        return None

def generate_short_uuid() -> str:
    """生成簡短的 UUID 字串（22個字元）"""
    u = uuid.uuid4()
    return base64.urlsafe_b64encode(u.bytes).rstrip(b'=').decode('ascii')

def remove_uuid(file_name: str) -> str:
    """移除檔案名稱中的 UUID"""
    name, ext = os.path.splitext(file_name)
    new_name = re.sub(UUID_PATTERN, "", name) + ext
    return new_name

def add_uuid(file_path: Path) -> str:
    """為檔案名稱添加 UUID 以避免名稱衝突"""
    short_id = generate_short_uuid()
    return f"{file_path.stem}.{short_id}{file_path.suffix}"

def move_file_safely(src: Path, dest: Path, log_prefix: str) -> bool:
    """安全地移動檔案，包含錯誤處理和日誌記錄"""
    try:
        shutil.move(str(src), str(dest))
        logger.debug(f"{log_prefix} 移動: {src}, {dest}")
        return True
    except (OSError, PermissionError, shutil.Error) as e:
        logger.error(f"{log_prefix} 移動檔案失敗: {src}, {dest}, {e}")
        return False

# ============================================================================
# Publisher
# ============================================================================
def publisher(file_path: Path, todo_dir: Path, doing_dir: Path, lock_dir: Path, subscriber_count: int) -> None:
    """移動單個任務從 todo_dir 到 doing_dir"""
    # 檢查 doing_dir 中目前的任務數量
    doing_task_files = find_task_files(doing_dir, "[Publisher]")
    if doing_task_files == None:
        return
    if len(doing_task_files) >= subscriber_count:
        logger.debug(f"[Publisher] 所有 subscriber 都忙碌中，doing_dir 有 {len(doing_task_files)} 個任務檔案")
        return

    logger.info(f"[Publisher] 開始移動任務: {file_path.name}")
    try:
        # 移除檔案名稱中的 UUID（如果有的話）
        clean_name = remove_uuid(file_path.name)
        # 添加新的 UUID 以避免名稱衝突
        dest = doing_dir / add_uuid(Path(clean_name))
        if move_file_safely(file_path, dest, "[Publisher]"):
            logger.info(f"[Publisher] 移動任務成功: {dest.name}")
    except Exception as e:
        logger.error(f"[Publisher] 移動任務錯誤: {file_path.name}, {e}")

def publisher_worker(todo_dir: Path, doing_dir: Path, lock_dir: Path, subscriber_count: int, publisher_heartbeat_sec: float) -> None:
    """Publisher worker: 持續從 todo_dir 移動任務到 doing_dir"""
    while True:
        try:
            task_file_and_lock = get_oldest_task_file_lock(todo_dir, lock_dir, "[PublisherWorker]")
            if task_file_and_lock:
                task_file, lock = task_file_and_lock
                publisher(task_file, todo_dir, doing_dir, lock_dir, subscriber_count)
                release_lock(lock)
            else:
                logger.debug("[PublisherWorker] todo_dir 中沒有待執行的任務")
        except KeyboardInterrupt:
            logger.info("[PublisherWorker] 收到中斷訊號，正在關閉...")
            break
        except Exception as e:
            logger.error(f"[PublisherWorker] 發生錯誤: {e}")
            time.sleep(publisher_heartbeat_sec)

# ============================================================================
# Subscriber
# ============================================================================
def subscriber(file_path: Path, log_dir: Path, opencode_exe: str, doing_dir: Path, done_dir: Path, failed_dir: Path, monitor_timeout_sec: float, monitor_terminate_sec: float, monitor_heartbeat_sec: float) -> None:
    """執行單個任務，包含監控機制"""
    logger.info(f"[Subscriber] 開始執行任務: {file_path.name}")
    log_file_name = f"{file_path.name}.log"
    log_file = log_dir / log_file_name

    # 開啟日誌檔案以附加模式寫入，確保所有輸出都被記錄
    with open(log_file, "a", encoding="utf-8") as f:
        try:
            # 執行 OpenCode 命令來處理任務
            process = subprocess.Popen(
                [opencode_exe, "run", "Execute this task.", "--file", str(file_path)],
                cwd=doing_dir, stdout=f, stderr=f,
            )

            # 監控 log_file 更新時間的執行緒
            def monitor_log_file():
                """
                監控任務執行狀態的內部函數。

                這個函數會定期檢查日誌檔案的修改時間，
                如果超過設定的時間沒有更新，則認為任務停滯，
                會嘗試終止任務。
                """
                logger.info(f"[Monitor] 監測執行任務: {log_file_name}")
                last_modified_time = time.time()
                while process.poll() is None:  # 當程序還在執行時
                    try:
                        current_modified_time = os.path.getmtime(log_file)
                        if current_modified_time > last_modified_time:
                            # 日誌檔案有更新，更新最後修改時間
                            last_modified_time = current_modified_time
                        elif time.time() - last_modified_time > monitor_timeout_sec:  # 超過設定時間沒更新
                            logger.warning(f"[Monitor] 終止停滯任務: {file_path.name}")
                            process.terminate()
                            try:
                                # 等待程序正常終止
                                process.wait(timeout=monitor_terminate_sec)
                            except subprocess.TimeoutExpired:
                                # 如果等待超時，強制殺死程序
                                process.kill()
                            break
                    except (OSError, FileNotFoundError):
                        # 如果無法取得檔案修改時間，繼續監控
                        pass
                    time.sleep(monitor_heartbeat_sec)  # 每設定間隔檢查一次

            # 啟動監控執行緒
            monitor_thread = Thread(target=monitor_log_file, daemon=True)
            monitor_thread.start()

            # 等待程序完成
            process.wait()

            # 檢查程序退出碼
            if process.returncode == 0:
                # 任務成功執行，移動到完成目錄
                logger.info(f"[Subscriber] 執行任務成功: {file_path.name}")
                dest = done_dir / file_path.name
                move_file_safely(file_path, dest, "[Subscriber]")
            else:
                # 命令執行失敗，移動到失敗目錄
                logger.error(f"[Subscriber] 執行任務失敗: {file_path.name}, 退出碼: {process.returncode}")
                dest = failed_dir / file_path.name
                move_file_safely(file_path, dest, "[Subscriber]")

        except Exception as e:
            # 其他未預期的錯誤，移動到失敗目錄
            logger.error(f"[Subscriber] 執行任務錯誤: {file_path.name}, {e}")
            dest = failed_dir / file_path.name
            move_file_safely(file_path, dest, "[Subscriber]")

def subscriber_worker(doing_dir: Path, lock_dir: Path, log_dir: Path, opencode_exe: str, done_dir: Path, failed_dir: Path, subscriber_heartbeat_sec: float, monitor_timeout_sec: float, monitor_terminate_sec: float, monitor_heartbeat_sec: float) -> None:
    """Subscriber worker: 持續從 doing_dir 取得並執行任務"""
    while True:
        try:
            task_file_and_lock = get_oldest_task_file_lock(doing_dir, lock_dir, "[SubscriberWorker]")
            if task_file_and_lock:
                task_file, lock = task_file_and_lock
                subscriber(task_file, log_dir, opencode_exe, doing_dir, done_dir, failed_dir, monitor_timeout_sec, monitor_terminate_sec, monitor_heartbeat_sec)
                release_lock(lock)
            else:
                logger.debug("[SubscriberWorker] doing_dir 中沒有待執行的任務")
            time.sleep(subscriber_heartbeat_sec)
        except KeyboardInterrupt:
            logger.info("[SubscriberWorker] 收到中斷訊號，正在關閉...")
            break
        except Exception as e:
            logger.error(f"[SubscriberWorker] 發生錯誤: {e}")
            time.sleep(subscriber_heartbeat_sec)

# ============================================================================
# 主程式
# ============================================================================
def runner(config: Config) -> None:
    """主程式入口點：啟動任務處理系統"""
    logger.info("[Runner] 任務處理系統啟動")

    # 啟動多個 publisher worker 執行緒
    for i in range(config.publisher_count):
        t = Thread(
            target=publisher_worker,
            args=(
                config.todo_dir, config.doing_dir, config.lock_dir,
                config.subscriber_count, config.publisher_heartbeat_sec
            ),
            daemon=True,
            name=f"PublisherWorker{i}"
        )
        t.start()
        logger.info(f"[Runner] 啟動: {t.name}")

    # 啟動多個 subscriber worker 執行緒
    for i in range(config.subscriber_count):
        t = Thread(
            target=subscriber_worker,
            args=(
                config.doing_dir, config.lock_dir, config.log_dir,
                config.opencode_exe, config.done_dir, config.failed_dir,
                config.subscriber_heartbeat_sec,
                config.monitor_timeout_sec, config.monitor_terminate_sec, config.monitor_heartbeat_sec
            ),
            daemon=True,
            name=f"SubscriberWorker{i}"
        )
        t.start()
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
    """程式進入點：當此檔案被直接執行時啟動任務處理系統"""
    # 讀取命令列參數，如果沒有提供則使用預設配置檔案
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.ini"

    # 建立配置物件並啟動系統
    config = Config(config_path)
    runner(config)
