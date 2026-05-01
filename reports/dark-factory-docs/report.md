# 研究報告：Dark Factory 模式對文件完備度的要求

## 執行摘要

本報告研究核心問題：**需要提供多充分的文件，才能讓單一 Code Agent 順利套用 dark factory 模式？**

答案是：**取決於任務複雜度，但核心原則一致 — 文件（spec）必須足以驅動 Seed → Loop → Fuel 自主循環，而驗證機制（validation harness）是其中最關鍵的要素。**

| 任務複雜度 | 所需文件規模 | 人類角色 | 自主性等級 |
|-----------|------------|---------|-----------|
| 簡單（如加入單元測試） | 無需額外文件，既有的程式碼即是 spec | 完全無需介入 | Level 5 |
| 中等（如加入 CRUD 端點） | 1-2 句描述 + 介面合約 | 低度審查或自動驗證 | Level 4-5 |
| 複雜（如實作計費系統） | Given-When-Then 驗收標準 + 介面合約 + 3+ 範例 | 人類寫 spec，AI 自主執行 | Level 4 |
| 系統級/綠地專案 | ~5,000-10,000 行結構化 spec（DOT 圖、schema、scenario） | 人類作為 spec 作者 + 結果驗收者 | Level 3-4 |

---

## 1. Dark Factory 概念概述

### 1.1 定義

「Dark Factory」（黑燈工廠）源於製造業 — 日本 Fanuc Robotics 自 2003 年開始運作的無人生產線。2025 年底被 AI 程式開發社群借用，指**完全自主的軟體開發流程，人類不需要（也不被允許）參與程式碼生成迴圈**。

### 1.2 Dan Shapiro 的 AI 程式開發自主性五層級

| 層級 | 名稱 | 描述 |
|------|------|------|
| 0 | 無自動化 | 純手寫程式碼 |
| 1 |  spicy autocomplete | Copilot 輔助完成 |
| 2 | 配對程式設計 | AI 為 junior 同事，人類主導 |
| 3 | 安全駕駛 | AI 為 senior 開發者，人類審查 diff |
| 4 | Robotaxi | 人類寫 spec，離開 12 小時，回來檢查測試 |
| 5 | **Dark Factory** | **黑盒：spec 進、軟體出，沒有人類閱讀或審查程式碼** |

來源: https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/

### 1.3 StrongDM 軟體工廠的核心原則

Justin McCarthy (StrongDM CTO) 於 2025 年 7 月成立 AI 團隊，訂下兩條鐵則：
- **程式碼不得由人類撰寫**
- **程式碼不得由人類審查**

核心循環：
1. **Seed**：從 spec 開始（PRD、截圖、既有程式庫）
2. **Loop**：驗證機制 → 反饋 → 重複直到 holdout scenarios 通過
3. **Fuel**：投入更多 token，將每個障礙轉化為模型可理解的表示

來源: https://factory.strongdm.ai/principles

---

## 2. 不同任務複雜度所需文件完備度

### 2.1 簡單 / 模板任務（如 "加入單元測試"、"補上 docstring"）

**最低可行文件：** 無。既有的程式碼即為 spec。

AI agent 在既有 repo 中可以從周圍檔案推斷結構。Copilot 風格的 inline completion 可以在無需任何 spec 文件的情況下處理此層級。

### 2.2 中等複雜度任務（如 "加入 CRUD 端點"、"建立工具函式"）

**最低可行文件：**
- 1-2 句自然語言描述
- 函式簽名或 API 合約

AI agent 依賴：
- 既有程式碼慣例（convention over configuration）
- 型別簽名 / 介面
- 框架慣例

### 2.3 中等複雜度任務（如 "實作計費系統整合"、"加入搜尋與過濾"）

**最低可行文件：**
- Given-When-Then 格式的驗收標準（可執行 spec）
- 介面合約（輸入/輸出 schema）
- 邊界案例列舉
- 3+ 個具體範例流程

關鍵發現：**端到端 scenario（稱為 "holdout scenarios"）存放在程式庫外部，是主要的驗證機制。** 這些不是單元測試，而是由 LLM-as-judge 驗證的使用者層級行為描述。

### 2.4 複雜多步驟任務（如 "加入多 provider 的 OAuth2"、"實作分散式任務佇列"）

**最低可行文件：**
- 架構決策記錄 (ADR) 或設計文件
- 關鍵路徑的序列圖或流程圖
- 合約測試 + scenario-based 驗收測試
- 錯誤處理矩陣
- 5+ 個具體範例流程

Key insight: **機器可讀的 spec（DOT 圖、JSON schema、OpenAPI spec）比散文文件更有效。**

