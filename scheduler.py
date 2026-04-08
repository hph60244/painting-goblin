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
from typing import Dict, Optional

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

# ============================================================================
# 設定 logging (會在 Config.__init__ 中重新配置)
# ============================================================================
logger = logging.getLogger(__name__)

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
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        # 驗證必要的區段
        required_sections = ["task", "scheduler", "job"]
        for section in required_sections:
            if not self.config.has_section(section):
                raise ValueError(f"Missing required section in {config_path}: [{section}]")

        # 讀取 task 設定
        self.base_dir_name = self.config["task"].get("base_dir_name", "task")
        self.todo_dir_name = self.config["task"].get("todo_dir_name", "todo")
        self.timezone = self.config["task"].get("timezone", "Asia/Taipei")

        # 讀取 scheduler 設定
        self.scheduler_log_dir_name = self.config["scheduler"].get("log_dir_name", "log")
        self.scheduler_job_dir_name = self.config["scheduler"].get("job_dir_name", "job")

        # 讀取 job 設定
        self.jobs: Dict[str, str] = {}
        if self.config.has_section("job"):
            for key, value in self.config["job"].items():
                self.jobs[key] = value.strip()

        # 計算目錄路徑
        root_dir = Path(os.getenv("PAINTING_GOBLIN_DIR"))
        self.base_dir = root_dir / self.base_dir_name
        self.todo_dir = self.base_dir / self.todo_dir_name
        self.scheduler_log_dir = root_dir / self.scheduler_log_dir_name

        # job 資料夾路徑（相對於專案根目錄）
        self.scheduler_job_dir = root_dir / self.scheduler_job_dir_name

        # 確保所有必要的資料夾都存在
        for d in [self.todo_dir, self.scheduler_log_dir]:
            d.mkdir(parents=True, exist_ok=True)

        # 設置 logging
        # 清除現有的 handlers
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        # 配置 root logger
        log_file_path = self.scheduler_log_dir / "scheduler.log"
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)-5s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(log_file_path, encoding="utf-8")
            ],
            force=True  # 強制重新配置，即使已經有 handlers
        )

        # 重新獲取 logger 以確保使用新的配置
        global logger
        logger = logging.getLogger(__name__)

        logger.info(f"配置載入完成，時區: {self.timezone}")
        logger.info(f"找到 {len(self.jobs)} 個排程任務")
        for job_name, cron_expr in self.jobs.items():
            logger.info(f"  - {job_name}: {cron_expr}")

# ============================================================================
# 工具函數
# ============================================================================
def copy_task_to_todo(task_name: str, config: Config) -> bool:
    """
    將任務檔案從 job 複製到 todo 資料夾

    遇到同名檔案時跳過複製，返回 True（不算失敗）

    Args:
        task_name: 任務名稱（不含 .md 副檔名）
        config: 配置物件

    Returns:
        bool: 複製是否成功（遇到同名檔案跳過不算失敗）
    """
    try:
        # 檢查來源檔案是否存在
        source_file = config.scheduler_job_dir / f"{task_name}.md"
        if not source_file.exists():
            logger.error(f"任務檔案不存在: {source_file}")
            return False

        # 檢查目標檔案是否已存在
        dest_file = config.todo_dir / f"{task_name}.md"
        if dest_file.exists():
            logger.debug(f"目標檔案已存在，跳過複製: {task_name}.md")
            return True

        # 複製檔案
        shutil.copy2(source_file, dest_file)
        logger.info(f"成功複製任務檔案: {task_name}.md")
        return True

    except (FileNotFoundError, PermissionError) as e:
        logger.error(f"檔案操作錯誤: {e}")
        return False
    except Exception as e:
        logger.error(f"複製任務檔案時發生錯誤: {e}")
        return False

def create_job_function(task_name: str, config: Config):
    """建立 APScheduler 的 job 函數"""
    def job_function():
        logger.info(f"執行排程任務: {task_name}")
        if copy_task_to_todo(task_name, config):
            logger.info(f"任務 {task_name} 執行成功")
        else:
            logger.error(f"任務 {task_name} 執行失敗")

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
    if not config.jobs:
        logger.warning("沒有找到任何排程任務，排程器將不會啟動")
        return None

    try:
        # 建立排程器
        scheduler = BackgroundScheduler(timezone=config.timezone)

        # 為每個 job 設定 cron 觸發器
        for task_name, cron_expr in config.jobs.items():
            try:
                # 建立 job 函數
                job_func = create_job_function(task_name, config)

                # 解析 cron 表達式
                # cron 表達式格式: "分 時 日 月 星期"
                parts = cron_expr.split()
                if len(parts) != 5:
                    logger.error(f"無效的 cron 表達式: {cron_expr}")
                    continue

                minute, hour, day, month, day_of_week = parts

                # 建立 cron 觸發器
                trigger = CronTrigger(
                    minute=minute, hour=hour, day=day,
                    month=month, day_of_week=day_of_week,
                    timezone=config.timezone
                )

                # 添加 job 到排程器
                scheduler.add_job(
                    create_job_function(task_name, config),
                    trigger=trigger,
                    id=f"job_{task_name}",
                    name=f"Task: {task_name}",
                    replace_existing=True
                )

                logger.info(f"已設定排程任務: {task_name} ({cron_expr})")

            except ValueError as e:
                logger.error(f"設定任務 {task_name} 時發生錯誤: {e}")
            except Exception as e:
                logger.error(f"設定任務 {task_name} 時發生未預期錯誤: {e}")

        return scheduler

    except Exception as e:
        logger.error(f"設定排程器時發生錯誤: {e}")
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

    try:
        # 建立配置物件並啟動系統
        config = Config(config_path)
        scheduler_main(config)
    except ValueError as e:
        print(f"配置錯誤: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"啟動排程器時發生錯誤: {e}")
        sys.exit(1)
