# painting-goblin

任務處理系統 - 基於檔案系統的任務佇列處理器

## 概述

painting-goblin 是一個基於檔案系統的任務處理系統，使用 Publisher-Subscriber 模式來管理任務佇列。系統會監控任務目錄，自動將任務從待處理狀態移動到處理中狀態，並執行任務處理。

## 待辦事項

- idea => wiki
- bookmark => wiki
- Study Opencode auto change model

## 系統架構

系統包含兩種角色：
- **Publisher**: 從待處理目錄 (todo) 移動任務到處理中目錄 (doing)，使用 UUID 機制避免檔案名稱衝突
- **Subscriber**: 從處理中目錄執行任務，並根據結果移動到完成或失敗目錄，包含任務執行監控機制

系統使用檔案鎖定機制來確保任務不會被多個 worker 同時處理，並包含任務執行監控功能，可自動終止停滯的任務。

## 安裝與設定

### 1. 系統需求

- Python 3.8+，filelock 套件
- OpenCode AI CLI 工具

### 2. 安裝 Python 套件

```bash
pip install -r requirements.txt
```

### 3. 安裝 pre-commit hooks（可選）

專案包含 pre-commit 配置，可在提交前自動檢查程式碼格式。安裝步驟：

1. 安裝 pre-commit：
```bash
pip install pre-commit
```

2. 安裝 git hooks：
```bash
pre-commit install
```

### 4. 安裝 OpenCode

系統需要 OpenCode CLI 工具來執行任務。請先安裝 OpenCode：

```bash
npm install -g opencode-ai
```

或根據您的系統從 [OpenCode GitHub](https://github.com/opencodeai/opencode) 下載安裝。

### 5. OpenCode 配置設定

OpenCode 使用 JSON 配置檔案來控制權限和實驗性功能。預設配置檔案位於 `~/.config/opencode/opencode.json`。

以下是建議的配置範例：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "external_directory": "deny",
    "doom_loop": "deny"
  },
  "experimental": {
    "continue_loop_on_deny": true
  }
}
```

配置說明：
- **permission.external_directory**: 控制是否允許存取外部目錄（建議設定為 `deny` 以增強安全性）
- **permission.doom_loop**: 防止無限迴圈（建議設定為 `deny`）
- **experimental.continue_loop_on_deny**: 當權限被拒絕時是否繼續執行（建議設定為 `true`）

您可以根據需要調整這些設定。建立或編輯 `~/.config/opencode/opencode.json` 檔案並貼上上述配置。

### 6. 配置檔案設定

編輯 `config.ini` 檔案，確保以下重要設定正確：

配置檔案包含三個主要區段：

#### [executor] 區段
- `root_dir_path`: 專案根目錄路徑（**必須根據您的安裝位置調整**，範例：`C:\Users\fnaith\Documents\Fork\painting-goblin`）
- `publisher_count`: Publisher worker 數量（預設：`1`）
- `publisher_heartbeat_sec`: Publisher 檢查新任務的間隔時間（秒）（預設：`60`）
- `subscriber_count`: Subscriber worker 數量（同時處理的任務數量）（預設：`1`）
- `subscriber_heartbeat_sec`: Subscriber 檢查新任務的間隔時間（秒）（預設：`60`）
- `monitor_timeout_sec`: 任務停滯超時時間（秒），當任務日誌超過此時間沒有更新時，系統會認為任務停滯並終止（預設：`60`）
- `monitor_terminate_sec`: 終止等待時間（秒），當終止任務時等待程序正常結束的時間，超過此時間會強制殺死程序（預設：`5`）
- `monitor_heartbeat_sec`: 監控檢查間隔（秒），監控執行緒檢查日誌檔案更新時間的間隔（預設：`5`）
- `opencode_exe_path`: OpenCode 執行檔的完整路徑（**必須根據您的安裝位置調整**，範例：`C:\Users\fnaith\AppData\Roaming\npm\node_modules\opencode-ai\node_modules\opencode-windows-x64\bin\opencode.exe`）
- `opencode_cwd_path`: OpenCode 工作目錄路徑。此設定控制執行 OpenCode 命令時的工作目錄（cwd），可用於指定任務執行的基礎目錄。（**必須根據您的安裝位置調整**，範例：`C:\Users\fnaith\Documents\Fork\painting-goblin`）

#### [scheduler] 區段
- `root_dir_path`: 專案根目錄路徑（**必須根據您的安裝位置調整**，範例：`C:\Users\fnaith\Documents\Fork\painting-goblin`）
- `job_dir_path`: 任務檔案目錄路徑（**必須根據您的安裝位置調整**，範例：`C:\Users\fnaith\Documents\Fork\painting-goblin\jobs`）。此設定指定排程系統從哪個目錄讀取任務檔案進行排程執行。。
- `timezone`: 系統時區設定（預設：`Asia/Taipei`）
- `cleaner_schedule`: 清理任務的 cron 排程表達式（預設：`0 0 * * *`，每天午夜執行）
- `cleaner_log_max_day`: 保留日誌檔案的最大天數（預設：`7`）

#### [job:任務名稱] 區段
- 定義排程任務，每個任務使用獨立的區段，格式為 `[job:任務名稱]`
- 每個區段必須包含 `schedule` 欄位，格式為 cron 表達式：`分 時 日 月 星期`
- 可選的參數欄位：可以定義任意參數，值用逗號分隔表示多個值，系統會為每個參數組合創建不同的任務檔案變體
- 範例：
  ```ini
  [job:print-42]
  schedule = 8 21 6 4 *  # 4月6日 21:08 執行
  xxx = a, b
  yyy = 12, 34
  ```
  這會創建 4 個任務檔案：`print-42_xxx-a_yyy-12.md`, `print-42_xxx-a_yyy-34.md`, `print-42_xxx-b_yyy-12.md`, `print-42_xxx-b_yyy-34.md`

### 7. 目錄結構

系統啟動時會自動建立以下目錄結構：

```
painting-goblin/
├── tasks/          # 基礎任務目錄
│   ├── todo/       # 待處理任務
│   ├── doing/      # 處理中任務
│   ├── done/       # 已完成任務
│   ├── failed/     # 失敗任務
│   ├── .log/       # 任務執行日誌目錄
│   └── .lock/      # 檔案鎖定目錄
├── logs/           # 系統執行日誌目錄
├── jobs/           # 範例任務目錄
│   ├── print-42.md
│   ├── print-command.md
│   └── ...
└── ...             # 其他專案檔案
```

## 使用方式

### 啟動任務處理系統 (executor.py)

`executor.py` 是主要的任務處理系統，負責監控任務目錄並執行任務。

```bash
python executor.py [config_file_path]
```

參數：
- `config_file_path`: 可選的配置檔案路徑，預設為 "config.ini"

範例：
```bash
# 使用預設 config.ini
python executor.py

