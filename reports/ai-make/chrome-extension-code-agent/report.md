# Code Agent 自動生成 Chrome 擴充功能 — 研究報告

## 摘要

本報告總結如何讓 Code Agent (AI 編碼代理) 根據需求文件自動製作 Chrome 外掛的參考範例、工具選擇與最佳實踐。

---

## 推薦工具

| 工具 | 適合場景 | 價格 |
|------|---------|------|
| **Claude Code** | 自主多檔案生成、終端機優先 | $17-20/月 |
| **Cursor** | AI-native IDE、深度整合、迭代開發 | $20/月 |
| **GitHub Copilot** | 跨 IDE 支援、廣泛相容 | $10/月 |

目前**不存在**專門的「Chrome 擴充功能 AI 產生器」，最佳方案是使用通用型 AI 編碼代理並搭配良好的設定檔。

---

## 關鍵參考範例與教學

### 1. Prompt Warrior 方法 (強烈推薦)
- **連結**: https://www.thepromptwarrior.com/p/how-to-build-a-chrome-extension-with-ai
- **方式**: 使用 Claude/ChatGPT 規劃 + Cursor 開發，無需程式經驗
- **流程**: 文字需求 prompt → AI 產出 MVP 功能清單、技術架構、檔案結構 → 迭代實作
- **特點**: 需求文件直接作為 AI spec，AI 從單一 prompt 生成完整專案

### 2. Meryam Bukhari — Claude 建置閱讀助手擴充功能
- **連結**: https://meryam.substack.com/p/ai-tutorial-i-built-a-browser-extension
- **GitHub**: https://github.com/123mbam/3rdextension
- **方式**: Claude chatbot + VS Code + Gemini API，數小時完成
- **特點**: 使用草圖+文字描述作為需求輸入

### 3. Google 官方 Chrome Extension AI 樣本
- **GitHub**: https://github.com/GoogleChrome/chrome-extensions-samples
- **包含**: Gemini Cloud API 範例、Gemini Nano 裝置端範例、Summarizer API 範例
- **官方文件**: https://developer.chrome.com/docs/extensions/ai

### 4. YouTube 教學
- "Build a Chrome Extension Using AI with Cursor": https://www.youtube.com/watch?v=vIcDmkK6vMs
- Anurag Wagh 完整開發者指南: https://www.anuragwagh.me/blog/how-to-build-chrome-extension-with-ai

---

## 從需求文件自動生成的最佳實務

### 步驟 1：建立結構化需求文件
將需求寫入 `AGENTS.md`（跨工具通用標準，60,000+ 開源專案採用），包含：
- 技術棧（Manifest V3、TypeScript 等）
- 專案結構
- 建置指令
- 權限清單

### 步驟 2：分階段提示 (Prompt in Phases)
1. **Scaffold**: manifest.json、資料夾結構
2. **核心邏輯**: service worker、content scripts
3. **UI**: popup、side panel、options page
4. **權限與 API**: permissions、host_permissions
5. **封裝測試**: 打包與 Chrome dev mode 測試

### 步驟 3：明確定義 Manifest V3 約束
在每個 prompt 中明確指定：
- 所有程式碼必須在套件內（無遠端執行）
- Service worker 無 DOM 存取 — 需要時使用 offscreen document
- Content scripts 執行在 isolated world
- 所有權限必須預先在 manifest.json 宣告

### Prompt 範本
```
I want to build a Chrome extension (Manifest V3) that [功能描述].
Tech stack: HTML, CSS, JavaScript.
Key constraints:
- All logic must be in the package (no remote code)
- Use service worker for background tasks
- Declare all permissions upfront
Help me plan the MVP features and file structure first.
```

---

## 已知限制與注意事項

1. **API 幻覺**: AI 可能產生不存在的 API 或混合 V2/V3 語法
2. **安全性**: AI 生成程式碼可能包含 XSS 漏洞、硬編碼憑證
3. **無法測試**: AI 無法在瀏覽器中載入擴充功能測試，除錯需手動
4. **權限混淆**: AI 經常宣告過多或遺漏必要權限
5. **無持久記憶**: 無 `AGENTS.md` 設定檔時，每次 session 需重複指令

---

## 核心結論

1. **最佳工具組合**: GitHub Copilot ($10/mo) 廣度 + Claude Code ($20/mo) 深度
2. **需求文件即 spec**: 將 `.md` 需求文件作為 AI 的 spec 輸入，減少反覆溝通
3. **迭代開發**: 先建最簡可行版本 (MVP)，再逐步疊加功能
4. **務必人工審查**: 安全相關程式碼需逐行審查
5. **參考官方樣本**: `GoogleChrome/chrome-extensions-samples` 作為 AI 上下文

---

## 原始資料來源

- Chrome Extensions 官方文件: https://developer.chrome.com/docs/extensions/get-started
- Extensions + AI 官方指南: https://developer.chrome.com/docs/extensions/ai
- Chrome Extensions Samples: https://github.com/GoogleChrome/chrome-extensions-samples
- Prompt Warrior 教學: https://www.thepromptwarrior.com/p/how-to-build-a-chrome-extension-with-ai
- Meryam Bukhari 實例: https://meryam.substack.com/p/ai-tutorial-i-built-a-browser-extension
- CosmicJS 工具比較: https://www.cosmicjs.com/blog/claude-code-vs-github-copilot-vs-cursor-which-ai-coding-agent-should-you-use-2026
- DeployHQ AI 設定檔指南: https://www.deployhq.com/blog/ai-coding-config-files-guide
- Toolradar AI 程式碼助手評比: https://toolradar.com/guides/best-ai-code-assistants
