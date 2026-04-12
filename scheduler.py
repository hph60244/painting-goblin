"""
任務排程系統 - 根據 config.ini 中的 cron 設定，
定期將 job 資料夾中的任務檔案複製到 todo 資料夾。
"""

import configparser
import logging
import os
import shutil
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, List, Tuple

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

# ============================================================================
# 設定 logging (會在 Config.__init__ 中重新配置)
# ============================================================================
logger = logging.getLogger(__name__)

# ============================================================================
# 資料類別定義
# ============================================================================
@dataclass
class JobSetting:
    """任務設定資料類別

    儲存從配置檔案讀取的任務設定資訊。

    Attributes:
        name: 任務名稱（配置檔案中 section name 的後半部分）
        schedule: cron 排程表達式
        params: 其他參數列表，每個元素為 (參數名稱, 參數值列表)
    """
    name: str
    schedule: str
    params: List[Tuple[str, List[str]]]

# ============================================================================
# 配置結構
# ============================================================================
class Config:
    """
    配置類，儲存所有排程系統設定值

    這個類別負責讀取和驗證配置文件，並提供所有必要的配置參數給排程系統使用。
    """
    def __init__(self, config_path: str):
        """
        初始化配置物件

        Args:
            config_path: 配置檔案路徑

        Raises:
            ValueError: 如果配置檔案缺少必要的區段
        """
        global logger
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        # 驗證必要的區段
        required_sections = ["scheduler"]
        for section in required_sections:
            if not self.config.has_section(section):
                raise ValueError(f"Missing required section in {config_path}: [{section}]")

        # 讀取 scheduler 設定
        self.root_dir = Path(self.config["scheduler"]["root_dir_path"])
        self.job_dir_path = Path(self.config["scheduler"]["job_dir_path"])
        self.scheduler_timezone = self.config["scheduler"].get("timezone", "Asia/Taipei")
        self.cleaner_schedule = self.config["scheduler"].get("cleaner_schedule", "0 0 * * *")
        self.cleaner_log_max_day = int(self.config["scheduler"].get("cleaner_log_max_day", "7"))

        # 讀取 job 設定
        self.job_settings: List[JobSetting] = []

        # 讀取所有 job: 開頭的 section（任務設定）
        for section_name in self.config.sections():
            if section_name.startswith("job:"):
                # 取得任務名稱（移除 "job:" 前綴）
                job_name = section_name[4:]

                # 讀取排程設定
                if self.config.has_option(section_name, "schedule"):
                    schedule = self.config[section_name]["schedule"].strip()

                    # 讀取其他任意欄位，值用逗號分隔表示列表
                    params: List[Tuple[str, List[str]]] = []
                    for key in self.config[section_name]:
                        if key != "schedule":
                            value_str = self.config[section_name][key].strip()
                            values = [v.strip() for v in value_str.split(",") if v.strip()]
                            params.append((key, values))

                    # 建立任務設定物件
                    # 注意：configparser 在 Python 3.7+ 會保持插入順序
                    job_setting = JobSetting(name=job_name, schedule=schedule, params=params)
                    self.job_settings.append(job_setting)
                else:
                    logger.warning(f"[Scheduler] 任務區段 '{section_name}' 缺少 schedule 設定，將跳過此任務")

        # 計算目錄路徑
        self.base_dir = self.root_dir / "tasks"
        self.todo_dir = self.base_dir / "todo"
        self.scheduler_log_dir = self.root_dir / "logs"  # 寫死的值
        self.scheduler_job_dir = self.job_dir_path  # 從配置檔案讀取

        # 確保所有必要的資料夾都存在
        for d in [self.todo_dir, self.scheduler_log_dir]:
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
                logging.FileHandler(self.scheduler_log_dir / "scheduler.log", encoding="utf-8")
            ],
            force=True  # 強制重新配置，即使已經有 handlers
        )

        # 重新獲取 logger 以確保使用新的配置
        logger = logging.getLogger(__name__)

        logger.info(f"[Scheduler] 配置載入完成，時區: {self.scheduler_timezone}")
        logger.info(f"[Scheduler] 找到 {len(self.job_settings)} 個排程任務")
        for job_setting in self.job_settings:
            logger.info(f"  - {job_setting.name}: {job_setting.schedule}")
            if job_setting.params:
                for key, values in job_setting.params:
                    logger.info(f"    * {key}: {', '.join(values)}")