### 2.5 系統級 / 綠地專案（如 "從頭建立 SaaS 平台"）

**最低可行文件：**
- PRD 或同等文件
- 架構規格（元件圖、資料流程、部署模型）
- 資料模型 / schema 定義
- 完整的驗收 scenarios（20-100+）
- 設計限制與技術選擇
- 非功能需求（效能、安全、合規）

StrongDM attractor pattern 顯示：**~5,700 行自然語言 spec**（以 DOT pipeline 圖組織）足以讓 4 個獨立團隊收斂到相同的 3 層架構。

---

## 3. 可執行 Spec vs 自然語言 Spec

| 類型 | 精確度 | AI 可解讀性 | 撰寫成本 | 最佳用途 |
|------|--------|------------|---------|---------|
| 自然語言（散文） | 低 | 中 | 低 | 背景脈絡、意圖、理由 |
| 結構化 NL（Given-When-Then） | 中 | 高 | 中 | 行為需求 |
| 可執行測試（單元） | 高 | 很高 | 中高 | 實作驗證 |
| 可執行測試（整合/E2E） | 很高 | 很高 | 高 | 系統層級驗證 |
| 形式化 spec（DOT、OpenAPI） | 很高 | 很高 | 高 | 架構、合約 |
| Holdout scenarios（LLM-as-judge） | 中高 | 高 | 中 | 自主驗證循環 |

### 關鍵洞察：可執行 spec 是驗證者，而非生成者

驗證機制是最關鍵的元件。Agent 可以從鬆散的自然語言 spec 生成程式碼，但需要**可執行的驗證**來知道何時完成。這就是收斂循環。

### Self-Debugging 模式

來源: arXiv:2304.05128 (Chen et al., Google Research)

Self-Debugging 教 LLM 自行除錯：
1. 程式碼解釋（橡皮鴨除錯）
2. 執行反饋（執行程式碼並觀察結果）
3. Few-shot debugging 示範

結果：程式碼生成基準測試準確率提升 +12%，最難問題提升 +9%

---

## 4. 文件完備度判斷準則

### 4.1 "Would the Code Pass" 測試

一份 spec 在以下情況算是足夠完備：給定 spec 且無其他資訊，人類開發者可以在不提出澄清問題的情況下產出通過的實作。

### 4.2 "Holdout Scenario" 準則

一份 spec 在以下情況算是足夠完備：團隊可以寫出 3-10 個 holdout scenarios，且最終實作必須滿足這些 scenarios，而 agent 無法作弊通過。

### 4.3 Three Cs 收斂原則

Alistair Cockburn 的格言 — 「使用者故事是對話的承諾」— 在自主 agent 的情境下反向適用。由於**沒有**對話，spec 必須自成體系：
- **Card** → 結構化 spec 文件
- **Conversation** → 必須預先編碼為替代方案/邊界案例
- **Confirmation** → Holdout scenarios + 可執行測試

### 4.4 Dorodango 原則

> "The pipeline files are the durable artifact. The factory code is dorodango — polish it, throw it away, rebuild from spec."
> — 2389 Research, https://2389.ai/posts/the-dark-factory-is-a-dot-file/

文件完備度不是關於記錄生成的程式碼，而是關於記錄**規格和 pipeline**，以便程式碼可以重新生成。

---

## 5. 各 Spec 元素的需求對照表

| Spec 元素 | 簡單任務 | 中等任務 | 複雜任務 | 綠地專案 |
|-----------|---------|---------|---------|---------|
| 1 句描述 | 必要 | 必要 | 必要 | 不適用（太模糊） |
| 驗收標準 (Given-When-Then) | 有幫助 | 必要 | 必要 | 必要 |
| 介面合約 (schema/type) | 有幫助 | 必要 | 必要 | 必要 |
| 具體範例+資料 | 不需要 | 必要 (3+) | 必要 (5+) | 必要 (20+) |
| 邊界案例列舉 | 不需要 | 必要 | 必要 | 必要 |
| 錯誤處理矩陣 | 不需要 | 有幫助 | 必要 | 必要 |
| 架構/設計文件 | 不需要 | 不需要 | 必要 | 必要 |
| 資料模型 | 不需要 | 有幫助 | 必要 | 必要 |
| Holdout scenarios | 不需要 | 必要 | 必要 | 必要 |
| 非功能需求 | 不需要 | 不需要 | 有幫助 | 必要 |

---

## 6. painting-goblin 在 Dark Factory 生態系中的定位

### 6.1 現有定位

painting-goblin 的檔案系統任務佇列（FSMQ）模式是 dark factory 概念的**極簡務實實作**：

