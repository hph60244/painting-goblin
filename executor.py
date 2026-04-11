"""
任務處理系統 - Executor

基於檔案系統的任務處理系統，包含 Publisher 和 Subscriber 兩種角色：
- Publisher: 從待處理目錄移動任務到處理中目錄
- Subscriber: 執行任務並根據結果移動到完成或失敗目錄

使用檔案鎖定機制確保任務不會被多個 worker 同時處理。
"""

import base64
import configparser
import logging
import os
import re
import shutil
import subprocess
import sys
import time
import uuid
from filelock import FileLock, Timeout
from pathlib import Path
from threading import Thread
from typing import Dict, List, Optional, Tuple

# ============================================================================
# 設定 logging (會在 Config.__init__ 中重新配置)
# ============================================================================
logger = logging.getLogger(__name__)

# ============================================================================
# 配置結構
# ============================================================================
class Config:
    """
    系統配置類，讀取和驗證配置文件

    負責從配置檔案讀取所有系統設定，包括目錄結構、執行參數和日誌配置。
    同時會驗證配置的完整性和正確性。
    """
    def __init__(self, config_path: str):
        """
        初始化配置物件

        Args:
            config_path: 配置檔案路徑

        Raises:
            ValueError: 當配置檔案缺少必要區段時
            FileNotFoundError: 當 OpenCode 執行檔不存在時
        """
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        # 驗證必要的區段
        required_sections = ["dir", "executor"]
        for section in required_sections:
            if not self.config.has_section(section):
                raise ValueError(f"Missing required section in {config_path}: [{section}]")

        # 讀取目錄相關設定
        self.root_dir = Path(self.config["dir"]["root_dir_path"])
        self.base_dir_name = self.config["dir"].get("base_dir_name", "tasks")
        self.todo_dir_name = self.config["dir"].get("todo_dir_name", "todo")
        self.doing_dir_name = self.config["dir"].get("doing_dir_name", "doing")
        self.done_dir_name = self.config["dir"].get("done_dir_name", "done")
        self.failed_dir_name = self.config["dir"].get("failed_dir_name", "failed")
        self.log_dir_name = self.config["dir"].get("log_dir_name", ".log")
        self.lock_dir_name = self.config["dir"].get("lock_dir_name", ".lock")

        # 讀取執行器相關設定
        self.executor_log_dir_name = self.config["executor"].get("log_dir_name", "logs")
        self.publisher_count = int(self.config["executor"].get("publisher_count", 1))
        self.publisher_heartbeat_sec = float(self.config["executor"].get("publisher_heartbeat_sec", 60))
        self.subscriber_count = int(self.config["executor"].get("subscriber_count", 1))
        self.subscriber_heartbeat_sec = float(self.config["executor"].get("subscriber_heartbeat_sec", 60))
        self.monitor_timeout_sec = float(self.config["executor"].get("monitor_timeout_sec", 60))
        self.monitor_terminate_sec = float(self.config["executor"].get("monitor_terminate_sec", 5))
        self.monitor_heartbeat_sec = float(self.config["executor"].get("monitor_heartbeat_sec", 5))
        self.opencode_exe_path = self.config["executor"]["opencode_exe_path"]

        # 驗證 OpenCode 執行檔是否存在
        if not Path(self.opencode_exe_path).exists():
            raise FileNotFoundError(f"OpenCode executable not found: {self.opencode_exe_path}")

        # 計算完整的目錄路徑
        self.base_dir = self.root_dir / self.base_dir_name
        self.todo_dir = self.base_dir / self.todo_dir_name
        self.doing_dir = self.base_dir / self.doing_dir_name
        self.done_dir = self.base_dir / self.done_dir_name
        self.failed_dir = self.base_dir / self.failed_dir_name
        self.log_dir = self.base_dir / self.log_dir_name
        self.lock_dir = self.base_dir / self.lock_dir_name
        self.executor_log_dir = self.root_dir / self.executor_log_dir_name

        # 確保所有必要的資料夾都存在
        for d in [self.todo_dir, self.doing_dir, self.done_dir, self.failed_dir, self.log_dir, self.lock_dir, self.executor_log_dir]:
            d.mkdir(parents=True, exist_ok=True)

        # 設置 logging 配置
        # 清除現有的 handlers 以避免重複
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        # 配置 root logger
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)-5s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.StreamHandler(),  # 輸出到控制台
                logging.FileHandler(self.executor_log_dir / "executor.log", encoding="utf-8")  # 輸出到檔案
            ],
            force=True  # 強制重新配置，即使已經有 handlers
        )

        # 重新獲取 logger 以確保使用新的配置
        global logger
        logger = logging.getLogger(__name__)