# ============================================================================
# 工具函數
# ============================================================================
def generate_param_combinations(params: List[Tuple[str, List[str]]]) -> List[str]:
    """
    生成參數排列組合

    Args:
        params: 參數列表，每個元素是 (參數名稱, 參數值列表)

    Returns:
        排列組合字串列表，格式為 "_參數1-值1_參數2-值2"
    """
    if not params:
        return [""]

    # 提取所有參數的名稱和值列表
    param_names = [name for name, _ in params]
    value_lists = [values for _, values in params]

    # 使用遞迴生成所有組合
    def generate_combinations(index: int, current: List[str]) -> List[List[str]]:
        if index == len(value_lists):
            return [current.copy()]

        combinations = []
        param_name = param_names[index]
        for value in value_lists[index]:
            # 格式為 "參數名稱-值"
            current.append(f"_{param_name}-{value}")
            combinations.extend(generate_combinations(index + 1, current))
            current.pop()

        return combinations

    # 生成所有組合並轉換為字串
    all_combinations = generate_combinations(0, [])
    return ["".join(combo) for combo in all_combinations]

def copy_task_to_todo(task_name: str, config: Config, params: List[Tuple[str, List[str]]] = None) -> bool:
    """
    將任務檔案從 job 複製到 todo 資料夾

    如果 params 不為空，則為每個參數組合創建一個檔案副本，
    檔案名稱格式為: taskname_參數1-值1_參數2-值2.md

    先嘗試複製檔案，如果複製失敗，則檢查目標檔案是否存在，
    如果存在則視為成功（同名檔案已存在於目標位置）。

    Args:
        task_name: 任務名稱（不含 .md 副檔名）
        config: 配置物件
        params: 參數列表，每個元素是 (參數名稱, 參數值列表)

    Returns:
        bool: 複製是否成功（已有檔案存在於目標位置也視為成功）
    """
    try:
        # 檢查來源檔案是否存在
        source_file = config.scheduler_job_dir / f"{task_name}.md"
        if not source_file.exists():
            logger.error(f"[Scheduler] 任務檔案不存在: {source_file}")
            return False

        # 生成參數組合
        if params is None:
            params = []

        param_suffixes = generate_param_combinations(params)

        success = True
        copied_count = 0

        for suffix in param_suffixes:
            # 構建目標檔案名稱
            dest_filename = f"{task_name}{suffix}.md"
            dest_file = config.todo_dir / dest_filename

            # 嘗試複製檔案
            try:
                shutil.copy2(source_file, dest_file)
                logger.debug(f"[Scheduler] 成功複製任務檔案: {dest_filename}")
                copied_count += 1
            except Exception as e:
                # 複製失敗，檢查目標檔案是否已存在
                if dest_file.exists():
                    logger.debug(f"[Scheduler] 複製失敗但目標檔案已存在，視為成功: {dest_filename}")
                    # 檔案已存在，視為成功
                    copied_count += 1
                else:
                    logger.error(f"[Scheduler] 複製任務檔案時發生錯誤: {e}")
                    success = False

        if copied_count > 0:
            logger.info(f"[Scheduler] 總共處理了 {copied_count} 個檔案變體")

        return success

    except Exception as e:
        logger.error(f"[Scheduler] 複製任務檔案時發生錯誤: {e}")
        return False

