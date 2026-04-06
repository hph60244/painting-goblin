# 新增任務方法

## 快速開始

要新增任務到 `painting-goblin` 系統，只需將任務檔案放入以下目錄：

```
$PAINTING_GOBLIN_DIR\tasks\todo\
```

## 詳細步驟

### 1. 準備任務檔案
- 任務檔案可以是任何格式（如 `.txt`, `.md`, `.json` 等）
- 檔案名稱建議使用有意義的名稱，系統會自動添加時間戳記

### 2. 放置任務檔案
將任務檔案複製或移動到：
```
$PAINTING_GOBLIN_DIR\tasks\todo\
```

### 3. 系統自動處理
一旦檔案放入 `todo` 目錄，系統會：
1. **Publisher** 會偵測新任務
2. 將任務移動到 `doing` 目錄
3. **Subscriber** 會執行任務
4. 完成後移動到 `done` 目錄
5. 失敗則移動到 `failed` 目錄

## 目錄結構說明

根據 `config.ini` 配置：
- `base_dir`: `$PAINTING_GOBLIN_DIR\tasks`
- `todo_dir`: `todo` - 待處理任務目錄
- `doing_dir`: `doing` - 執行中任務目錄
- `done_dir`: `done` - 已完成任務目錄
- `failed_dir`: `failed` - 失敗任務目錄

完整路徑：
- 待處理：`$PAINTING_GOBLIN_DIR\tasks\todo\`
- 執行中：`$PAINTING_GOBLIN_DIR\tasks\doing\`
- 已完成：`$PAINTING_GOBLIN_DIR\tasks\done\`
- 失敗：`$PAINTING_GOBLIN_DIR\tasks\failed\`

## 範例

```bash
# 新增一個任務檔案
echo "這是一個測試任務" > "$PAINTING_GOBLIN_DIR\tasks\todo\test_task.txt"

# 查看任務狀態
dir "$PAINTING_GOBLIN_DIR\tasks\todo\"
```

## 注意事項

1. 系統會按照檔案修改時間順序處理（最舊的優先）
2. 可以同時放入多個任務檔案
3. 系統支援並行處理（根據 `subscriber.count` 配置）
4. 任務執行日誌會記錄在 `runner.log` 檔案中

## 檢查任務狀態

```bash
# 查看待處理任務
dir "$PAINTING_GOBLIN_DIR\tasks\todo\"

# 查看執行中任務
dir "$PAINTING_GOBLIN_DIR\tasks\doing\"

# 查看已完成任務
dir "$PAINTING_GOBLIN_DIR\tasks\done\"

# 查看失敗任務
dir "$PAINTING_GOBLIN_DIR\tasks\failed\"

# 查看系統日誌
type runner.log