# ============================================================================
# 工具函數
# ============================================================================

# 任務檔案副檔名設定（只處理 .md 檔案）
TASK_FILE_EXTENSION: str = ".md"

# UUID 模式正則表達式（用於識別和移除檔案名稱中的 UUID）
UUID_PATTERN = re.compile(r"\.[A-Za-z0-9_-]{22}$")

def parse_underscore_params(filename: str) -> List[Tuple[str, str]]:
    """
    解析檔案名稱中的 _XXX-YYY 格式參數

    從檔案名稱中提取所有 _參數名-參數值 格式的參數對。
    例如：檔案名 "task_priority-high_difficulty-medium.md" 會解析出
    [("priority", "high"), ("difficulty", "medium")]

    Args:
        filename: 檔案名稱（包含或不包含副檔名）

    Returns:
        參數對列表，每個元素為 (參數名, 參數值)
    """
    # 移除副檔名
    name_without_ext = filename.rsplit('.', 1)[0]

    # 尋找所有 _XXX-YYY 模式
    # 匹配格式：_後跟字母數字字符序列，然後是-，然後是字母數字字符序列
    # 使用 \w+ 匹配字母、數字和下劃線（包括 Unicode 字符）
    pattern = r'_(\w+)-(\w+)'
    matches = re.findall(pattern, name_without_ext)

    # 轉換為參數對列表
    result: List[Tuple[str, str]] = []
    for key, value in matches:
        result.append((key, value))

    return result

def try_lock(lock_file: str) -> Optional[FileLock]:
    """
    非阻塞方式嘗試取得檔案鎖

    嘗試取得檔案鎖，如果檔案已被鎖定則立即返回 None。

    Args:
        lock_file: 鎖定檔案路徑

    Returns:
        成功時返回 FileLock 物件，失敗時返回 None
    """
    lock = FileLock(lock_file)
    try:
        lock.acquire(timeout=0)  # timeout=0 表示非阻塞模式
        return lock
    except Timeout:
        return None

def release_lock(lock: FileLock) -> None:
    """
    釋放檔案鎖

    如果鎖定物件處於鎖定狀態，則釋放鎖定。

    Args:
        lock: 要釋放的 FileLock 物件
    """
    if lock.is_locked:
        lock.release()

def build_lock_file_path(task_file: Path, lock_dir: Path) -> Path:
    """
    根據任務檔案路徑生成對應的鎖定檔案路徑

    Args:
        task_file: 任務檔案路徑
        lock_dir: 鎖定檔案目錄

    Returns:
        鎖定檔案完整路徑
    """
    return lock_dir / f"{task_file.name}.lock"

def find_task_files(folder: Path, log_prefix: str) -> Optional[List[Path]]:
    """
    在指定資料夾中尋找任務檔案

    掃描指定資料夾，找出所有副檔名為 .md 的檔案。

    Args:
        folder: 要搜尋的資料夾路徑
        log_prefix: 日誌前綴（用於錯誤訊息）

    Returns:
        任務檔案路徑列表，發生錯誤時返回 None
    """
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
    """
    取得資料夾中最舊的未鎖定任務檔案

    掃描資料夾中的任務檔案，按修改時間排序，嘗試鎖定最舊的檔案。

    Args:
        folder: 要搜尋的資料夾路徑
        lock_dir: 鎖定檔案目錄
        log_prefix: 日誌前綴（用於錯誤訊息）

    Returns:
        成功時返回 (任務檔案路徑, 鎖定物件)，失敗時返回 None
    """
    try:
        task_files = find_task_files(folder, log_prefix)

        if not task_files:
            logger.debug(f"{log_prefix} 資料夾 {folder} 中找不到任務檔案")
            return None

        # 根據修改時間排序（最舊的優先）
        sorted_task_files = sorted(task_files, key=lambda p: p.stat().st_mtime)

        # 嘗試鎖定最舊的檔案
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
    """
    生成簡短的 UUID 字串（22個字元）

    使用 UUID v4 生成隨機 UUID，並使用 base64 URL-safe 編碼縮短為 22 字元。

    Returns:
        22 字元的簡短 UUID 字串
    """
    u = uuid.uuid4()
    return base64.urlsafe_b64encode(u.bytes).rstrip(b'=').decode('ascii')

