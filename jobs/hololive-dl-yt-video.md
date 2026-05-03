Use $AGENT_CWD/skills/build-python-cli-app to write a app for:

# Problem

下載Hololive成員的頻道的YouTube影片

# Constraints

## 實作時如果需要做決策，要根據Constraint或Problem做決策並明確註解
- 避免Coding Agent在無人監督的狀況下做無關的決策
- 避免Coding Agent在長期任務中遺忘Constraint
- 避免Coding Agent在長期任務中遺忘Problem

## 使用排程任務下載影片
- YouTube影片變動頻率不高
- 避免浪費CPU等待
- 避免浪費網路頻寬
- 避免DOS外部api

## 影片下載到檔案系統
- 避免浪費CPU
- 避免浪費網路頻寬

## 使用apscheduler
- 用於實作排程任務
- 排程類型靈活
- 易於人類跟AI設定跟使用

## 使用SQLite
- 用於儲存任務資訊
- 輕量化與高效能
- 易於人類跟AI使用

## 每個任務各自連接SQLite
- SQLite objects created in a thread can only be used in that same thread

## 使用yt-dlp
- 用於取得YouTube影片的資訊
- 用於下載最高品質的YouTube影片
- 不須設定金鑰
- 易於人類跟AI使用

## 使用ini設定檔
- 用於設定參數
- 結構極度簡單
- 易於人類跟AI使用

## 使用logger輸出訊息
- 用於除錯
- 高效能
- 易於人類跟AI使用

# Task

## 使腳本接收輸入參數

### Contract
- 腳本用法為`python hololive-dl-yt-video.py <config_file_path>`
- <config_file_path>參數缺失時，預設為`hololive-dl-yt-video.ini`
- <config_file_path>檔案不存在時建立ini檔案，並包含所有預設值
- <config_file_path>檔案不為合法ini時報錯並結束

### Acceptance
- 輸入有<config_file_path>且檔案為合法ini時: 正常執行
- 輸入沒有<config_file_path>且`hololive-dl-yt-video.ini`檔案為合法ini時: 正常執行
- <config_file_path>但檔案不存在建立ini檔案成功時: 正常執行
- <config_file_path>但檔案不存在建立ini檔案失敗時: 報錯並結束
- <config_file_path>不為合法ini時報錯時: 報錯並結束

## 使腳本解析<config_file_path>檔案

### Contract
- 使用configparser解析<config_file_path>
- <config_file_path>解析失敗時報錯並結束
- <config_file_path>檔案的[general] section包含:
  - sqlite_file_path: SQLite的檔案路徑。若缺失時，預設為`hololive-dl-yt-video.sqlite3`
  - task_timezone: apscheduler的時區設定。若缺失時，預設為`Asia/Taipei`
  - sync_yt_video_task_cron_schedule: sync_yt_video_task的cron週期，預設為`*/5 * * * *`
  - sync_yt_video_task_timeout_minutes: sync_yt_video_task的超時分鐘數，預設為5
  - sync_yt_video_task_max_video_minutes: sync_yt_video_task的要下載影片的最大分鐘數，預設為10
  - sync_yt_video_task_cooldown_minutes: sync_yt_video_task的冷卻分鐘數，預設為1440
  - dl_yt_video_task_cron_schedule: dl_yt_video_task的cron週期，預設為`* * * * *`
  - dl_yt_video_task_timeout_minutes: dl_yt_video_task的超時分鐘數，預設為5
  - dl_yt_video_task_output_folder_path: dl_yt_video_task下載檔案的根資料夾路徑，預設為`downloads`

### Acceptance
- <config_file_path>檔案有[general] section時: 正常執行
- <config_file_path>檔案缺失[general] section時: 正常執行

## 初始化SQLite DB

### Contract
- `sqlite_file_path`檔案不存在時建立新的SQLite DB
- 建立新的SQLite DB失敗時報錯並結束

### Acceptance
- `sqlite_file_path`檔案存在時: 正常執行
- `sqlite_file_path`檔案不存在但建立新的SQLite DB成功時: 正常執行
- `sqlite_file_path`檔案不存在且建立新的SQLite DB失敗時: 報錯並結束

## 連接SQLite DB

### Contract
- 使用sqlite3連接`sqlite_file_path`
- `sqlite_file_path`連接失敗時報錯並結束

### Acceptance
- `sqlite_file_path`連接成功時: 正常執行
- `sqlite_file_path`連接失敗時: 報錯並結束

## 初始化hololive_channel資料表

### Contract
- `sqlite_file_path`裡不存在`hololive_channel`資料表時建立新的table
- 建立新的資料表失敗時報錯
- 欄位: channel_id, talent_name, updated_at, status
  - channel_id: youtube channel id; primary key
  - talent_name: utf8 string
  - updated_at: 最後更新時間; 格式為ISO 8601: `YYYY-MM-DD HH:MM:SS`
  - status: task status; STARTED|COMPLETED|FAILED

### Acceptance
- `hololive_channel`資料表存在時: 正常執行
- `hololive_channel`資料表不存在但建立新的table成功時: 正常執行
- `hololive_channel`資料表不存在且建立新的table失敗時: 報錯並結束

## 驗證hololive_channel資料表

### Contract
- 確認`hololive_channel`資料表的欄位符合規格
- `hololive_channel`資料表不符合規格時報錯並結束

### Acceptance
- `hololive_channel`驗證成功時: 正常執行
- `hololive_channel`驗證失敗時: 報錯並結束

## 初始化dl_yt_video_task資料表

