Use $AGENT_CWD/skills/build-python-cli-app to write a app for:

# Problem

製作Snake遊戲原型

# Constraints

## 實作時註解要與Constraint或Problem的關聯
- 避免Coding Agent在無人監督的狀況下做無關的決策
- 避免Coding Agent在長期任務中遺忘Constraint
- 避免Coding Agent在長期任務中遺忘Problem

## 使用Pygame
- 適合製作2D遊戲原型
- 輕量化

## 用極簡風格呈現
- 強調玩法概念
- 節省製作時間

## 使用logger輸出訊息
- 用於人類跟AI除錯

# Task

## 使腳本接收輸入參數

### Contract
- Snake: Grid movement, growing linked list, self-collision

### Acceptance
- 測試遊戲執行符合原作描述