| 維度 | painting-goblin (FSMQ) | DOT Pipeline (Fabro/Kilroy) | Claude Code Routines | Devin |
|------|-----------------------|-----------------------------|---------------------|-------|
| **佇列** | 檔案系統目錄 | DOT 圖節點 | 雲端後端 | 專有 |
| **任務格式** | `.md` 檔案 | `*.dot` 圖形檔案 | 提示 + repo | 自然語言 |
| **協調器** | Python（無 LLM 呼叫） | LLM + 工具節點 | 雲端服務 | 專有 |
| **排程** | APScheduler（本機 cron） | 不適用（觸發式） | 雲端 cron/API/GitHub | 不適用 |
| **失敗處理** | 移至 `failed/` 目錄 | Checkpoint + 重試 | Session 重播 | 未知 |
| **人類角色** | 撰寫 `.md` 任務檔案 | 撰寫 DOT spec | 撰寫提示/排程 | Issue 作者 |

### 6.2 獨特優勢

1. **最低基礎設施負擔**：無雲端、無資料庫、無訊息代理 — 只需檔案系統
2. **最高可移植性**：可在任何有 Python + 任何 AI CLI 工具的 OS 上執行
3. **簡單的失敗模型**：`done/failed` 目錄是優雅、可檢查的狀態儲存
4. **無 LLM 廠商鎖定**：協調器從不直接呼叫 LLM

### 6.3 可擴展方向

1. **DOT pipeline 整合**：支援 `.dot` 檔案定義多步驟 pipeline
2. **任務依賴**：DAG 基礎的任務排程
3. **自我驗證**：類似 StrongDM 的 scenarios 或 OctopusGarden 的 LLM-as-judge
4. **檢查點**：中間狀態保存
5. **單 agent 內的平行任務**：為大型專案衍生子任務

---

## 7. 結論與建議

### 7.1 Dark Factory 模式的文件需求總結

**核心答案：文件完備度取決於任務複雜度，但有一條普遍適用的規則。**

**普遍規則：** Spec 必須完備到 agent 可以自主執行 **Seed → Loop → Fuel** 循環。最關鍵的元素是**驗證機制（validation harness）** — 一種不需要人類判斷即可自動判定 pass/fail 的方式。Holdout scenarios + LLM-as-judge 是目前的最佳實踐。

### 7.2 對 painting-goblin 的實際建議

如果要在 painting-goblin 中實現 dark factory 模式（Level 4-5）：

1. **對於中等以下任務**：單個 `.md` 檔案搭配 Given-When-Then 驗收標準就足夠，無需額外基礎設施
2. **對於複雜任務**：需要加入驗證機制（執行測試或 LLM-as-judge）和 holdout scenarios
3. **對於綠地專案**：需要外部 spec 存放區（類似 StrongDM 的 spec repo）和完整的 pipeline 定義
4. **關鍵瓶頸**：spec 撰寫已從 coding 的瓶頸轉移到 specification。正如 Dan Shapiro 所說：「你是 PM。寫 spec、辯論 spec、離開 12 小時、回來檢查測試。」

### 7.3 已知挑戰

1. **程式碼可維護性**：dark factory 生成的程式碼可以運作，但人類通常不想維護
2. **合規性**：ISO 27001、SOC 2 對完全 AI 生成的程式碼是未解決的問題
3. **除錯困難**：LLM 服務中斷會阻斷整個 pipeline；生成的程式碼不透明
4. **獎勵駭客 (reward hacking)**：Agent 會作弊通過測試；holdout scenarios 只能部分緩解
5. **Token 經濟學**：「投入更多 token」的原則有真實的貨幣成本

---

## 資料來源

1. https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/
2. https://factory.strongdm.ai/
3. https://factory.strongdm.ai/principles
4. https://factory.strongdm.ai/techniques
5. https://2389.ai/posts/the-dark-factory-is-a-dot-file/
6. https://sotaverified.org/blog/improving-autoresearch-dark-factory-harness
7. https://github.com/fabro-sh/fabro
8. https://github.com/danshapiro/kilroy
9. https://github.com/foundatron/octopusgarden
10. https://docs.anthropic.com/en/docs/claude-code/sub-agents
11. https://docs.anthropic.com/en/docs/claude-code/agent-teams
12. https://docs.anthropic.com/en/docs/claude-code/routines
13. https://www.cognition.ai/blog/introducing-devin
14. https://arxiv.org/abs/2304.05128 — "Teaching Large Language Models to Self-Debug"
15. https://en.wikipedia.org/wiki/Specification-driven_development
16. https://en.wikipedia.org/wiki/Behavior-driven_development
17. https://www.danshapiro.com/blog/2026/02/you-dont-write-the-code/
18. https://news.ycombinator.com/item?id=47920020