### Contract
- `sqlite_file_path`裡不存在`dl_yt_video_task`資料表時建立新的table
- 建立新的資料表失敗時報錯
- 欄位: video_id, channel_id, updated_at, status
  - video_id: youtube video id; primary key
  - channel_id: youtube channel id
  - video_name: youtube name id; utf8 string
  - updated_at: 最後更新時間; 格式為ISO 8601: `YYYY-MM-DD HH:MM:SS`
  - status: task status; STARTED|COMPLETED|FAILED

### Acceptance
- `dl_yt_video_task`資料表存在時: 正常執行
- `dl_yt_video_task`資料表不存在但建立新的table成功時: 正常執行
- `dl_yt_video_task`資料表不存在且建立新的table失敗時: 報錯並結束

## 驗證dl_yt_video_task資料表

### Contract
- 確認`dl_yt_video_task`資料表的欄位符合規格
- `dl_yt_video_task`資料表不符合規格時報錯並結束

### Acceptance
- `dl_yt_video_task`驗證成功時: 正常執行
- `dl_yt_video_task`驗證失敗時: 報錯並結束

## 初始化dl_yt_video_task_output_folder_path資料夾

### Contract
- `dl_yt_video_task_output_folder_path`資料夾不存在時建立新的資料夾
- 建立新的資料表失敗時報錯

### Acceptance
- `dl_yt_video_task_output_folder_path`資料夾存在時: 正常執行
- `dl_yt_video_task_output_folder_path`資料夾不存在但建立新的資料夾成功時: 正常執行
- `dl_yt_video_task_output_folder_path`資料夾不存在且建立新的資料夾失敗時: 報錯並結束

## 註冊sync_yt_video_task

### Contract
- 根據`sync_yt_video_task_cron_schedule`設定`sync_yt_video_task`
- `sync_yt_video_task`步驟:
    1. 標記超時任務為失敗
        - 搜尋`hololive_channel`資料表裡所有`status=STARTED`且`updated_at`離現在超過`sync_yt_video_task_timeout_minutes`的task
        - 把task的`status`標記為`FAILED`
    2. 還有任務在執行時結束
        - 在`hololive_channel`資料表找到`status=STARTED`的task時強制結束task
    3. 執行任務
        - 在`hololive_channel`資料表裡面找一個`updated_at`最舊的，`status=COMPLETED||FAILED`且`updated_at`離現在超過`sync_yt_video_task_cooldown_minutes`的task
        - 把task的`status`標記為`STARTED`，`updated_at`更新為現在時間
        - 根據task的`channel_id`從YouTube取得全部的video資訊
        - 反轉全部video資訊的順序
        - 對每一個video資訊:
            - 如果一個video時長大於`sync_yt_video_task_max_video_minutes`分鐘就忽略
            - 根據video的發布時間，用`當前<video>的id,<channel_id>,'',<當前時間>,'FAILED'`在`dl_yt_video_task`資料表裡建立新的task
        - 如果task的執行失敗:
            - 把task的`status`標記為`FAILED`，`updated_at`更新為現在時間
            - 強制結束task
        - 如果task的執行時間超過`sync_yt_video_task_timeout_minutes`:
            - 把task的`status`標記為`FAILED`，`updated_at`更新為現在時間
            - 強制結束task
        - 如果task正常執行:
            - 把task的`status`標記為`COMPLETED`，`updated_at`更新為現在時間
            - 正常結束task

### Acceptance
- 可在`hololive_channel`資料表裡加上 `channel_id=UCqm3BQLlJfvkTsX_hvm0UmA, talent_name=tsunomaki-watame` 測試，`dl_yt_video_task`資料表至少能找到新的task

## 註冊dl_yt_video_task

### Contract
- 根據`dl_yt_video_task_cron_schedule`設定`dl_yt_video_task`
- `dl_yt_video_task`步驟:
    1. 標記超時任務為失敗
        - 搜尋`dl_yt_video_task`資料表裡所有`status=STARTED`且`updated_at`離現在超過`dl_yt_video_task_timeout_minutes`的task
        - 把task的`status`標記為`FAILED`
    2. 還有任務在執行時結束
        - 在`dl_yt_video_task`資料表找到`status=STARTED`的task時強制結束task
    3. 執行任務
        - 在`dl_yt_video_task`資料表裡面找一個`updated_at`最舊的，`status=COMPLETED||FAILED`的task
        - 把task的`status`標記為`STARTED`，`updated_at`更新為現在時間
        - 根據task的`channel_id`在`hololive_channel`資料表裡面找到`talent_name`
        - 根據task的`video_id`從YouTube下載最高品質的.mp4到`dl_yt_video_task_output_folder_path/<talent_name>/<video_title>.mp4`，`video_title`為影片標題
        - 如果task的執行失敗:
            - 把task的`status`標記為`FAILED`，`updated_at`更新為現在時間
            - 強制結束task
        - 如果task的執行時間超過`dl_yt_video_task_task_timeout_minutes`:
            - 把task的`status`標記為`FAILED`，`updated_at`更新為現在時間
            - 強制結束task
        - 如果task正常執行:
            - 把task的`status`標記為`COMPLETED`，`video_name`更新為影片的檔案名稱，`updated_at`更新為現在時間
            - 正常結束task

### Acceptance
- 可在`hololive_channel`資料表裡加上 `channel_id=UCqm3BQLlJfvkTsX_hvm0UmA, talent_name=tsunomaki-watame`，在`dl_yt_video_task`資料表裡加上 `channel_id=UCqm3BQLlJfvkTsX_hvm0UmA, video_id=d3UTywBDSW4`測試，`dl_yt_video_task_output_folder_path/tsunomaki-watame`資料表能找到新的影片
