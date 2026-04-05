# 模板任務排程器 (scheduler.py)

## 簡介

`scheduler.py` 是一個模板任務排程器，可以定時將 `template` 資料夾中的任務檔案複製到 `todo` 目錄，讓 `runner.py` 系統自動處理。

## 功能特點

1. **定時排程**：根據配置定時處理模板任務
2. **多種觸發方式**：
   - 特定時間（如 09:00, 14:00, 18:00）
   - 固定間隔（如每 60 分鐘）
3. **手動操作**：支援手動執行、複製特定模板、列出模板
4. **日誌記錄**：所有操作都會記錄到 `scheduler.log` 檔案

## 安裝與設定

### 1. 安裝依賴套件
```bash
pip install -r requirements.txt
```

### 2. 配置設定檔 (`config.ini`)
在 `config.ini` 中添加 `[scheduler]` 部分：
```ini
[scheduler]
enabled = true
template_dir = template
interval_minutes = 60
specific_times = 09:00,14:00,18:00
```

### 3. 創建模板目錄
```bash
mkdir template
```

## 使用方法

### 啟動排程器
```bash
python scheduler.py
```

### 手動處理所有模板
```bash
python scheduler.py --manual
```

### 複製特定模板
```bash
python scheduler.py --copy 模板檔案名稱
```

### 列出所有模板
```bash
python scheduler.py --list
```

## 配置選項說明

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `enabled` | 是否啟用排程器 | `true` |
| `template_dir` | 模板目錄路徑 | `template` |
| `interval_minutes` | 檢查間隔（分鐘） | `60` |
| `specific_times` | 特定執行時間（逗號分隔） | `09:00,14:00,18:00` |

## 模板檔案格式

模板檔案可以是任何格式（如 `.txt`, `.md`, `.json` 等），系統會自動為檔案名稱添加時間戳記。

### 範例模板檔案
```markdown
# 每日報告任務

## 任務描述
生成每日工作報告，包含：
1. 完成的工作項目
2. 遇到的問題
3. 明日計劃

## 執行指令
請使用 OpenCode 生成一份詳細的每日報告。
```

## 工作流程

1. 排程器根據配置定時檢查 `template` 目錄
2. 將模板檔案複製到 `tasks/todo` 目錄，並添加時間戳記
3. `runner.py` 系統自動偵測並處理 `todo` 目錄中的任務
4. 任務完成後移動到 `done` 目錄，失敗則移動到 `failed` 目錄

## 日誌檔案

- `scheduler.log`：排程器操作日誌
- `runner.log`：任務執行日誌（由 `runner.py` 產生）

## 注意事項

1. 排程器會為每個複製的檔案添加時間戳記（格式：`BYYYYMMDDHHMMSSmmm`）
2. 如果目標檔案已存在，預設會跳過（除非使用強制複製）
3. 排程器與 `runner.py` 可以同時運行，互不影響
4. 可以透過修改 `config.ini` 動態調整排程設定

## 故障排除

### 問題：排程器沒有執行
- 檢查 `config.ini` 中的 `enabled` 設定是否為 `true`
- 檢查 `scheduler.log` 檔案中的錯誤訊息
- 確認 `template` 目錄是否存在且有檔案

### 問題：模板檔案沒有被複製
- 檢查檔案權限
- 確認 `tasks/todo` 目錄是否存在
- 查看 `scheduler.log` 中的詳細資訊

### 問題：檔案名稱亂碼
- 確保使用 UTF-8 編碼儲存模板檔案
- 檢查系統地區設定