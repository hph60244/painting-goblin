Use $AGENT_CWD/skills/build-python-cli-app to write a app for:

# Problem

製作踩地雷遊戲原型

# Constraints

## 實作時註解要與Constraint或Problem的關聯
- 避免Coding Agent在無人監督的狀況下做無關的決策
- 避免Coding Agent在長期任務中遺忘Constraint
- 避免Coding Agent在長期任務中遺忘Problem

## 使用Pygame
- 適合製作2D遊戲原型
- 輕量化與高效能
- 易於人類跟AI使用

## 用極簡風格呈現
- 強調玩法概念
- 節省製作時間

## 使用logger輸出訊息
- 用於除錯
- 高效能
- 易於人類跟AI使用

# Task

## 使腳本接收輸入參數

### Contract
- 踩地雷經典規格 (Windows 版本)
    - 初級 (Beginner): 9x9 网格，10 顆地雷。
    - 中級 (Intermediate): 16x16 网格，40 顆地雷。
    - 高級 (Expert): 30x16 网格，99 顆地雷。
    - 自訂 (Custom): 玩家可自行設定寬、高與地雷總數。

### Acceptance
- 測試各種模式下遊戲可執行

## 使腳本接收輸入參數

### Contract
- 遊戲核心規則
    - 左鍵點擊: 翻開方格。若點到地雷則遊戲結束；若為數字則顯示周圍 8 格的雷數。
    - 右鍵標記: 對懷疑是地雷的方格點擊右鍵插旗，避免誤觸。
    - 數字邏輯: 數字方格顯示該格周圍八個方格內的雷數。
    - 獲勝條件: 翻開所有「沒有地雷」的方格。
    - 第一下必安全: 現代版本通常確保第一下不會點到雷。

### Acceptance
- 測試每條規則符合預期
