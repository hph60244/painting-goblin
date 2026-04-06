# painting-goblin

任務處理系統 - 基於檔案系統的任務佇列處理器

## 概述

painting-goblin 是一個基於檔案系統的任務處理系統，使用 Publisher-Subscriber 模式來管理任務佇列。系統會監控任務目錄，自動將任務從待處理狀態移動到處理中狀態，並執行任務處理。

## 待辦事項

以下是系統的未來發展方向：

- [ ] **make report skill** - 開發學習技能功能，讓系統能夠處理研究任務
- [ ] **build app skill** - 建立應用程式開發技能，支援更複雜的應用程式建置任務
- [ ] **allow opencode agent setting** - 允許 OpenCode 代理設定，提供更靈活的 AI 代理配置選項

## 系統架構

系統包含兩種角色：
- **Publisher**: 從待處理目錄 (todo) 移動任務到處理中目錄 (doing)
- **Subscriber**: 從處理中目錄執行任務，並根據結果移動到完成或失敗目錄

系統使用檔案鎖定機制來確保任務不會被多個 worker 同時處理。

## 安裝與設定

### 1. 系統需求

- Python 3.14+
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

### 5. 環境變數設定

設定 `PAINTING_GOBLIN_DIR` 環境變數，指向專案根目錄：

**Windows (CMD):**
```cmd
set PAINTING_GOBLIN_DIR=C:\Users\fnaith\Documents\Fork\painting-goblin
```

**Windows (PowerShell):**
```powershell
$env:PAINTING_GOBLIN_DIR = "C:\Users\fnaith\Documents\Fork\painting-goblin"
```

**Linux/macOS:**
```bash
export PAINTING_GOBLIN_DIR=/path/to/painting-goblin
```

建議將此設定加入您的 shell 設定檔（如 `.bashrc`, `.zshrc`, 或 PowerShell 設定檔）。

### 6. 配置檔案設定

編輯 `config.ini` 檔案，確保以下重要設定正確：

配置檔案包含四個主要區段：

#### [task] 區段
- `base_dir_name`: 基礎任務目錄名稱（預設：`task`）
- `todo_dir_name`: 待處理任務目錄名稱（預設：`todo`）
- `doing_dir_name`: 處理中任務目錄名稱（預設：`doing`）
- `done_dir_name`: 已完成任務目錄名稱（預設：`done`）
- `failed_dir_name`: 失敗任務目錄名稱（預設：`failed`）
- `log_dir_name`: 任務執行日誌目錄名稱（預設：`.log`）
- `lock_dir_name`: 檔案鎖定目錄名稱（預設：`.lock`）
- `timezone`: 系統時區設定（預設：`Asia/Taipei`）
- `opencode_exe`: OpenCode 執行檔的完整路徑（**必須根據您的安裝位置調整**）

#### [runner] 區段
- `log_dir_name`: runner 系統日誌目錄名稱（預設：`log`）
- `publisher_count`: Publisher worker 數量（預設：`1`）
- `publisher_heartbeat_secs`: Publisher 檢查新任務的間隔時間（秒）（預設：`3`）
- `subscriber_count`: Subscriber worker 數量（同時處理的任務數量）（預設：`3`）
- `subscriber_heartbeat_secs`: Subscriber 檢查新任務的間隔時間（秒）（預設：`3`）

#### [scheduler] 區段
- `log_dir_name`: scheduler 系統日誌目錄名稱（預設：`log`）
- `example_dir_name`: 範例任務目錄名稱（預設：`example`）

#### [job] 區段
- 定義排程任務，格式為 `任務名稱 = cron表達式`
- cron 表達式格式：`分 時 日 月 星期`
- 範例：`print-42 = 8 21 6 4 *` 表示在 4月6日 21:08 執行 `print-42` 任務

### 7. 目錄結構

系統啟動時會自動建立以下目錄結構：

```
painting-goblin/
├── task/           # 基礎任務目錄
│   ├── todo/       # 待處理任務
│   ├── doing/      # 處理中任務
│   ├── done/       # 已完成任務
│   ├── failed/     # 失敗任務
│   ├── .log/       # 任務執行日誌
│   └── .lock/      # 檔案鎖定目錄
├── log/            # 系統執行日誌
├── example/        # 範例任務目錄
│   ├── print-42.md
│   ├── ls-tasks.md
│   └── ...
└── ...             # 其他專案檔案
```

## 使用方式

### 啟動任務處理系統 (runner.py)

`runner.py` 是主要的任務處理系統，負責監控任務目錄並執行任務。

```bash
python runner.py [config_file_path]
```

