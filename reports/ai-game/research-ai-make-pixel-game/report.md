# Research Report: Using Code Agents to Create Pixel Games from Requirements

## 結論

Code Agent（AI 編碼代理）**已完全可以**根據需求文件製作像素遊戲。多個實際案例證明，從零經驗的非工程師到專業開發者，都能透過 AI 代理成功產出可玩的像素遊戲。

---

## 1. 推薦的 AI 代理工具

| 工具 | 適合用途 | 價格 |
|------|----------|------|
| **Claude Code** (Anthropic) | 單一提示生成完整遊戲，複雜邏輯最好 | ~$3/$15 per M tokens |
| **Cursor IDE** + Claude | 多檔案專案、迭代開發最佳組合 | Token-based |
| **ChatGPT** (GPT-4/5) | 快速原型、單檔 HTML 遊戲 | $20/月 (Plus) |
| **GitHub Copilot Agent** | 專業專案、CI/CD 整合 | $10-39/月 |

**最強組合：Claude + Cursor** — Claude 提供最佳程式碼品質，Cursor 提供最佳代理工作流程。

---

## 2. 推薦的遊戲框架

| 框架 | 語言 | 適合度 | 原因 |
|------|------|--------|------|
| **Pyxel** ⭐ | Python | **最佳** | 內建 CLAUDE.md、16色限制、256x256畫面、內建編輯器 |
| **Pygame** | Python | 佳 | 簡單 API、大量訓練資料 |
| **Phaser.js** | JavaScript | 佳 | 瀏覽器即時執行、單檔部署 |
| **Godot** | GDScript | 佳 | 2D 引擎、節點系統 |
| **GameMaker** | GML | 新增支援 | 2026年4月整合 Claude Code CLI |

**不要用** Unity / Unreal — AI 難以處理其元件系統與編輯器依賴。

---

## 3. 具體成功案例

### 案例 A: SameGame (Pyxel + ChatGPT)
- 作者幾乎**零手寫程式碼**，全部由 ChatGPT 生成
- 流程：確認規則 → 生成基礎版 → 貼錯誤訊息 → 自然語言加功能
- 最終：5種難度、計分、音效、BGM
- 來源：https://qiita.com/hann-solo/items/d5093fd30a89f42f08c4

### 案例 B: Snake.io (TypeScript/Vue 3 + Claude Sonnet 4.5)
- Type-first 架構，Claude 提出 fixed-timestep accumulator pattern
- 3種遊戲模式、觸控支援、排行榜
- 關鍵：小而聚焦的請求比大型提示更好
- 來源：https://dev.to/blamsa0mine/building-a-typescript-snakeio-game-with-vue-3-and-claude-sonnet-45-1p9k

### 案例 C: Snake + 8-Bit 像素美術 (Claude Artifacts)
- ~3 個提示完成，幾分鐘內出貨
- Claude 同時生成**像素美術和遊戲程式碼**
- 關鍵：使用 AI 自己的變數名稱在後續提示中
- 來源：https://pandaitech.my/alpha/creating-a-snake-game-and-8-bit-graphic-assets-wit-b1f6j8g0

### 案例 D: Flappy Bird 在實體硬體上 (Claude Code)
- 非開發者也能用「vibe-coding loop」完成
- 流程：描述 → 生成 → 編譯 → 測試 → 修復 → 重複
- 來源：https://posthog.com/tutorials/deskhog-claude-tutorial

### 案例 E: 零經驗非工程師做出完整遊戲 (Claude 3 Opus)
- 作者是無程式經驗的攝影師，用 Claude 寫全部程式碼
- DALL-E 3 生成背景美術
- 證明 AI 讓**完全非工程師**也能做遊戲
- 來源：Reddit r/artificial

---

## 4. 最佳提示策略

### 策略 A: 遊戲設計文件 (GDD) 方法
先寫結構化的 GDD 再寫程式碼，包含：
- 核心機制（一句話）
- 操作方式
- 視覺風格（解析度、色數）
- 遊戲物件
- 勝敗條件

