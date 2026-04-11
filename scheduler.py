"""
任務排程系統 - 根據 config.ini 中的 cron 設定，
定期將 job 資料夾中的任務檔案複製到 todo 資料夾。
"""

import os
import sys
import shutil
import logging
from pathlib import Path
import configparser
from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass

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
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        # 驗證必要的區段
        required_sections = ["dir", "scheduler"]
        for section in required_sections:
            if not self.config.has_section(section):
                raise ValueError(f"Missing required section in {config_path}: [{section}]")

        # 讀取 dir 設定
        self.root_dir = Path(self.config["dir"]["root_dir_path"])
        self.base_dir_name = self.config["dir"].get("base_dir_name", "tasks")
        self.todo_dir_name = self.config["dir"].get("todo_dir_name", "todo")

        # 讀取 scheduler 設定
        self.scheduler_log_dir_name = self.config["scheduler"].get("log_dir_name", "logs")
        self.scheduler_job_dir_name = self.config["scheduler"].get("job_dir_name", "jobs")
        self.scheduler_timezone = self.config["scheduler"].get("timezone", "Asia/Taipei")

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
        self.base_dir = self.root_dir / self.base_dir_name
        self.todo_dir = self.base_dir / self.todo_dir_name
        self.scheduler_log_dir = self.root_dir / self.scheduler_log_dir_name

        # job 資料夾路徑（相對於專案根目錄）
        self.scheduler_job_dir = self.root_dir / self.scheduler_job_dir_name

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
            import time
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