def create_job_function(job_setting: JobSetting, config: Config):
    """建立 APScheduler 的任務函數

    這個函數會建立一個閉包函數，該函數會在排程觸發時執行。

    Args:
        job_setting: 任務設定物件
        config: 配置物件

    Returns:
        一個可執行的任務函數，會在執行時複製對應的任務檔案
    """
    def job_function():
        """實際執行的任務函數（閉包）"""
        task_name = job_setting.name
        params = job_setting.params
        logger.info(f"[Job] 執行排程任務: {task_name}")
        if copy_task_to_todo(task_name, config, params):
            logger.info(f"[Job] 任務 {task_name} 執行成功")
        else:
            logger.error(f"[Job] 任務 {task_name} 執行失敗")

    return job_function


def clean_task_dirs(base_dir: Path) -> int:
    """清理任務目錄中的非 .md 檔案

    清理以下目錄：
    1. todo_dir 裡面不是 .md 的檔案
    2. doing_dir 裡面不是 .md 的檔案
    3. done_dir 裡面不是 .md 的檔案
    4. failed_dir 裡面不是 .md 的檔案

    Args:
        base_dir: 基礎目錄路徑

    Returns:
        刪除的檔案數量
    """
    todo_dir = base_dir / "todo"
    doing_dir = base_dir / "doing"
    done_dir = base_dir / "done"
    failed_dir = base_dir / "failed"

    task_dirs = [
        (todo_dir, "todo"),
        (doing_dir, "doing"),
        (done_dir, "done"),
        (failed_dir, "failed")
    ]

    total_deleted = 0

    for dir_path, dir_name in task_dirs:
        # 確保目錄存在
        dir_path.mkdir(parents=True, exist_ok=True)

        deleted_count = 0
        for file_path in dir_path.iterdir():
            if file_path.is_file() and not file_path.name.endswith('.md'):
                try:
                    file_path.unlink()
                    logger.debug(f"[Cleaner] 刪除 {dir_name} 目錄中的非 .md 檔案: {file_path.name}")
                    deleted_count += 1
                except Exception as e:
                    logger.error(f"[Cleaner] 刪除檔案失敗 {file_path}: {e}")

        if deleted_count > 0:
            logger.info(f"[Cleaner] 在 {dir_name} 目錄中刪除了 {deleted_count} 個非 .md 檔案")
            total_deleted += deleted_count

    return total_deleted


def clean_log_dir(base_dir: Path, max_days: int) -> int:
    """清理 log 目錄

    執行以下清理：
    1. 刪除非 .md.log 的檔案
    2. 刪除超過指定天數的 .md.log 檔案

    Args:
        base_dir: 基礎目錄路徑
        max_days: 保留 log 的最大天數

    Returns:
        刪除的檔案數量
    """

    log_dir = base_dir / ".log"

    # 確保目錄存在
    log_dir.mkdir(parents=True, exist_ok=True)

    deleted_log_count = 0
    deleted_old_log_count = 0

    # 計算日期閾值
    cutoff_date = datetime.now() - timedelta(days=max_days)

    for file_path in log_dir.iterdir():
        if file_path.is_file():
            # 1. 刪除非 .md.log 檔案
            if not file_path.name.endswith('.md.log'):
                try:
                    file_path.unlink()
                    logger.debug(f"[Cleaner] 刪除非 .md.log 檔案: {file_path.name}")
                    deleted_log_count += 1
                except Exception as e:
                    logger.error(f"[Cleaner] 刪除檔案失敗 {file_path}: {e}")
            # 2. 刪除超過天數的 .md.log 檔案
            elif file_path.name.endswith('.md.log'):
                try:
                    # 獲取檔案修改時間
                    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if mtime < cutoff_date:
                        file_path.unlink()
                        logger.debug(f"[Cleaner] 刪除超過 {max_days} 天的 log 檔案: {file_path.name}")
                        deleted_old_log_count += 1
                except Exception as e:
                    logger.error(f"[Cleaner] 檢查/刪除 log 檔案失敗 {file_path}: {e}")

    if deleted_log_count > 0:
        logger.info(f"[Cleaner] 刪除了 {deleted_log_count} 個非 .md.log 檔案")

    if deleted_old_log_count > 0:
        logger.info(f"[Cleaner] 刪除了 {deleted_old_log_count} 個超過 {max_days} 天的 log 檔案")

    return deleted_log_count + deleted_old_log_count


