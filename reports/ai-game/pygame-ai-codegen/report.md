# AI Code Agents for Pygame Game Generation: 綜合研究報告

**研究日期:** 2026-05-03
**目標:** 尋找讓Code Agent根據需求文件製作Pygame遊戲的參考範例

---

## 摘要

本研究調查了使用AI Code Agent根據需求文件/規格文件自動生成Pygame遊戲的現有工具、提示工程技術與實際案例。核心發現：此領域仍處於早期階段，多以小型玩具專案為主，但已有明確可用的工具鏈與模式。

---

## 一、可用工具與框架

### 1. GPT-Engineer (⭐55.2k, 已封存)
- **運作方式**: 從自然語言 `prompt` 檔案生成完整程式碼庫
- **Pygame適用性**: 可接受如「用Pygame做一個平台跳躍遊戲，含玩家移動、碰撞檢測與敵人AI」的提示
- **限制**: 一次性生成，無內建執行/除錯迴圈

### 2. Smol Developer (⭐12.2k)
- **運作方式**: 三階段管線：計畫→檔案路徑→逐檔程式碼生成
- **Pygame適用性**: 官方範例包含 **Pong遊戲** (`examples/v1_pong_game/`)，使用 `prompt.md` 描述遊戲機制
- **關鍵創新**: `shared_dependencies.md` 概念確保跨檔案一致性；支援將錯誤輸出貼回提示進行迭代除錯

### 3. GitHub Copilot / Cursor / Claude Code / Aider
- **IDE整合型工具**: 適合反覆迭代開發
- **最佳模式**: 先用GPT-Engineer/Smol Developer從規格生成骨架，再用Copilot/Cursor細修
- **Claude Code**: 可讀寫檔案、執行命令，適合自動化生成+測試循環

### 4. OpenCode (opencode.ai)
- CLI工具，支援Agent風格的工作流程，可用於根據規格生成Pygame遊戲檔案

---

## 二、提示工程最佳實踐

### 核心原則
| 原則 | 說明 |
|------|------|
| **角色設定** | 「你是一位專精Pygame的資深Python遊戲開發者」 |
| **極度具體** | 明確指定控制方式、遊戲機制、限制條件 |
| **單一檔案優先** | 首次迭代限制為單一 `.py` 檔案，減少跨檔案錯誤 |
| **避免外部資源** | 明確要求「使用pygame.draw繪圖，不依賴外部圖片檔」 |
| **指定FPS** | 總是加上 `pygame.time.Clock.tick(60)` |
| **XML標籤結構化** | 用 `<spec>` / `<constraints>` / `<code_quality>` 分隔不同部分 |

### 推薦提示模板

```
You are a senior Python game developer specializing in Pygame.

<task>
Create a complete, runnable Pygame game based on the specification below.
</task>

<spec>
- Game title: [NAME]
- Window: [WxH] pixels, title set, 60 FPS cap
- Player: [shape, color, controls, speed]
- Enemies/obstacles: [spawn pattern, movement, behavior]
- Scoring: [how points are earned/lost]
- Win/lose condition: [game over criteria]
</spec>

<constraints>
- Single .py file: game.py
- Only imports: pygame, sys, random, math
- Use pygame.draw for all graphics (no image files)
- Use pygame.Rect for collision detection
- Game loop structure: events -> update -> draw -> clock.tick(60)
- Entry point guard: if __name__ == "__main__"
- Include game over screen with R to restart, Q to quit
</constraints>
```

### 迭代模式
1. **除錯**: 「遊戲啟動時報錯：[錯誤訊息]。讀取game.py，找出根因並修復」
2. **加功能**: 「在現有遊戲中加入[功能]。不要破壞既有功能」
3. **重構**: 「重構game.py使用pygame.sprite.Sprite子類別，行為保持不變」
4. **優化**: 「當畫面上有[N]個 Sprite 時遊戲變慢，分析並優化」

---

## 三、實際案例

### 直接相關案例

| 專案 | 連結 | 說明 |
|------|------|------|
| AI Generated Snake Game | `github.com/stealthness/AI-Generated-Snake-Game` | 用ChatGPT一次提示生成的貪食蛇遊戲 |
| Pygame Flappy Bird | `github.com/aiapps-creator/pygame-flappy-bird` | AI App Generator生成的Flappy Bird |
| Snake + Auto Maze | `github.com/aiapps-creator/snake-pygame-with-auto-generated-maze` | 含迷宮生成的貪食蛇 |
| Snake + Dynamic Maze | `github.com/aiapps-creator/pygame-snake-game-with-dynamic-maze` | 動態迷宮貪食蛇變體 |
| Math Flashcards | `github.com/JD-Jones-ASES/math_flashcards` | AI生成的Pygame教育用應用 |

### 模式歸納
1. **AI寫遊戲程式碼**: LLM根據提示產生Pygame原始碼
2. **Pygame跑AI**: Pygame作為AI演算法的視覺化/模擬層

### 已確認的侷限
- 尚無大規模的端到端AI遊戲開發案例研究
- 多數範例為小型、單一檔案的實驗
- AI擅長樣板程式碼（事件循環、碰撞檢測），但架構設計仍需人工指導

---

## 四、對Painting Goblin專案的建議

### 推薦工作流程

```
[需求文件] → [Smol Developer/GPT-Engineer] → [初始Pygame骨架]
                                                 ↓
                                      [手動執行並收集錯誤]
                                                 ↓
                                      [將錯誤回饋給AI迭代]
                                                 ↓
                                      [Copilot/Cursor細修功能]
                                                 ↓
                                      [Claude Code重構與優化]
```

### 具體行動步驟
1. **準備需求文件**: 用結構化Markdown撰寫遊戲規格（視窗大小、玩家控制、敵人行為、計分方式、勝敗條件）
2. **使用Smol Developer**: 將需求文件作為 `prompt.md` 輸入，生成初始程式碼
3. **迭代除錯**: 執行遊戲，將錯誤訊息複製回提示中讓AI修復
4. **提示模板**: 使用上方提示模板確保生成品質
5. **CLAUDE.md**: 在專案根目錄建立記憶檔案，持久化Pygame版本限制與架構慣例

### 成功關鍵
- 需求文件越具體越好（控制鍵、顏色、速度數值）
- 首次迭代限定單一檔案
- 每次只改一個面向（先讓遊戲能跑，再加功能，最後重構）
- 所有可調整參數放在檔案頂部的常數區

---

## 五、參考來源

1. https://github.com/gpt-engineer-org/gpt-engineer
2. https://github.com/smol-ai/developer
3. https://github.com/features/copilot
4. https://github.com/paul-gauthier/aider
5. https://github.com/stealthness/AI-Generated-Snake-Game
6. https://github.com/aiapps-creator/pygame-flappy-bird
7. https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
8. https://code.claude.com/docs/en/overview
9. https://simonwillison.net/2024/Dec/19/gemini-2-pygame/
10. https://opencode.ai

---

*報告由web-research skill自動生成*
