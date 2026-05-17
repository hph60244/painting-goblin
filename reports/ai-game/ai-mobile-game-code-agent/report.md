# AI Code Agent 製作手機遊戲：研究報告

## 研究問題
尋找讓 Code Agent 根據需求文件製作手機遊戲的參考範例

## 執行摘要

截至 2026 年 5 月，**尚無成熟、公開的端到端案例**顯示有人將完整的需求規格文件餵給 AI Code Agent，並成功產出已上架的行動遊戲。然而，多種工具與工作流程已能將「文字描述 → 可遊玩遊戲」的過程大幅自動化，尤其適合簡單的 2D 網頁/手機遊戲原型。

---

## 一、可行的 AI Code Agent 方案

| Agent | 適合遊戲開發的理由 | 限制 |
|-------|-------------------|------|
| **Claude Code** | 深度多檔案推理、自主執行任務、支援 Unity (via Glade MCP) | 需手動設定手機建置流程 |
| **GitHub Copilot (Agent Mode)** | 與 GitHub 整合、Plan agent 可先分析再實作、支援 CLI/IDE/GitHub 三階段流程 | 需搭配遊戲引擎使用 |
| **Cursor** | AI-native IDE、agent mode、MCP 支援 | 同上 |
| **Bolt (bolt.new)** | 瀏覽器內即可生成全端應用、即時預覽 | 主要產出 web app，非原生手機 |
| **Replit Agent** | 可生成全端應用並部署 | 主要針對 web |

**推薦工作流程**（改編自 GitHub Blog, Feb 2026）：
1. 描述遊戲意圖（intent），不要從 scaffolding 開始
2. 讓 Agent 分析架構並提出模組化方案
3. 定義模組邊界（遊戲邏輯、UI、資料、音效等）
4. 迭代實作功能：架構評估 → 實作 → 測試 → 文件
5. 審查所有 AI 生成的程式碼（尤其安全性）

---

## 二、專用工具與平台

| 工具 | 輸入方式 | 輸出 | 手機匯出 |
|------|---------|------|---------|
| **Rosebud AI** | 自然語言描述遊戲 | 可遊玩 2D/3D 遊戲 | 行動版網頁 |
| **Buildbox 4** | 自然語言提示（場景、行為、特效） | 完整遊戲 + AI 生成的場景/邏輯/素材 | Android/iOS |
| **GameMaker + Claude Code** | 需求 + AI 輔助開發 | GameMaker 專案 | Android/iOS/HTML5 |
| **Unity + Glade MCP** | Claude Code/Cursor 直接操作 Unity Editor | Unity 專案 | Android/iOS |
| **GitHub Spark** | 自然語言描述 | TypeScript/React 全端應用 | 網頁 |

**關鍵發現**：目前沒有任何工具能直接解析結構化的需求文件（Game Design Document）並產出完整手機遊戲。所有工具都是使用**對話式提示**（conversational prompting），而非結構化文件解析。

---

## 三、案例研究

### 成功案例（簡單遊戲）
- **HTML5 Canvas 遊戲**：Tetris、Snake、Pong、迷宮遊戲、問答遊戲 — AI 表現最佳
- **GitHub 上約 4,100 個** tagged「AI generated game」的 repo，多為小型專案
- **GameMaker 官方整合 Claude Code**（2026 年 4 月）— 遊戲引擎開始原生支援 AI 輔助

### 參考專案
| 專案 | 說明 | 網址 |
|------|------|------|
| Glade MCP for Unity | 讓 Claude Code/Cursor 直接操控 Unity Editor | github.com/Glade-tool/glade-mcp-unity |
| cosmoart/quiz-game | AI 生成題目的問答遊戲（NextJS + Cohere） | github.com/cosmoart/quiz-game |
| Minoxds/prompt-to-puzzle | 從文字提示生成「找不同」遊戲 | github.com/Minoxds/prompt-to-puzzle |

### 尚未成功的領域
- **已上架 App Store/Google Play 的遊戲** — 未發現任何案例
- **多場景手機遊戲**（含導航、存檔、觸控操作）
- **即時連線/多人遊戲**
- **複雜物理引擎或客製渲染**
- **生產級素材管線**

---

## 四、需求文件最佳實踐（給 Code Agent 用）

### 文件結構建議
將需求文件分為以下區塊，逐區塊餵給 Agent：