# 使用自訂配置檔案
python executor.py my_config.ini
```

### 啟動任務排程系統 (scheduler.py)

`scheduler.py` 是任務排程系統，根據 config.ini 中的 cron 設定，定期將 job 資料夾中的任務檔案複製到 todo 資料夾。系統還包含自動清理功能，可以定期清理系統中的臨時檔案和舊日誌。

```bash
python scheduler.py [config_file_path]
```

參數：
- `config_file_path`: 可選的配置檔案路徑，預設為 "config.ini"

範例：
```bash
# 使用預設 config.ini
python scheduler.py

# 使用自訂配置檔案
python scheduler.py my_config.ini
```

#### 清理任務功能

`scheduler.py` 包含自動清理功能，可以根據 `cleaner_schedule` 設定定期執行以下清理工作：

1. **清理任務目錄中的非 .md 檔案**：
   - 刪除 `todo`、`doing`、`done`、`failed` 目錄中所有不是 `.md` 檔案的檔案

2. **清理日誌目錄**：
   - 刪除 `.log` 目錄中所有不是 `.md.log` 的檔案
   - 刪除超過 `cleaner_log_max_day` 天數的 `.md.log` 檔案

3. **清理鎖定目錄**：
   - 刪除 `.lock` 目錄中未鎖定的檔案（檔案未被其他程序使用）

清理任務的排程可以在 `config.ini` 的 `[scheduler]` 區段中設定 `cleaner_schedule` 參數，預設為每天午夜執行 (`0 0 * * *`)。您也可以根據需要調整為更頻繁的清理，例如 `0/5 * * * *` 表示每5分鐘執行一次清理。

### 新增任務

有兩種方式可以新增任務：

#### 1. 手動新增
將任務檔案（副檔名為 `.md`）放入 `tasks/todo/` 目錄中。系統會自動偵測並處理。

任務檔案範例 (`jobs/print-42.md`)：
```markdown
請寫一個 Python 程式，印出數字 42。
```

#### 2. 排程新增
在 `config.ini` 中使用 `[job:任務名稱]` 區段設定排程任務，系統會自動在指定時間將 `jobs/` 目錄中的任務檔案複製到 `tasks/todo/` 目錄。支援參數化任務，可以為每個參數組合創建不同的檔案變體。

範例配置：
```ini
[job:print-42]
schedule = 8 21 6 4 *  # 4月6日 21:08 執行
xxx = a, b
yyy = 12, 34