### 策略 B: 一次做一件事
```
BUILD N: [功能名稱]
CONTEXT: 之前已經有 [X, Y, Z]
NEW: 加入 [特定功能]
TEST: 執行遊戲驗證 [預期行為]
```

### 策略 C: 代理專用結構化模板
````
## Task
Create a pixel [genre] game using [framework].

## Requirements
1. [功能需求]
2. [視覺需求]
3. [操作需求]

## Files
- main.py
- player.py
- ...

## Constraints
- 16 colors max
- 256x256 screen
- 60 FPS
````

### 策略 D: Vibe Coding 循環
1. **描述**想要的東西
2. **生成**初始實作
3. **立即測試**
4. **回報**問題（自然語言）
5. **修復**
6. **增強**（加入下一功能）
7. **出貨**

---

## 5. 像素美術資產策略

**最佳做法：在程式碼中定義資產**（而非依靠 AI 生成圖檔）

```python
# AI 擅長生成陣列/tilemap 資料
tilemap = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 2, 0],
    [3, 3, 3, 3, 3],
]
```

如果需要圖檔，混合流程：AI 生成概念 → Aseprite/Pyxel Editor 清理 → 遊戲引擎 tilemap 系統。

---

## 6. 關鍵成功因素

| 因素 | 說明 |
|------|------|
| **小範圍迭代** | 一次一個功能，測試後再繼續 |
| **使用版本控制** | 每次 AI 修改前提交正常版本 |
| **固定框架版本** | AI 常混淆不同版本的 API |
| **CLAUDE.md / AGENTS.md** | 在專案根目錄放 AI 編碼規範（Pyxel 做法最佳） |
| **貼錯誤訊息** | 不要重新描述問題，直接貼錯誤訊息給 AI |
| **分模組** | 大檔案會混淆 AI，及早拆分 |
| **使用 AI 的命名** | 後續提示中使用 AI 自己創造的變數名稱 |

---

## 7. 潛在限制

1. **像素美術生成**仍是瓶頸 — AI 寫遊戲邏輯遠比生成資產圖檔強
2. **回歸錯誤** — AI 修改時可能破壞原本正常的功能
3. **上下文視窗限制** — 長時間會話有長度限制
4. **API 幻覺** — AI 可能發明不存在的框架方法
5. **邊界情況遺漏** — AI 傾向只覆蓋快樂路徑

---

## 8. 給 Painting Goblin 的建議

針對讓 Code Agent 根據需求文件製作像素遊戲：

1. **選 Pyxel 作為首選框架** — Python 基底、內建 AI 協作政策、16色限制讓範圍可控
2. **需求文件格式化** — 使用 GDD 風格的結構化 markdown 文件
3. **使用 AGENTS.md** — 在專案根目錄放 AI 編碼規範
4. **Vibe Coding 工作流** — 生成 → 測試 → 修復 → 增強 循環
5. **程式碼內建資產** — 避免 AI 生成圖檔，改用 tilemap 陣列
6. **逐功能迭代** — 永遠不要一次要求整個遊戲

---

## 參考來源

- https://github.com/kitao/pyxel - Pyxel 遊戲引擎 (17.4k stars)
- https://cursor.com/features - Cursor IDE
- https://github.com/features/copilot - GitHub Copilot
- https://qiita.com/hann-solo/items/d5093fd30a89f42f08c4 - Pyxel SameGame + ChatGPT
- https://dev.to/blamsa0mine/building-a-typescript-snakeio-game-with-vue-3-and-claude-sonnet-45-1p9k - Snake.io + Claude
- https://posthog.com/tutorials/deskhog-claude-tutorial - Flappy Bird + Claude Code
- https://www.gamedeveloper.com/production/gamemaker-incorporates-claude-code-to-enable-ai-assisted-workflows - GameMaker + Claude Code
- https://github.com/kitao/pyxel/blob/main/CLAUDE.md - Pyxel CLAUDE.md 範本
