# Comparative Analysis Report: 讓 AI 不用監督就把事情做對

## 核心問題
在 Harness Engineering 的框架下，什麼是真正有效的方法讓 AI 不用人工監督就能可靠地完成任務？

---

## 1. 核心洞見：Agent 能力 = 模型 × 環境

參考文章（mCell, 2026）的核心論點指出：

> "Agent 的重點不在模型，而在環境。"

並將傳統公式升級為：

> **Agent = Loop(Model + Harness)**

其中 Context 和 Tools 已被 Harness 吸納。真正決定 agent 上限的，不是你有沒有這些元件，而是你有沒有把這些元件工程化成一個可以長期運轉的環境。

### 三個最重要的關鍵詞
- **約束（Constraint）**
- **回饋（Feedback）**
- **穩定（Stability）**

---

## 2. Harness 工程的五層架構 vs. 無人監督可靠性方法

以下是從參考文章與跨框架研究中提煉的，對應五層架構的有效方法：

### 2.1 上下文裝配系統

| Harness 層 | 無人監督的具體方法 | 實例框架 |
|---|---|---|
| 動態提示詞裝配 | 將提示詞拆為六層（基礎模板、使用者偏好、專案上下文、Skills、工具描述、工具定義），不同來源有不同優先級和新鮮度 | Claude Code: 層級式 CLAUDE.md + auto memory + 路徑範圍規則 |
| 上下文裁剪 | 當 context 滿時自動壓縮，保留專案根目錄 CLAUDE.md 並從磁碟重新讀取 | Claude Code: `/compact` 機制 |
| 跨會話記憶 | 前 N 行/ KB 自動載入，其餘按需加載 | Claude Code: auto memory（前 200 行或 25KB） |

**關鍵方法：不要把提示詞寫成一坨，要把它當成裝配系統。**

### 2.2 工具治理系統

| Harness 層 | 無人監督的具體方法 | 實例框架 |
|---|---|---|
| 工具發現 | 宣告式 DSL 定義工具，讓模型可發現 | MCP 協議（Claude）/ Codex SDK |
| 風險分級 | read / write / execute / critical 四級分級 | Claude: 權限層級 deny > ask > allow |
| 呼叫攔截 | 統一入參驗證、審批攔截、結果裁剪、錯誤歸類 | Codex CLI: guardian auto-review agent |

**關鍵方法：讓工具呼叫成為可治理系統，而不是一堆裸奔介面。**

### 2.3 安全與審批系統

| Harness 層 | 無人監督的具體方法 | 實例框架 |
|---|---|---|
| 三道防線 | 子程序管理 + 命令守衛 + 審批系統 | Claude: permission-first; Codex: sandbox-first |
| OS 級沙箱 | macOS Seatbelt, Linux bubblewrap+seccomp, Windows 原生沙箱 | Codex CLI: 三層 OS 沙箱 |
| 自動審查 | 檢查資料外洩、憑證探測、破壞性操作 | Codex CLI: guardian policy（高風險直接拒絕） |
| 狀態機約束 | Colang 定義完整互動路徑約束 | NVIDIA NeMo Guardrails（精度提升 20x） |

**關鍵方法：安全不能只靠模型自覺。真正的安全邊界必須落在執行時。**

> "Permission deny rules block Claude from even attempting to access restricted resources. Sandbox restrictions prevent Bash commands from reaching resources outside defined boundaries, even if a prompt injection bypasses Claude decision-making." — Anthropic Docs

### 2.4 回饋與狀態系統

| Harness 層 | 無人監督的具體方法 | 研究來源 |
|---|---|---|
| 系統事件翻譯 | 把系統內部發生的事翻譯成模型能消費的回饋語言（失敗原因、權限問題、輸出裁剪等） | mCell Harness 框架 |
| 自我反思記憶 | 每個動作後計算啟發式，檢測低效軌跡或幻覺，將反思存入工作記憶 | Reflexion (Shinn & Labash, 2023) |
| 思考-行動-觀察迴圈 | Thought → Action → Observation → repeat | ReAct (Yao et al., 2023) |
| 外部驗證 | 永遠不單靠 LLM 自我評估；領域特定任務需要外部工具驗證 | ChemCrow 研究發現 |

**關鍵方法：自我修正不會在一次 pass 中發生——它需要結構化的記憶系統儲存過去的失敗、反思和改進策略。**

### 2.5 熵管理系統