1. **高層概念**：遊戲類型、視角、平台 target
2. **遊戲機制**：核心玩法、規則、勝利條件
3. **UI/UX**：畫面配置、觸控操作方式
4. **資料模型**：分數、存檔、設定
5. **素材需求**：圖像、音效、字型（AI 程式生成 ≠ AI 素材生成）
6. **技術限制**：效能目標、離線支援、第三方 SDK

### Prompt 模式推薦

| 模式 | 範例 | 使用時機 |
|------|------|---------|
| Analyze first | "Analyze this spec and propose architecture..." | 複雜專案起始 |
| Scaffold + iterate | "Create minimal [game type] with [mechanics]" | 全新專案 |
| Incremental execution | "Implement steps 1-3 only. Stop before [risky part]" | 安全迭代 |

---

## 五、具體建議：如何用 Code Agent 製作手機遊戲

### 方案 A：HTML5 網頁遊戲（最快入門）
- **工具**：Claude Code / Cursor + Phaser.js
- **流程**：寫需求文件 → Agent 生成遊戲程式碼 → 用 Capacitor/Cordova 包成 Android/iOS App
- **優點**：AI 對 JavaScript/TypeScript 支援最佳、即時預覽、迭代快速
- **限制**：非原生效能、較難使用平台特定功能

### 方案 B：Unity 遊戲（最完整）
- **工具**：Claude Code + Glade MCP for Unity
- **流程**：需求文件 → Agent 透過 MCP 直接操作 Unity Editor → 產出 Unity 專案 → 匯出 Android/iOS
- **優點**：完整的行動遊戲功能支援、大量資源
- **限制**：需熟悉 Unity、C# 程式碼品質依賴 prompt 品質

### 方案 C：GameMaker（折衷方案）
- **工具**：GameMaker + Claude Code（官方整合）
- **流程**：需求文件 → Claude Code 輔助開發 GML 程式碼 → GameMaker 匯出
- **優點**：官方支援、2D 遊戲專用、匯出選項豐富
- **限制**：較少 AI 輔助開發的社群資源

### 方案 D：Buildbox 4（無程式碼）
- **工具**：Buildbox 4 AI
- **流程**：自然語言描述遊戲 → AI 自動生成場景/邏輯/素材 → 匯出
- **優點**：完全不用寫程式、最快產出
- **限制**：客製化程度有限、較難處理複雜邏輯

---

## 六、風險與注意事項

1. **安全性**：AI 常忽略認證與授權（XSS、未驗證 API endpoints）
2. **資產管線**：程式碼生成 ≠ 素材生成；美術、音效需另外處理
3. **除錯困難**：AI 生成的程式碼可能有難以追蹤的細微錯誤
4. **範疇蔓延**：無明確規格時，AI 會讓遊戲功能無限擴張
5. **手機特定挑戰**：觸控輸入、多螢幕尺寸、效能優化、App Store 合規

---

## 七、結論

1. **沒有現成的「需求文件 → 手機遊戲」的完整參考範例**，但相關工具生態已成熟到可以自建管線
2. 最務實的做法：**先寫結構化需求文件 → 用 Claude Code / Cursor 搭配 Phaser.js 或 Unity 迭代生成 → 再用 Capacitor 或 Unity 匯出匯出行動版本**
3. **簡單的 2D 遊戲**（如拼圖、問答、跑酷）是 AI 目前最能勝任的範圍
4. 預計 2026–2027 年，隨著 GameMaker + Claude Code、Unity + Glade MCP 等整合成熟，將出現更多端到端的 AI 生成手機遊戲案例

---

## 參考資料

| 來源 | 網址 |
|------|------|
| VS Code Copilot Docs | https://code.visualstudio.com/docs/copilot/overview |
| Anthropic Claude Code | https://claude.ai/code |
| Cursor Docs | https://docs.cursor.com/getting-started/overview |
| GitHub Blog - Agentic Capabilities | https://github.blog/ai-and-ml/github-copilot/how-to-maximize-github-copilots-agentic-capabilities/ |
| GitHub Blog - Idea to PR | https://github.blog/ai-and-ml/github-copilot/from-idea-to-pull-request-a-practical-guide-to-building-with-github-copilot-cli/ |
| Rosebud AI | https://rosebud.ai |
| Buildbox 4 | https://www.buildbox.com |
| Glade MCP Unity | https://github.com/Glade-tool/glade-mcp-unity |
| GameMaker + Claude Code | https://www.gamedeveloper.com/production/gamemaker-incorporates-claude-code-to-enable-ai-assisted-workflows |
| GitHub Spark | https://github.com/features/spark |
| Hacker News - Security Discussion | https://news.ycombinator.com/item?id=42914072 |