def clean_lock_dir(base_dir: Path) -> int:
    """清理 lock 目錄中沒上鎖的檔案

    Args:
        base_dir: 基礎目錄路徑

    Returns:
        刪除的檔案數量
    """
    lock_dir = base_dir / ".lock"

    # 確保目錄存在
    lock_dir.mkdir(parents=True, exist_ok=True)

    deleted_lock_count = 0

    for file_path in lock_dir.iterdir():
        if file_path.is_file():
            try:
                # 檢查檔案是否被鎖定（嘗試打開檔案）
                # 在 Windows 上，如果檔案被鎖定，打開會失敗
                try:
                    # 嘗試以讀取模式打開檔案
                    with open(file_path, 'r') as f:
                        # 如果能打開，表示檔案沒被鎖定
                        f.read(1)  # 讀取一個字元
                        # 檔案沒被鎖定，刪除它
                        file_path.unlink()
                        logger.debug(f"[Cleaner] 刪除未鎖定的 lock 檔案: {file_path.name}")
                        deleted_lock_count += 1
                except (IOError, OSError):
                    # 檔案被鎖定或其他錯誤，跳過
                    pass
            except Exception as e:
                logger.error(f"[Cleaner] 檢查 lock 檔案失敗 {file_path}: {e}")

    if deleted_lock_count > 0:
        logger.info(f"[Cleaner] 刪除了 {deleted_lock_count} 個未鎖定的 lock 檔案")

    return deleted_lock_count


def run_cleaner_job(config: Config):
    """執行清理任務

    根據配置執行以下清理工作：
    1. 清除 todo_dir 裡面不是 .md 的檔案
    2. 清除 doing_dir 裡面不是 .md 的檔案
    3. 清除 done_dir 裡面不是 .md 的檔案
    4. 清除 failed_dir 裡面不是 .md 的檔案
    5. 清除 log_dir 裡面不是 .md.log 的檔案
    6. 清除 log_dir 裡面超過 cleaner_log_max_day 的 log
    7. 清除 lock_dir 裡面沒上鎖的檔案
    """
    logger.info("[Cleaner] 開始執行清理任務")

    total_deleted = 0

    # 1-4: 清理任務目錄中的非 .md 檔案
    deleted_task_files = clean_task_dirs(config.base_dir)
    total_deleted += deleted_task_files

    # 5-6: 清理 log 目錄
    deleted_log_files = clean_log_dir(config.base_dir, config.cleaner_log_max_day)
    total_deleted += deleted_log_files

    # 7: 清理 lock 目錄中沒上鎖的檔案
    deleted_lock_files = clean_lock_dir(config.base_dir)
    total_deleted += deleted_lock_files

    logger.info(f"[Cleaner] 清理任務完成，總共刪除了 {total_deleted} 個檔案")