| Harness 層 | 無人監督的具體方法 |
|---|---|
| 規則過期 | 讓過期規則自動失效 |
| 上下文壓縮 | 定期壓縮長上下文 |
| 低價值歷史退出 | 讓低價值歷史退出上下文 |
| 知識沉澱 | 讓專案知識以可維護方式沉澱 |

**關鍵方法：沒有這層意識，再強的 agent 也會越跑越歪。**

---

## 3. 生產級 vs Demo 級：關鍵區別

| 維度 | 生產級（Claude Code / Codex CLI） | Demo 級 |
|---|---|---|
| 安全 | 深度防禦：權限 + 沙箱 + hooks/guardian 多層獨立 | 無沙箱/權限系統，agent 擁有使用者完整權限 |
| 狀態持久化 | 跨會話記憶，可從崩潰/壓縮/context 限制中恢復 | 所有狀態臨時性，每次會話從頭開始 |
| 上下文管理 | 層級式、路徑範圍、自動記憶 | 單一提示詞，無跨會話記憶 |
| 可觀測性 | 結構化遙測、OTel 匯出、審計日誌 | 無 |
| 恢復機制 | 優雅的 context 限制處理，重要 context 從磁碟重新注入 | context 溢出 = 狀態遺失 |
| 配置分層 | managed > CLI > local > project > user，清晰優先級 | 單一設定檔（如果有的話） |

**關鍵結論：Demo 和生產系統的界線不是功能多寡，而是可靠性、安全性和運維成熟度。**

---

## 4. 真正有效的方法總結

### 優先級排序（從參考文章 + 跨框架研究提取）

1. **先建環境，再追模型** — 環境是可複用資產，換模型能繼承。測試時故意使用老模型來驗證環境設計的成效。

2. **工具系統必須「系統化」** — 至少做到：可發現、可驗證、可分級、可攔截、可審計。

3. **上下文不要寫成一坨** — 把 prompt 當成裝配系統（6 層動態組裝），不要當成單文件。

4. **安全邊界必須在執行時** — 不要把安全寄託在提示詞上。雙層安全：行為層（權限）+ OS 強制層（沙箱），單一層不足。

5. **所有失敗都要可解釋** — 系統內部發生的事必須翻譯成模型能消費的回饋語言，否則模型無法做出下一步正確行動。

6. **長任務要有狀態與恢復機制** — 沒有狀態管理就沒有真正的持續執行。Claude Code 的 `/compact` 和 Codex CLI 的歷史持久化都是範例。

7. **定期做熵管理** — 規則、記憶、會話、文件會腐爛。不定期清理，系統就會慢慢失控。

8. **使用模擬測試替代人工監督** — 在生產前進行大規模模擬測試（參考 Waymo 20B 模擬里程 vs 20M 真實里程），覆蓋邊緣案例。

9. **外部驗證永遠必要** — LLM 無法評估自身領域特定任務的正確性（ChemCrow 發現）。需要搭配確定性驗證器 + LLM-as-a-Judge 的雙層評估。

10. **分層守門員架構** — IBM 四層分類：資料守門員 → 模型守門員 → 應用守門員 → 基礎設施守門員。

---

## 5. 來源

| 來源 | URL |
|---|---|
| 參考文章（原始簡體） | https://juejin.cn/post/7620226704209592360 |
| 參考文章（繁體翻譯） | https://codelove.tw/@tony/post/qO2Rda |
| 作者個人站點 | https://stack.mcell.top/blog/2026/harness-engineering-agent-engineering-explained |
| Lilian Weng Agent 綜述 | https://lilianweng.github.io/posts/2023-06-23-agent/ |
| Claude Code 文檔 | https://docs.anthropic.com/en/docs/claude-code/overview |
| OpenAI Codex CLI | https://github.com/openai/codex |
| Codex Enterprise Governance | https://developers.openai.com/codex/enterprise/governance |
| Guardrails AI / Snowglobe | https://www.guardrailsai.com/blog/intro |
| IBM AI Guardrails | https://www.ibm.com/think/topics/ai-guardrails |
| Wikipedia: Prompt Engineering | https://en.wikipedia.org/wiki/Prompt_engineering |
| LangChain: Context Engineering | https://blog.langchain.com/context-engineering-for-agents/ |
| Comet: Context Engineering | https://www.comet.com/site/blog/context-engineering/ |
| NeMo Guardrails Integration | https://www.guardrailsai.com/blog/nemoguardrails-integration |
| AI Guardrails Index | https://www.guardrailsai.com/blog/introducing-the-ai-guardrails-index |

---

*報告產生日期: 2026-04-28*
