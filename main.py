import re
import os
import time
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from threading import Thread
from filelock import FileLock, Timeout
import subprocess
import configparser

# ----------------------------
# 讀取設定檔
# ----------------------------
config = configparser.ConfigParser()
config.read("config.ini")

BASE_DIR = Path(config["task"]["base_dir"])
TODO_DIR = BASE_DIR / config["task"]["todo_dir"]
DOING_DIR = BASE_DIR / config["task"]["doing_dir"]
DONE_DIR = BASE_DIR / config["task"]["done_dir"]
FAILED_DIR = BASE_DIR / config["task"]["failed_dir"]
LOCK_DIR = BASE_DIR / config["task"]["lock_dir"]
TIMEZONE = config["task"].get("timezone", "UTC")
OPENCODE_EXE = config["task"]["opencode_exe"]

PUBLISHER_SLEEP_INTERVAL = float(config["publisher"].get("sleep_interval", 1))

SUBSCRIBER_COUNT = int(config["subscriber"].get("count", 1))
SUBSCRIBER_SLEEP_INTERVAL = float(config["subscriber"].get("sleep_interval", 1))

# 確保資料夾存在
for d in [TODO_DIR, DOING_DIR, DONE_DIR, FAILED_DIR, LOCK_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ----------------------------
# 工具函數
# ----------------------------
def get_oldest_file(folder: Path):
    files = sorted(folder.iterdir(), key=lambda f: f.stat().st_mtime)
    return files[0] if files else None

def strip_time_stamp(file_name: str) -> str:
    pattern = r'\.(?:[BE]\d{17})'
    name, ext = os.path.splitext(file_name)
    new_name = re.sub(pattern, '', name) + ext
    return new_name

def add_timestamp(file_path: Path, datetime_prefix: str):
    now = datetime.now(ZoneInfo(TIMEZONE))
    ts = now.strftime(datetime_prefix + "%Y%m%d%H%M%S%f")[:-3]
    return f"{file_path.stem}.{ts}{file_path.suffix}"

# ----------------------------
# Publisher
# ----------------------------
def publisher():
    if len(list(DOING_DIR.iterdir())) >= SUBSCRIBER_COUNT:
        return

    task_file = get_oldest_file(TODO_DIR)
    if task_file:
        lock_file = LOCK_DIR / f"{task_file.name}.lock"
        try:
            with FileLock(str(lock_file), timeout=0.1):
                if task_file.exists():
                    clean_name = strip_time_stamp(task_file.name)
                    temp_file = Path(clean_name)
                    dest = DOING_DIR / add_timestamp(temp_file, "B")
                    shutil.move(str(task_file), str(dest))
                    print(f"[Publisher] Moved {task_file.name} -> {dest.name}")
        except Timeout:
            pass

# ----------------------------
# Subscriber
# ----------------------------
def execute_task(file_path: Path):
    lock_file = LOCK_DIR / f"{file_path.name}.lock"
    try:
        with FileLock(str(lock_file), timeout=0.1):
            if not file_path.exists():
                return

            print(f"[Subscriber] Executing {file_path.name}")

            try:
                with tempfile.TemporaryDirectory() as tmpdir:
                    tmp_task = Path(tmpdir) / file_path.name
                    shutil.copy(str(file_path), tmp_task)
                    subprocess.run([OPENCODE_EXE, "run", "Execute this task", "--file", str(tmp_task)], check=True, cwd=tmpdir)
                
                dest = DONE_DIR / add_timestamp(file_path, "E")
                try:
                    shutil.move(str(file_path), str(dest))
                except Exception:
                    pass
                print(f"[Subscriber] Finished {file_path.name}, moved to done")
            except Exception as e:
                error_msg = f"Task execution failed: {e}"
                print(f"[Subscriber] {error_msg}, moving to failed")

                log_file = f"{dest.name}.log"
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"{datetime.now(ZoneInfo(TIMEZONE)).isoformat()} - {error_msg}\n")

                dest = FAILED_DIR / file_path.name
                try:
                    shutil.move(str(file_path), str(dest))
                except Exception:
                    pass

    except Timeout:
        pass

def subscriber_worker():
    while True:
        task_file = get_oldest_file(DOING_DIR)
        if task_file:
            execute_task(task_file)
        time.sleep(SUBSCRIBER_SLEEP_INTERVAL)

# ----------------------------
# 主程式
# ----------------------------
if __name__ == "__main__":
    # 啟動多個 subscriber worker
    for _ in range(SUBSCRIBER_COUNT):
        t = Thread(target=subscriber_worker, daemon=True)
        t.start()

    print("[System] Task system started. Ctrl+C to exit.")
    try:
        while True:
            publisher()
            time.sleep(PUBLISHER_SLEEP_INTERVAL)
    except KeyboardInterrupt:
        print("[System] Shutting down...")
