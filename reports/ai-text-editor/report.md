# 讓 Code Agent 根據需求文件製作文字編輯器 — 參考範例與方法

## 研究問題
尋找讓 Code Agent（AI 程式碼代理）根據需求文件（spec/PRD）製作文字編輯器的參考範例、專案與工作流程。

---

## 一、最相關的參考範例

### 1. Anthropic Autonomous Coding Agent（最推薦）
- **倉庫:** `anthropics/claude-quickstarts`（16.4k stars）
- **網址:** https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding
- **工作流程:**
  1. **Initializer Agent** 讀取 `app_spec.txt`，生成 `feature_list.json`（含測試案例），建立專案結構並初始化 git
  2. **Coding Agent** 逐個實現功能，通過測試後標記為完成
  3. 進度會透過 `feature_list.json` 和 git commit 在 session 之間持久化
- **為何最適合：** 這是唯一公開的、從規格檔（spec）自動構建完整應用的開源參考實現，直接對應「根據需求文件製作文字編輯器」的場景。每個編碼迭代約 5-15 分鐘，支援包含 rich UI 的 Web 應用。

### 2. Anthropic "Building Effective Agents" Cookbook
- **倉庫:** `anthropics/claude-cookbooks`（41.9k stars）
- **網址:** https://github.com/anthropics/claude-cookbooks/tree/main/patterns/agents
- **適用的代理模式:**
  - **Prompt Chaining** — 逐步呼叫工具進行增量編輯
  - **Orchestrator-Subagents** — 將語法高亮、自動補全等子任務委派給子代理
  - **Evaluator-Optimizer** — 對生成的編輯器程式碼進行迭代優化
- **為何重要：** 提供了構建文字編輯器時所需的代理架構模式參考。

---

## 二、AI 代理構建文字編輯器的主要工具平台

### Claude Code（Anthropic）
- "If you can describe it, you can build it." — 支援專案級別的多檔案生成與修改
- 成功案例：Stripe（10,000 行遷移 4 天完成）、Wiz（50,000 行遷移 20 小時）
- **適用方式：** 將需求文件（spec.md）作為 prompt 輸入，Claude Code 會讀取、規劃、生成整個專案

### Cursor（Anysphere）
- 35% 的內部 PR 由自主雲端代理建立；代理使用量年增 15 倍
- "Our designer built an operating system with Cursor" 影片證明非工程師也能構建完整應用
- **適用方式：** 使用 Agent Composer 2，讓自主代理根據 spec 從零構建

### GitHub Copilot Agent Mode
- 支援分配任務給 Copilot、Claude、OpenAI Codex 等多種代理
- 代理可自主規劃、探索、執行，跨 IDE/CLI/GitHub.com 工作

### GitHub Spark
- "Describe → Generate → Deploy" 從自然語言生成完整全端應用
- 基於 TypeScript/React，支援一鍵部署

### Lovable（前身為 GPT Engineer）
- 已達 $100M ARR，從自然語言 prompt 構建全端應用
- 支援 Agent Mode 自主規劃與構建功能，已整合 React/TypeScript/Tailwind

---

## 三、Spec-to-Code 工作流程模式

### 模式 1：Smol Developer 三步驟管線（12.2k stars）
1. **Plan** — AI 讀取 spec，生成 `shared_dependencies.md`（定義跨檔案合約）
2. **Specify** — AI 列出所有需要的檔案路徑
3. **Generate** — 為每個檔案生成程式碼

**關鍵創新：** 中間的 shared_dependencies 步驟解決了「跨檔案一致性」這個一次性生成的最大失敗模式。

### 模式 2：GPT Engineer 迭代循環（55.2k stars，已歸檔）
1. 撰寫 `prompt` 檔（spec）
2. 執行 `gpte <project>` — AI 生成整個程式碼庫
3. 審查輸出，執行並找出錯誤
4. 修改 `prompt` 檔加入改進說明
5. 執行 `gpte <project> -i` — AI 改進現有程式碼
6. 重複

### 模式 3：Aider 的程式碼庫感知模式（44.2k stars）
- 使用 repomap 理解整個程式碼庫
- 對相關檔案進行精確修改
- 自動 lint、測試、git commit

### 最佳實踐總結
- **Spec 是控制面：** 最有效的方式是「編輯 spec，重新生成程式碼」
- **中間規劃層：** shared_dependencies.md 之類的中間步驟顯著提升生成品質
- **錯誤回饋循環：** 將執行錯誤自動回饋給 AI 進行自我修復
- **Markdown 是通用 spec 格式：** 可混合自然語言和程式碼區塊

---

## 四、給 painting-goblin 專案的實作建議

### 建議架構（參考 Anthropic Autonomous Coding Agent）

```
需求檔案（spec.md / requirements.md）
        │
        ▼
Initializer Agent ─→ feature_list.json（含測試案例）
        │
        ▼
Coding Agent ─→ 逐個實現功能 → 測試驗證 → git commit
        │
        ▼
Review & Iterate（人類審查 → 修改需求 → 重新生成）
```

### 技術棧建議（基於研究成果）
| 層級 | 建議技術 | 原因 |
|------|----------|------|
| **核心編輯器** | CodeMirror 6 / Monaco Editor | 最成熟的 Web 文字編輯器框架 |
| **框架** | React + TypeScript | 所有 AI agent 平台最佳支援 |
| **代理工具** | Claude Code SDK / Cursor | 支援 spec-to-code 工作流程 |
| **格式** | Markdown spec file | 通用標準，AI 支援度最高 |

### 可直接採用的開源參考
1. **Anthropic Autonomous Coding Agent** — 完整的 spec-to-app 參考實現（https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding）
2. **Agent Cookbook 模式** — 代理架構模式參考（https://github.com/anthropics/claude-cookbooks/tree/main/patterns/agents）
3. **Smol Developer 的 shared_dependencies 模式** — 跨檔案一致性方案（https://github.com/smol-ai/developer）

---

## 五、已知限制與注意事項

1. **無公開的文字編輯器專用案例：** 雖然 AI 代理構建 GUI 應用的能力已被多方驗證，但尚無廣為人知的「AI 從 spec 構建文字編輯器」的公開案例
2. **安全性至關重要：** Anthropic 的自主編碼代理使用 OS 級沙箱、檔案系統限制和指令白名單
3. **人類仍需參與：** 目前最佳實踐是「人類負責架構與審查，AI 負責實現」的分工模式

---

## 資料來源

- Anthropic Claude Code: https://www.anthropic.com/product/claude-code
- Cursor Third Era: https://www.cursor.com/blog/third-era
- GitHub Spark: https://github.com/features/spark
- Anthropic Autonomous Coding Agent: https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding
- Anthropic Agent Cookbook: https://github.com/anthropics/claude-cookbooks/tree/main/patterns/agents
- GPT Engineer: https://github.com/AntonOsika/gpt-engineer
- Smol Developer: https://github.com/smol-ai/developer
- Aider: https://github.com/Aider-AI/aider
- Cursor: https://www.cursor.com/
- Lovable: https://www.lovable.dev/blog
