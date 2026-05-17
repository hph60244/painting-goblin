# Code Agent 根據需求文件製作 Godot 遊戲 — 研究報告

## 核心問題
如何讓 Code Agent（如 Claude Code, OpenCode）根據需求文件自動製作 Godot 遊戲？

---

## 關鍵發現

### 1. 基礎設施已就緒

| 項目 | 說明 | Star數 | 連結 |
|------|------|--------|------|
| **godot-lsp-stdio-bridge** | stdio↔TCP橋接，讓AI代理（OpenCode, Claude Code）能與Godot的GDScript LSP通訊，獲得程式碼智能（診斷、跳轉、補全） | 16 | [GitHub](https://github.com/code-xhyun/godot-lsp-stdio-bridge) |
| **Godot-Skills** | 12個技能模組，為OpenCode/Claude Code提供GDScript語法、TSCN格式、場景操作等Godot專業知識 | 3 | [GitHub](https://github.com/fenixnix/Godot-Skills) |
| **Godot AI Chat** | 編輯器內AI助手，ReAct代理，支援多供應商，可自動呼叫工具（場景編輯、檔案操作、程式碼撰寫） | 18 | [GitHub](https://github.com/snougo/Godot-AI-Chat) |

### 2. 從需求文件到遊戲的可行模式

目前最成熟的模式是：

```
需求文件/規格書 (Markdown/Google Doc)
  → AI提取需求
  → AI生成專案結構 + 所有源碼
  → AI建立建置/執行腳本
  → 人工測試並找出差距
  → AI迭代修復問題
  → 可運作的遊戲原型
```

**參考文獻**：
- [Gemini Code Assist: 從需求到原型](https://cloud.google.com/blog/topics/developers-practitioners/from-requirements-to-prototype-with-gemini-code-assist) — 最接近的正式工作流程
- [Augment Code: 規格驅動的AI程式碼生成（多代理架構）](https://www.augmentcode.com/guides/spec-driven-ai-code-generation-with-multi-agent-systems)
- Claude Code 生成2D遊戲的YouTube教學（9萬+觀看）

### 3. 代理架構選擇

| 方式 | 優點 | 缺點 |
|------|------|------|
| **單一代理** (Claude Code, OpenCode) | 設定簡單，適合小型遊戲 | 上下文限制，無法平行工作，難以驗證是否符合規格 |
| **多代理** (Coordinator-Implementor-Verifier) | 規格驗證，平行生成，可處理更大範圍 | 設定更複雜，成本更高 |

### 4. 現有生態系統缺口

- ❌ **尚無** 從「遊戲設計文件 → Godot專案」的完整工具或良好記錄的工作流程
- ❌ 沒有框架原生理解 GDScript/Godot場景檔案 (.tscn) 作為規格生成目標
- ✅ Claude Code 是目前最適合的代理（已被 GameMaker 正式整合）
- ✅ 迭代式開發（產生→測試→修復→重複）是所有成功案例的共同模式

---

## 建議行動方案

### 方案 A：使用 OpenCode + Godot-Skills + LSP Bridge

```
需求文件 (MD)
  → OpenCode 載入 Godot-Skills 技能
  → 透過 godot-lsp-stdio-bridge 連接 Godot LSP
  → 迭代生成 GDScript 程式碼與場景
```

**已就緒的元件**：
- OpenCode（已安裝）
- godot-lsp-stdio-bridge（需安裝）
- Godot-Skills（可直接引用）

### 方案 B：建立「規格→Godot」管道

參考 Gemini Code Assist 的模式，建立以下流程：
1. 撰寫結構化的遊戲設計文件（Markdown）
2. 設計 `.cursorrules` / `CLAUDE.md` 或 OpenCode Agent 設定，讓代理理解：
   - Godot 專案結構慣例
   - GDScript 最佳實踐
   - TSCN 場景檔案格式
3. 代理讀取需求文件 → 產生完整專案
4. 人工啟動 Godot 測試 → 回饋給代理迭代

### 方案 C：善用 Godot AI Chat 插件

直接在 Godot 編輯器內整合 AI 助手，提供：
- 場景編輯（新增/修改節點）
- 程式碼生成
- 檔案操作
- 多供應商支援（OpenAI, Gemini, Claude）

---

## 結論

**目前最務實的路徑**是方案 A：以 OpenCode 為核心，搭配 Godot-Skills 提供領域知識，並透過 godot-lsp-stdio-bridge 獲得 Godot LSP 支援。這三項工具皆為開源且可直接整合。

**關鍵提醒**：
- 所有成功案例都強調**迭代**的重要性，單次生成很少完美
- 規格文件越結構化（包含資料模型、場景結構、遊戲機制），輸出品質越高
- Godot 社群對 AI 生成程式碼持謹慎態度，生成後需要人工審查