[job:ls-tasks]
schedule = 0 20 * * 1  # 每週一 20:00 執行
```

這會為 `print-42` 任務創建 4 個檔案變體：`print-42_xxx-a_yyy-12.md`, `print-42_xxx-a_yyy-34.md`, `print-42_xxx-b_yyy-12.md`, `print-42_xxx-b_yyy-34.md`

### 監控系統狀態

系統執行時會輸出日誌到控制台和日誌檔案。您可以監控以下資訊：

#### executor.py 日誌
- 控制台輸出
- 檔案：`logs/executor.log`
- 包含：任務移動狀態、任務執行結果、系統錯誤訊息、Publisher/Subscriber 活動

#### scheduler.py 日誌
- 控制台輸出
- 檔案：`logs/scheduler.log`
- 包含：排程任務執行狀態、檔案複製結果、系統錯誤訊息、cron 觸發記錄

#### 任務執行日誌
- 檔案：`tasks/.log/任務檔案名.log`
- 包含：OpenCode 執行輸出、錯誤訊息、任務執行結果

### 停止系統

按 `Ctrl+C` 可優雅地停止系統。

## 任務處理流程

1. **任務提交**: 使用者將 `.md` 任務檔案放入 `tasks/todo/` 目錄
2. **Publisher 處理**: Publisher worker 檢查 `tasks/todo/` 目錄，將最舊的未鎖定任務移動到 `tasks/doing/` 目錄。系統會移除檔案名稱中可能存在的 UUID，然後添加新的 UUID（22個字元）以避免檔案名稱衝突
3. **Subscriber 處理**: Subscriber worker 檢查 `tasks/doing/` 目錄，取得任務並使用 OpenCode 執行。OpenCode 命令會在 `opencode_cwd_path` 設定的工作目錄中執行，這允許任務在不同的目錄環境中執行。系統會監控任務執行狀態，如果任務日誌超過設定的時間（`monitor_timeout_sec`）沒有更新，系統會認為任務停滯並終止執行。
4. **結果處理**:
   - 成功：任務檔案移動到 `tasks/done/` 目錄，保留帶有 UUID 的檔案名稱
   - 失敗：任務檔案移動到 `tasks/failed/` 目錄，保留帶有 UUID 的檔案名稱
5. **日誌記錄**: 所有任務執行日誌儲存在 `tasks/.log/` 目錄中，檔名為 `任務檔案名.log`

### AGENT_PROMPT 說明
系統使用預定義的 AGENT_PROMPT 來控制 OpenCode 代理行為：
```
You are an autonomous, non-interactive agent.
Operational Rules:
1. Do not ask the user any questions or request confirmations.
2. Do not present options or require user selections.
3. Make all decisions automatically based on the provided configuration and policies.
4. Follow a deny-by-default principle for any unauthorized or ambiguous actions.
5. Operate only within explicitly allowed resources.
6. Provide clear, deterministic outcomes for every task.
7. If assumptions are made, document them without requesting clarification.
Your objective is to complete tasks reliably in a fully automated environment.
```

### 參數解析功能
系統支援從檔案名稱解析參數，格式為 `_參數名-參數值`：
- 範例：`research_priority-high_topic-ai.md` 解析為 `[("priority", "high"), ("topic", "ai")]`
- 參數會傳遞給 OpenCode 作為環境變數
- 支援 Unicode 字符（使用 `\w+` 正則表達式匹配）

## 檔案鎖定機制

為避免多個 worker 同時處理同一個任務，系統使用檔案鎖定機制：
- 每個任務檔案對應一個 `.lock` 檔案在 `tasks/.lock/` 目錄中
- worker 在處理任務前會嘗試取得鎖定（非阻塞模式）
- 鎖定失敗表示任務正在被其他 worker 處理
- 鎖定檔案名稱為 `任務檔案名.lock`

## 疑難排解

### 常見問題

1. **配置檔案路徑錯誤**
   - 確認 `config.ini` 中的 `root_dir_path` 設定正確
   - 檢查配置檔案是否位於正確位置

2. **OpenCode 執行檔找不到**
   - 檢查 `config.ini` 中的 `opencode_exe_path` 路徑是否正確
   - 確認 OpenCode 已正確安裝

3. **OpenCode 工作目錄問題**
   - 檢查 `config.ini` 中的 `opencode_cwd_path` 設定是否正確
   - 確認指定的工作目錄存在且有適當的存取權限
   - 如果任務需要在特定目錄中執行，請確保 `opencode_cwd_path` 指向正確的目錄

4. **權限問題**
   - 確認 Python 有權限讀寫專案目錄
   - 檢查檔案鎖定目錄的存取權限

5. **任務未處理**
   - 檢查任務檔案副檔名是否為 `.md`
   - 確認檔案在正確的目錄中（`tasks/todo/`）
   - 檢查系統日誌是否有錯誤訊息

6. **排程任務未執行**
   - 檢查 `config.ini` 中的 `[job:任務名稱]` 區段設定是否正確
   - 確認每個任務區段都包含 `schedule` 欄位
   - 確認 cron 表達式格式正確（分 時 日 月 星期）
   - 檢查 `jobs` 目錄中是否有對應的任務檔案
   - 查看 `logs/scheduler.log` 是否有錯誤訊息

### 日誌位置

系統提供多種日誌檔案，用於監控和除錯：

- **logs/executor.log**: `executor.py`日誌，包含任務移動狀態、Publisher/Subscriber 活動、系統錯誤
- **logs/scheduler.log**: `scheduler.py`日誌，包含排程任務執行狀態、檔案複製結果、cron 觸發記錄
- **tasks/.log/任務檔案名.log**: 包含 OpenCode 執行輸出、任務執行結果、錯誤訊息