def remove_uuid(file_name: str) -> str:
    """
    移除檔案名稱中的 UUID

    從檔案名稱中移除 .{22字元UUID} 的部分。

    Args:
        file_name: 原始檔案名稱

    Returns:
        移除 UUID 後的檔案名稱
    """
    name, ext = os.path.splitext(file_name)
    new_name = re.sub(UUID_PATTERN, "", name) + ext
    return new_name

def add_uuid(file_path: Path) -> str:
    """
    為檔案名稱添加 UUID 以避免名稱衝突

    在檔案名稱的基礎名稱和副檔名之間插入 .{22字元UUID}。

    Args:
        file_path: 原始檔案路徑

    Returns:
        添加 UUID 後的檔案名稱
    """
    short_id = generate_short_uuid()
    return f"{file_path.stem}.{short_id}{file_path.suffix}"

def move_file_safely(src: Path, dest: Path, log_prefix: str) -> bool:
    """
    安全地移動檔案，包含錯誤處理和日誌記錄

    嘗試移動檔案，並記錄成功或失敗的詳細資訊。

    Args:
        src: 來源檔案路徑
        dest: 目標檔案路徑
        log_prefix: 日誌前綴（用於識別移動操作的來源）

    Returns:
        移動成功返回 True，失敗返回 False
    """
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
    """
    移動單個任務從 todo_dir 到 doing_dir

    檢查目前處理中的任務數量，如果未超過 subscriber 數量限制，
    則將任務從待處理目錄移動到處理中目錄。

    Args:
        file_path: 要移動的任務檔案路徑
        todo_dir: 待處理目錄
        doing_dir: 處理中目錄
        lock_dir: 鎖定檔案目錄
        subscriber_count: subscriber 數量限制
    """
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
    """
    Publisher worker: 持續從 todo_dir 移動任務到 doing_dir

    持續監控待處理目錄，將最舊的未鎖定任務移動到處理中目錄。
    使用心跳機制控制檢查頻率。

    Args:
        todo_dir: 待處理目錄
        doing_dir: 處理中目錄
        lock_dir: 鎖定檔案目錄
        subscriber_count: subscriber 數量限制
        publisher_heartbeat_sec: 心跳間隔（秒）
    """
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
def subscriber(file_path: Path, root_dir: Path, log_dir: Path, opencode_exe_path: str, doing_dir: Path, done_dir: Path, failed_dir: Path, monitor_timeout_sec: float, monitor_terminate_sec: float, monitor_heartbeat_sec: float) -> None:
    """
    執行單個任務，包含監控機制

    執行任務檔案，使用 OpenCode 處理任務，並監控執行狀態。
    如果任務執行成功，移動到完成目錄；如果失敗，移動到失敗目錄。

    Args:
        file_path: 任務檔案路徑
        root_dir: 根目錄路徑
        log_dir: 日誌目錄路徑
        opencode_exe_path: OpenCode 執行檔路徑
        doing_dir: 處理中目錄
        done_dir: 完成目錄
        failed_dir: 失敗目錄
        monitor_timeout_sec: 監控超時時間（秒）
        monitor_terminate_sec: 終止等待時間（秒）
        monitor_heartbeat_sec: 監控心跳間隔（秒）
    """
    logger.info(f"[Subscriber] 開始執行任務: {file_path.name}")

    log_file_name = f"{file_path.name}.log"
    log_file = log_dir / log_file_name

    # 開啟日誌檔案以附加模式寫入，確保所有輸出都被記錄
    with open(log_file, "a", encoding="utf-8") as f:
        try:
            # 解析檔案名稱中的參數
            params = parse_underscore_params(file_path.name)
            params = list(map(lambda x: f"{x[0]}={x[1]}", params))
            message = "\n".join(["Give:", *params, f"PAINTING_GOBLIN_DIR={root_dir}", "Execute this task"])

            # 執行 OpenCode 命令來處理任務
            process = subprocess.Popen(
                [opencode_exe_path, "run", message, "--file", str(file_path)],
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

def subscriber_worker(doing_dir: Path, root_dir: Path, lock_dir: Path, log_dir: Path, opencode_exe_path: str, done_dir: Path, failed_dir: Path, subscriber_heartbeat_sec: float, monitor_timeout_sec: float, monitor_terminate_sec: float, monitor_heartbeat_sec: float) -> None:
    """
    Subscriber worker: 持續從 doing_dir 取得並執行任務

    持續監控處理中目錄，取得最舊的未鎖定任務並執行。
    使用心跳機制控制檢查頻率。

    Args:
        doing_dir: 處理中目錄
        root_dir: 根目錄路徑
        lock_dir: 鎖定檔案目錄
        log_dir: 日誌目錄路徑
        opencode_exe_path: OpenCode 執行檔路徑
        done_dir: 完成目錄
        failed_dir: 失敗目錄
        subscriber_heartbeat_sec: 心跳間隔（秒）
        monitor_timeout_sec: 監控超時時間（秒）
        monitor_terminate_sec: 終止等待時間（秒）
        monitor_heartbeat_sec: 監控心跳間隔（秒）
    """
    while True:
        try:
            task_file_and_lock = get_oldest_task_file_lock(doing_dir, lock_dir, "[SubscriberWorker]")
            if task_file_and_lock:
                task_file, lock = task_file_and_lock
                subscriber(task_file, root_dir, log_dir, opencode_exe_path, doing_dir, done_dir, failed_dir, monitor_timeout_sec, monitor_terminate_sec, monitor_heartbeat_sec)
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
def executor(config: Config) -> None:
    """
    主程式入口點：啟動任務處理系統

    根據配置啟動指定數量的 publisher 和 subscriber worker 執行緒，
    並管理系統的生命週期。

    Args:
        config: 系統配置物件
    """
    logger.info("[Executor] 任務處理系統啟動")

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
        logger.info(f"[Executor] 啟動: {t.name}")

    # 啟動多個 subscriber worker 執行緒
    for i in range(config.subscriber_count):
        t = Thread(
            target=subscriber_worker,
            args=(
                config.doing_dir, config.root_dir, config.lock_dir, config.log_dir,
                config.opencode_exe_path, config.done_dir, config.failed_dir,
                config.subscriber_heartbeat_sec,
                config.monitor_timeout_sec, config.monitor_terminate_sec, config.monitor_heartbeat_sec
            ),
            daemon=True,
            name=f"SubscriberWorker{i}"
        )
        t.start()
        logger.info(f"[Executor] 啟動: {t.name}")

    logger.info("[Executor] 系統已啟動，按 Ctrl+C 結束")

    try:
        # 主執行緒持續執行，等待中斷訊號
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("[Executor] 收到中斷訊號，正在關閉...")
    except Exception as e:
        logger.error(f"[Executor] 主程式發生未預期錯誤: {e}")
    finally:
        logger.info("[Executor] 任務處理系統關閉完成")


if __name__ == "__main__":
    """
    程式進入點：當此檔案被直接執行時啟動任務處理系統

    讀取命令列參數或使用預設配置檔案，建立配置物件並啟動系統。
    """
    # 讀取命令列參數，如果沒有提供則使用預設配置檔案
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.ini"

    # 建立配置物件並啟動系統
    config = Config(config_path)
    executor(config)
