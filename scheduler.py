import os
import shutil
import time
import logging
import schedule
import threading
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import configparser
from typing import List, Dict, Optional
from filelock import FileLock, Timeout

# ----------------------------
# 讀取設定檔
# ----------------------------
config = configparser.ConfigParser()
config.read("config.ini")

required_sections = ["task", "scheduler"]
for section in required_sections:
    if not config.has_section(section):
        raise ValueError(f"Missing required section in config.ini: [{section}]")

BASE_DIR = Path(config["task"]["base_dir"])
TODO_DIR = BASE_DIR / config["task"]["todo_dir"]
TIMEZONE = config["task"].get("timezone", "UTC")

# Scheduler 配置
TEMPLATE_DIR = Path(config["scheduler"].get("template_dir", "template"))
SCHEDULE_INTERVAL = int(config["scheduler"].get("interval_minutes", 60))  # 預設每小時檢查一次
SCHEDULE_SPECIFIC_TIMES = config["scheduler"].get("specific_times", "").split(",")  # 例如 "09:00,14:00,18:00"
ENABLE_SCHEDULER = config["scheduler"].getboolean("enabled", True)

# 確保目錄存在
TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
TODO_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------
# 設定 logging
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('scheduler.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# ----------------------------
# 工具函數
# ----------------------------
def add_timestamp(file_path: Path) -> str:
    """為檔案名稱添加時間戳記"""
    now = datetime.now(ZoneInfo(TIMEZONE))
    ts = now.strftime("B%Y%m%d%H%M%S%f")[:-3]  # B 開頭表示開始時間
    return f"{file_path.stem}.{ts}{file_path.suffix}"

def copy_template_to_todo(template_file: Path, force_copy: bool = False) -> bool:
    """
    將模板檔案複製到 todo 目錄
    
    Args:
        template_file: 模板檔案路徑
        force_copy: 是否強制複製（即使目標已存在）
    
    Returns:
        bool: 複製是否成功
    """
    try:
        # 檢查檔案是否存在
        if not template_file.exists():
            logger.warning(f"模板檔案不存在: {template_file}")
            return False
        
        # 生成帶時間戳記的目標檔案名稱
        dest_filename = add_timestamp(template_file)
        dest_path = TODO_DIR / dest_filename
        
        # 檢查是否已存在相同檔案（除非強制複製）
        if dest_path.exists() and not force_copy:
            logger.debug(f"目標檔案已存在，跳過: {dest_path}")
            return False
        
        # 複製檔案
        shutil.copy2(str(template_file), str(dest_path))
        logger.info(f"已複製模板到 todo: {template_file.name} -> {dest_filename}")
        return True
        
    except (OSError, PermissionError, shutil.Error) as e:
        logger.error(f"複製模板檔案失敗 {template_file}: {e}")
        return False

def process_all_templates() -> None:
    """處理所有模板檔案"""
    logger.info("開始處理模板檔案...")
    
    try:
        # 獲取所有模板檔案
        template_files = list(TEMPLATE_DIR.iterdir())
        if not template_files:
            logger.debug("模板目錄中沒有檔案")
            return
        
        processed_count = 0
        for template_file in template_files:
            if template_file.is_file():
                if copy_template_to_todo(template_file):
                    processed_count += 1
        
        logger.info(f"模板處理完成，共處理 {processed_count} 個檔案")
        
    except Exception as e:
        logger.error(f"處理模板時發生錯誤: {e}")

def process_specific_template(template_name: str) -> bool:
    """
    處理特定的模板檔案
    
    Args:
        template_name: 模板檔案名稱
    
    Returns:
        bool: 處理是否成功
    """
    template_file = TEMPLATE_DIR / template_name
    if not template_file.exists():
        logger.error(f"指定的模板檔案不存在: {template_name}")
        return False
    
    return copy_template_to_todo(template_file)

# ----------------------------
# 排程任務
# ----------------------------
def scheduled_job() -> None:
    """排程任務：處理所有模板檔案"""
    logger.info("執行排程任務...")
    process_all_templates()

def setup_schedule() -> None:
    """設定排程任務"""
    # 清除現有排程
    schedule.clear()
    
    # 根據配置設定排程
    if SCHEDULE_SPECIFIC_TIMES and SCHEDULE_SPECIFIC_TIMES[0]:  # 有指定特定時間
        for time_str in SCHEDULE_SPECIFIC_TIMES:
            time_str = time_str.strip()
            if time_str:
                schedule.every().day.at(time_str).do(scheduled_job)
                logger.info(f"已設定排程任務在每天 {time_str}")
    else:  # 使用間隔時間
        schedule.every(SCHEDULE_INTERVAL).minutes.do(scheduled_job)
        logger.info(f"已設定排程任務每 {SCHEDULE_INTERVAL} 分鐘執行一次")
    
    # 立即執行一次
    scheduled_job()

def run_scheduler() -> None:
    """執行排程器主循環"""
    if not ENABLE_SCHEDULER:
        logger.info("排程器已禁用")
        return
    
    logger.info("=" * 50)
    logger.info("模板排程器啟動")
    logger.info(f"模板目錄: {TEMPLATE_DIR}")
    logger.info(f"目標目錄: {TODO_DIR}")
    logger.info(f"時區: {TIMEZONE}")
    logger.info("=" * 50)
    
    # 設定排程
    setup_schedule()
    
    logger.info("排程器已啟動，按 Ctrl+C 結束")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)  # 每秒檢查一次排程
    except KeyboardInterrupt:
        logger.info("收到中斷訊號，正在關閉排程器...")
    except Exception as e:
        logger.error(f"排程器發生未預期錯誤: {e}")
    finally:
        logger.info("排程器關閉完成")

# ----------------------------
# CLI 介面
# ----------------------------
def manual_run() -> None:
    """手動執行：處理所有模板檔案"""
    logger.info("手動執行模板處理...")
    process_all_templates()
    logger.info("手動執行完成")

def manual_copy(template_name: str) -> None:
    """手動複製特定模板檔案"""
    logger.info(f"手動複製模板: {template_name}")
    if process_specific_template(template_name):
        logger.info(f"成功複製模板: {template_name}")
    else:
        logger.error(f"複製模板失敗: {template_name}")

def list_templates() -> None:
    """列出所有模板檔案"""
    logger.info("模板檔案列表:")
    try:
        template_files = list(TEMPLATE_DIR.iterdir())
        if not template_files:
            logger.info("  沒有模板檔案")
            return
        
        for i, template_file in enumerate(template_files, 1):
            if template_file.is_file():
                size = template_file.stat().st_size
                mtime = datetime.fromtimestamp(template_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"  {i}. {template_file.name} ({size} bytes, 修改時間: {mtime})")
    except Exception as e:
        logger.error(f"列出模板時發生錯誤: {e}")

# ----------------------------
# 主程式
# ----------------------------
def main() -> None:
    """主程式入口點"""
    import argparse
    
    parser = argparse.ArgumentParser(description='模板任務排程器')
    parser.add_argument('--run', action='store_true', help='執行排程器')
    parser.add_argument('--manual', action='store_true', help='手動處理所有模板')
    parser.add_argument('--copy', type=str, help='複製特定模板檔案')
    parser.add_argument('--list', action='store_true', help='列出所有模板檔案')
    
    args = parser.parse_args()
    
    if args.manual:
        manual_run()
    elif args.copy:
        manual_copy(args.copy)
    elif args.list:
        list_templates()
    else:
        # 預設執行排程器
        run_scheduler()

if __name__ == "__main__":
    main()