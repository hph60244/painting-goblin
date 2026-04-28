# Research Plan: 讓 AI 不用監督就把事情做對

## Main Research Question
基於 Harness Engineering 的概念，尋找真正有效的方法讓 AI 不用監督就能可靠地完成任務。

## Subtopics

### 1. Harness Engineering 核心概念與方法
- Harness 的五層架構：上下文裝配、工具治理、安全審批、回饋狀態、熵管理
- Agent = Loop(Model + Harness) 公式的具體實踐
- OpenAI Codex App Server 的 Harness 實作案例

### 2. 無人監督 AI 的可靠性工程方法
- 環境設計如何取代人工監督
- 回饋迴路與自我修正機制
- 安全邊界與約束系統的實務做法

### 3. 現有 Agent 框架的 Harness 比較分析
- Claude Code / OpenAI Codex CLI 的架構比較
- 各框架在上下文管理、工具治理、安全審批方面的差異
- 生產環境 vs Demo 級別的關鍵區別

## Synthesis Approach
將三個 subtopics 的發現整合，回答：「要讓 AI 不用監督就把事情做對，真正有效的方法是什麼？」並以 Harness Engineering 為框架提供具體可行的建議。