# ============================================================================
# 排程器設定
# ============================================================================
def setup_scheduler(config: Config) -> Optional[BackgroundScheduler]:
    """
    設定 APScheduler

    Args:
        config: 配置物件

    Returns:
        BackgroundScheduler: 設定好的排程器，如果設定失敗則返回 None
    """
    if not config.job_settings:
        logger.warning("[Scheduler] 沒有找到任何排程任務，排程器將不會啟動")
        return None

    try:
        # 建立排程器
        scheduler = BackgroundScheduler(timezone=config.scheduler_timezone)

        # 為每個 job 設定 cron 觸發器
        for job_setting in config.job_settings:
            try:
                task_name = job_setting.name
                cron_expr = job_setting.schedule

                # 解析 cron 表達式（格式: "分 時 日 月 星期"）
                parts = cron_expr.split()
                if len(parts) != 5:
                    logger.error(f"[Scheduler] 無效的 cron 表達式: {cron_expr}")
                    continue

                minute, hour, day, month, day_of_week = parts

                # 建立 cron 觸發器
                trigger = CronTrigger(
                    minute=minute, hour=hour, day=day,
                    month=month, day_of_week=day_of_week,
                    timezone=config.scheduler_timezone
                )

                # 添加任務到排程器
                scheduler.add_job(
                    create_job_function(job_setting, config),
                    trigger=trigger,
                    id=f"job_{task_name}",
                    name=f"Task: {task_name}",
                    replace_existing=True  # 如果已存在相同 ID 的任務，則替換
                )

                logger.info(f"[Scheduler] 已設定排程任務: {task_name} ({cron_expr})")

            except ValueError as e:
                logger.error(f"[Scheduler] 設定任務 {task_name} 時發生錯誤: {e}")
            except Exception as e:
                logger.error(f"[Scheduler] 設定任務 {task_name} 時發生未預期錯誤: {e}")

        # 添加 cleaner job（如果設定了 cleaner_schedule）
        if hasattr(config, 'cleaner_schedule') and config.cleaner_schedule:
            try:
                # 解析 cleaner cron 表達式
                parts = config.cleaner_schedule.split()
                if len(parts) == 5:
                    minute, hour, day, month, day_of_week = parts

                    # 建立 cron 觸發器
                    trigger = CronTrigger(
                        minute=minute, hour=hour, day=day,
                        month=month, day_of_week=day_of_week,
                        timezone=config.scheduler_timezone
                    )

                    # 添加 cleaner 任務到排程器
                    scheduler.add_job(
                        lambda: run_cleaner_job(config),
                        trigger=trigger,
                        id="cleaner_job",
                        name="Cleaner: 系統清理任務",
                        replace_existing=True
                    )

                    logger.info(f"[Scheduler] 已設定清理任務: {config.cleaner_schedule}")
                else:
                    logger.warning(f"[Scheduler] 無效的 cleaner cron 表達式: {config.cleaner_schedule}")
            except Exception as e:
                logger.error(f"[Scheduler] 設定清理任務時發生錯誤: {e}")

        return scheduler

    except Exception as e:
        logger.error(f"[Scheduler] 設定排程器時發生錯誤: {e}")
        return None

# ============================================================================
# 主程式
# ============================================================================
def scheduler_main(config: Config) -> None:
    """
    主程式入口點：啟動任務排程系統

    Args:
        config: 配置物件
    """
    logger.info("[Scheduler] 任務排程系統啟動")

    # 設定排程器
    scheduler = setup_scheduler(config)

    if scheduler is None:
        logger.info("[Scheduler] 排程器未啟動，系統結束")
        return

    try:
        # 啟動排程器
        scheduler.start()
        logger.info("[Scheduler] 排程器已啟動")

        # 列出所有已設定的 jobs
        jobs = scheduler.get_jobs()
        logger.info(f"[Scheduler] 已設定 {len(jobs)} 個排程任務:")
        for job in jobs:
            next_run = job.next_run_time
            next_run_str = next_run.strftime("%Y-%m-%d %H:%M:%S") if next_run else "N/A"
            logger.info(f"  - {job.name} (ID: {job.id}), 下次執行: {next_run_str}")

        logger.info("[Scheduler] 系統已啟動，按 Ctrl+C 結束")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("[Scheduler] 收到中斷訊號，正在關閉...")

    except Exception as e:
        logger.error(f"[Scheduler] 主程式發生錯誤: {e}")
    finally:
        if scheduler and scheduler.running:
            scheduler.shutdown(wait=True)
            logger.info("[Scheduler] 排程器已關閉")

        logger.info("[Scheduler] 任務排程系統關閉完成")

if __name__ == "__main__":
    """
    程式進入點：當此檔案被直接執行時啟動任務排程系統

    使用方式：
        python scheduler.py [config_file_path]

    參數：
        config_file_path: 可選的配置檔案路徑，預設為 "config.ini"
    """
    # 讀取命令列參數，如果沒有提供則使用預設配置檔案
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.ini"

    # 建立配置物件並啟動系統
    config = Config(config_path)
    scheduler_main(config)