參數：
- `config_file_path`: 可選的配置檔案路徑，預設為 "config.ini"

範例：
```bash
# 使用預設 config.ini
python runner.py

# 使用自訂配置檔案
python runner.py my_config.ini
```

### 啟動任務排程系統 (scheduler.py)

`scheduler.py` 是任務排程系統，根據 config.ini 中的 cron 設定，定期將 example 資料夾中的任務檔案複製到 todo 資料夾。

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

### 新增任務

有兩種方式可以新增任務：

#### 1. 手動新增
將任務檔案（副檔名為 `.md`）放入 `task/todo/` 目錄中。系統會自動偵測並處理。

任務檔案範例 (`example/print-42.md`)：
```markdown
請寫一個 Python 程式，印出數字 42。
```

#### 2. 排程新增
在 `config.ini` 的 `[job]` 區段設定排程任務，系統會自動在指定時間將 `example/` 目錄中的任務檔案複製到 `task/todo/` 目錄。

範例配置：
```ini
[job]
print-42 = 8 21 6 4 *      # 4月6日 21:08 執行
ls-tasks = 0 20 * * 1  # 每週一 20:30 執行
```

### 監控系統狀態

系統執行時會輸出日誌到控制台和日誌檔案。您可以監控以下資訊：

#### runner.py 日誌
- 控制台輸出
- 檔案：`log/runner.log`
- 包含：任務移動狀態、任務執行結果、系統錯誤訊息

#### scheduler.py 日誌
- 控制台輸出
- 檔案：`log/scheduler.log`
- 包含：排程任務執行狀態、檔案複製結果、系統錯誤訊息

#### 任務執行日誌
- 檔案：`task/.log/任務檔案名.log`
- 包含：OpenCode 執行輸出、錯誤訊息

### 停止系統

按 `Ctrl+C` 可優雅地停止系統。

## 任務處理流程

1. **任務提交**: 使用者將 `.md` 任務檔案放入 `todo/` 目錄
2. **Publisher 處理**: Publisher worker 檢查 `todo/` 目錄，將最舊的未鎖定任務移動到 `doing/` 目錄，並添加開始時間戳記（格式：`檔案名.BYYYYMMDDHHMMSSmmm.md`）
3. **Subscriber 處理**: Subscriber worker 檢查 `doing/` 目錄，取得任務並使用 OpenCode 執行
4. **結果處理**:
   - 成功：任務檔案移動到 `done/` 目錄，並添加結束時間戳記（格式：`檔案名.EYYYYMMDDHHMMSSmmm.md`）
   - 失敗：任務檔案移動到 `failed/` 目錄，保留原始檔名
5. **日誌記錄**: 所有任務執行日誌儲存在 `.log/` 目錄中，檔名為 `任務檔案名.log`

## 檔案鎖定機制

為避免多個 worker 同時處理同一個任務，系統使用檔案鎖定機制：
- 每個任務檔案對應一個 `.lock` 檔案在 `.lock/` 目錄中
- worker 在處理任務前會嘗試取得鎖定
- 鎖定失敗表示任務正在被其他 worker 處理

## 疑難排解

### 常見問題

1. **OpenCode 執行檔找不到**
   - 檢查 `config.ini` 中的 `opencode_exe` 路徑是否正確
   - 確認 OpenCode 已正確安裝

2. **環境變數未設定**
   - 確認 `PAINTING_GOBLIN_DIR` 環境變數已設定
   - 重新啟動終端機或 IDE 使環境變數生效

3. **權限問題**
   - 確認 Python 有權限讀寫專案目錄
   - 檢查檔案鎖定目錄的存取權限

4. **任務未處理**
   - 檢查任務檔案副檔名是否為 `.md`
   - 確認檔案在正確的目錄中（`task/todo/`）
   - 檢查系統日誌是否有錯誤訊息

5. **排程任務未執行**
   - 檢查 `config.ini` 中的 `[job]` 區段設定是否正確
   - 確認 cron 表達式格式正確（分 時 日 月 星期）
   - 檢查 `example/` 目錄中是否有對應的任務檔案
   - 查看 `log/scheduler.log` 是否有錯誤訊息

### 日誌位置

系統提供多種日誌檔案，用於監控和除錯：

- **log/runner.log**: `runner.py`日誌，包含任務移動狀態、Publisher/Subscriber 活動、系統錯誤
- **log/scheduler.log**: `scheduler.py`日誌，包含排程任務執行狀態、檔案複製結果、cron 觸發記錄
- **task/.log/任務檔案名.log**: 包含 OpenCode 執行輸出、任務執行結果、錯誤訊息
