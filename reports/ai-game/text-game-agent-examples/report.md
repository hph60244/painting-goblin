# 讓Code Agent根據需求文件製作文字遊戲 — 參考範例綜合報告

## 研究目標
尋找讓 Code Agent（AI 編碼代理）根據需求文件製作文字遊戲的參考範例、工具方法與最佳實踐。

---

## 一、實際專案範例

### 1. Google Gemma 2 文字冒險遊戲
- **連結**: [Build a Text-Based Adventure Game with Gemma 2](https://developers.googleblog.com/build-a-text-based-adventure-game-with-gemma-2/)
- **技術**: Gemma 2 + Python + Keras
- **架構**: 階段式遊戲循環 (`IStage` 介面)，每個階段有自己的 system prompt，搭配 `GemmaBot` wrapper 管理 AI 互動
- **特點**: 支援本地執行 (Keras/Kaggle) 或雲端部署 (Vertex AI)；附完整 Python 遊戲碼於 [GitHub](https://github.com/bebechien/gemma/tree/main/escape)

### 2. Google Gemini + Spring Boot 謀殺懸疑遊戲 (pratikIT95)
- **連結**: [Building an AI-Powered Text Adventure with Google Gemini](https://pratikit95.github.io/llm-text-adventure/)
- **技術**: Spring Boot (後端) + Angular (前端) + Google Gemini API
- **架構**: System instruction 定義了英屬印度時代的謀殺懸疑背景，強制輸出 JSON 格式讓前端解析 (`storyText`, `choices`, `isEnding`)
- **特點**: 隨機分配偵探角色、三幕結構、最多 20 次互動防止無限循環、UUID session 追蹤

### 3. DSPy + GPT-4o-mini 奇幻 RPG (Stanford)
- **連結**: [Building a Creative Text-Based AI Game](https://dspy.ai/tutorials/ai_text_game/)
- **技術**: DSPy (Stanford NLP) + GPT-4o-mini + Python (`rich`, `typer`)
- **架構**: 三個子模組 — `StoryGenerator`(場景)、`DialogueGenerator`(NPC)、`ActionResolver`(行動判定)
- **特點**: 角色養成系統 (力量/智力/魅力/潛行)、物品欄、存讀檔、三層邊界系統 (Always/Ask First/Never)

### 4. Nomad — 自主遊玩文字冒險的 AI Agent (ganileni)
- **連結**: [GitHub - ganileni/Nomad](https://github.com/ganileni/Nomad)
- **技術**: 多模型支援 (OpenAI/Anthropic/Google)、Python agent 框架
- **架構**: 分層架構 — Games Layer / Models Layer / Agents Layer / Utils Layer
- **特點**: 工具式 AI 互動 (function calling)、對話摘要管理長對話、session 持久化、每層級都有 `AGENTS.md`

---

## 二、適用的遊戲引擎與框架

| 類別 | 最佳選擇 |
|---|---|
| **腳本式敘事 (人類撰寫)** | Ink, Inform 7, TADS, Twine |
| **視覺小說 / 對話為主** | Ren'Py, Twine, Ink + Unity |
| **LLM 驅動動態敘事** | Python + OpenAI/Claude API + LangChain |
| **快速原型 / 非程式設計師** | Twine, Inky (Ink editor) |
| **遊戲引擎整合** | Ink (Unity/Unreal), Ren'Py (standalone) |
| **Agent 建構遊戲** | Python + 結構化 LLM 輸出 + 迭代程式碼生成 |

---

## 三、Prompt Engineering 模式

1. **結構化輸出解析** — 強制 LLM 輸出 JSON 格式的遊戲狀態 (`narration`, `state_changes`, `available_actions`)
2. **世界狀態注入** — 在 LLM context 外維護標準世界狀態，每次請求注入相關狀態
3. **約束執行** — System prompt 定義遊戲規則，chain-of-thought 處理謎題
4. **敘事一致性** — 維持 "story so far" buffer，context 滿時使用摘要
5. **多代理架構** — Game Master / World Model / NPC / Evaluator 各司其職

---

## 四、需求文件最佳實踐

### 建議的文件結構

```
# Game: [Title]
## Identity & Genre
## Tech Stack & Constraints
## Core MVP Mechanics (ordered by priority)
├── Fight system
├── Inventory
├── Dialogue
└── Saving/Loading
## Expansion Features
## Code Conventions & Architecture
## Example Play Session
## Reference Files
```

### 關鍵原則 (來自 Anthropic/OpenAI/Cursor/Aider)

- **保持簡單** — Anthropic 研究指出「最成功的 implementation 使用的是簡單、可組合的模式」
- **分層規格** — 先 MVP，再擴展功能；避免一次性給巨大 spec
- **明確的邊界** — 定義 Always / Ask First / Never 三層系統
- **使用非目標 (Non-goals)** — AI 無法從省略推斷範圍，需明確寫出「不要做的事」
- **迭代開發** — 從 broad spec 開始，透過對話逐步細化
- **Evaluator-Optimizer 循環** — 生成 → 測試 → 評論 → 重新生成
- **使用 `.cursor/rules/*.mdc` / `AGENTS.md` / `.github/copilot-instructions.md`** — 這些是事實上的「需求文件」標準格式

### 常見的 Agent 工作流模式 (Anthropic 分類)

| 模式 | 適用場景 |
|---|---|
| **Prompt Chaining** | 固定子任務的順序處理 |
| **Orchestrator-Workers** | 多檔案遊戲程式碼生成 |
| **Evaluator-Optimizer** | 迭代打磨遊戲體驗 |
| **Autonomous Agent** | 開放式遊戲開發 |

---

## 五、結論與建議

要讓 Code Agent 根據需求文件製作文字遊戲，建議採用的方法：

1. **選擇技術棧**: Python + LLM API (動態敘事) 或 Ink/Twine (腳本式敘事)
2. **撰寫分層 Spec**: 使用上述文件結構，包含身份/類型 → 技術棧 → MVP 功能 → 擴展功能 → 程式碼慣例 → 範例遊玩
3. **使用 Agent 設定檔**: `AGENTS.md` 或 `.cursor/rules/*.mdc` 定義 agent 的角色與慣例
4. **迭代開發**: 先生成可玩的 MVP，再透過 Evaluator-Optimizer 循環逐步改善
5. **結構化輸出**: 要求 LLM 輸出 JSON 格式的遊戲狀態，便於程式解析

### 參考來源

- https://developers.googleblog.com/build-a-text-based-adventure-game-with-gemma-2/
- https://pratikit95.github.io/llm-text-adventure/
- https://dspy.ai/tutorials/ai_text_game/
- https://github.com/ganileni/Nomad
- https://addyosmani.com/blog/good-spec/
- https://www.anthropic.com/engineering/building-effective-agents
- https://platform.openai.com/docs/guides/prompt-engineering
- https://docs.cursor.com/context/rules-for-ai
- https://aider.chat/docs/repomap.html
- https://codex.best/guides/agents-md
