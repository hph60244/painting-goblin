---
tags: ['#idea', '#task/suspend', '#game', '#wip']
---

# OpenSpec Proposal Series
# 崩壞將棋（Collapse Shogi）

## 專案概念

崩壞將棋是一種將棋變體。

除了正常將棋規則之外，棋盤會隨時間逐漸崩壞。

在每位玩家的奇數回合結束時，系統會從該玩家側的棋盤邊緣隨機選擇一格進行標記。

被標記的格子會在下一個對應玩家回合結束時永久消失。

若格子消失時上面存在棋子，該棋子會一同被移除。

若被移除的是王將，該玩家立即敗北。

---

# Proposal 001
# Project Bootstrap

## Goal

建立最小可執行 pygame 專案。

## Scope

- 9x9 棋盤
- 格子渲染
- 滑鼠選取格子
- 回合切換

## Out of Scope

- 棋子
- 將棋規則
- 崩壞系統

## Acceptance Criteria

- 顯示 9x9 棋盤
- 可選取格子
- 顯示目前玩家
- Space 鍵切換回合

## Architecture

```text
Game
├─ Board
├─ Renderer
└─ TurnManager
```

---

# Proposal 002
# Piece Prototype

## Goal

建立最小棋子系統。

## Scope

僅實作：

- 王將
- 步兵

## Rules

### 王將

八方向移動一格。

### 步兵

向前移動一格。

## Acceptance Criteria

- 棋子可選取
- 顯示合法移動位置
- 可執行移動

## Data Model

```python
class Piece:
    owner
    piece_type
    position
```

---

# Proposal 003
# Capture System

## Goal

加入吃子機制。

## Rules

移動到敵方棋子所在格：

- 敵方棋子消失

## Victory Condition

敵方王將被吃掉：

- 立即勝利

## Acceptance Criteria

- 棋子可被移除
- 顯示勝負結果

---

# Proposal 004
# Board Collapse Prototype

## Goal

加入棋盤崩壞機制。

## Tile State

```python
class TileState(Enum):
    NORMAL
    MARKED
    REMOVED
```

## Rules

玩家奇數回合結束後：

```text
Turn 1
Turn 3
Turn 5
...
```

系統：

- 從玩家側邊緣選一格
- 標記為 MARKED

## Visual

### NORMAL

白色

### MARKED

紅色閃爍

### REMOVED

黑色空洞

## Acceptance Criteria

- 奇數回合產生標記
- 標記正確顯示

---

# Proposal 005
# Piece Destruction

## Goal

格子消失時摧毀棋子。

## Rules

當格子變成 REMOVED：

- 若存在棋子
- 棋子同步移除

## Special Rule

若移除王將：

- 玩家立即敗北

## Acceptance Criteria

- 棋子會隨格子消失
- 王將掉落判負

---

# Proposal 006
# Collapse Scheduler

## Goal

支援延遲崩壞事件。

## Data Model

```python
class CollapseEvent:
    owner
    target_tile
    created_turn
    execute_turn
```

## Example

```text
Turn 1
標記 A

Turn 2
A 消失

Turn 3
標記 B

Turn 4
B 消失
```

## Acceptance Criteria

- 多個事件可同時存在
- 事件正確執行

---

# Proposal 007
# Edge Selection Rules

## Goal

定義崩壞格選取規則。

## Selection Pool

### 先手

```text
第 9 排
```

### 後手

```text
第 1 排
```

## Invalid Targets

不可選：

- MARKED
- REMOVED

## Fallback

若整排無合法格：

```text
向內搜尋下一排
```

## Acceptance Criteria

- 永遠能找到合法目標

---

# Proposal 008
# Full Shogi Lite

## Goal

加入主要棋種。

## Pieces

- 王
- 金
- 銀
- 桂
- 香
- 飛
- 角
- 步

## Out of Scope

- 成棋
- 持駒
- 打入

## Acceptance Criteria

- 可進行簡化版將棋對局

---

# Proposal 009
# Promotion System

## Goal

加入升變。

## Promotion Zone

敵陣三排。

## Supported Pieces

- 步
- 香
- 桂
- 銀
- 飛
- 角

## Acceptance Criteria

- 進入升變區可選擇升變
- 升變後移動規則正確

---

# Proposal 010
# Hand Pieces

## Goal

加入完整將棋特色。

## Rules

吃到敵方棋子：

```text
加入持駒區
```

玩家可：

```text
將持駒打入棋盤
```

## Future Restrictions

- 二步
- 打步詰
- 不合法打入

## Acceptance Criteria

- 可使用持駒

---

# Proposal 011
# Collapse Strategy Layer

## Goal

讓崩壞規則可替換。

## Mode

### RANDOM

```text
完全隨機
```

### CHOOSE_ONE

```text
系統提出兩格
玩家選擇一格
```

### PLAYER_CONTROLLED

```text
玩家指定崩壞位置
```

## Data Model

```python
class CollapseMode(Enum):
    RANDOM
    CHOOSE_ONE
    PLAYER_CONTROLLED
```

## Acceptance Criteria

- 規則可自由切換

---

# Proposal 012
# Sudden Death

## Goal

加速終局。

## Trigger

剩餘格數：

```text
<= 30
```

## Effect

每次崩壞：

```text
標記 2 格
```

## Acceptance Criteria

- 終局速度顯著提升

---

# Proposal 013
# AI Opponent

## Goal

加入單機 AI。

## Phase 1

隨機合法移動。

## Phase 2

加入權重：

- 保護王將
- 吃子
- 遠離崩壞格

## Phase 3

Minimax

```text
Depth 2~3
```

## Acceptance Criteria

- AI 可完成對局

---

# Proposal 014
# Replay System

## Goal

方便測試與除錯。

## Save Format

```json
{
  "turn": 17,
  "moves": [],
  "collapse_events": []
}
```

## Features

- Replay
- Pause
- Step
- Fast Forward

## Acceptance Criteria

- 可重播完整對局

---

# Proposal 015
# Rule DSL

## Goal

讓所有環境規則資料化。

## DSL Example

```yaml
collapse:
  enabled: true

  trigger:
    odd_turn_end: true

  source:
    side: self

  selection:
    mode: random

  delay_turns: 1

  destroy_piece: true

  king_fall_loss: true
```

---

# Core Data Model

## Board

```python
class Board:
    width = 9
    height = 9
    tiles
```

## Tile

```python
class Tile:
    state
    piece
```

## Piece

```python
class Piece:
    owner
    piece_type
    promoted
    position
```

## Collapse Event

```python
class CollapseEvent:
    target_tile
    execute_turn
```

## Game State

```python
class GameState:
    board
    players
    turn
    collapse_events
    winner
```

---

# Future Environment Expansions

透過 DSL 可快速製作不同棋盤災害。

## 火山將棋

```yaml
volcano:
  eruption_every: 5
```

效果：

- 隨機區域爆炸
- 周圍棋子摧毀

---

## 冰河將棋

```yaml
ice:
  slide_enabled: true
```

效果：

- 棋子進入冰面會持續滑行

---

## 毒霧將棋

```yaml
poison:
  spread_each_turn: true
```

效果：

- 毒區持續擴散
- 停留扣血

---

## 黑洞將棋

```yaml
blackhole:
  attract_radius: 2
```

效果：

- 棋子逐漸被拉向中心

---

## 地震將棋

```yaml
earthquake:
  random_shift: true
```

效果：

- 棋子位置可能被震動改變

---

# Recommended Development Order

```text
001 Project Bootstrap
002 Piece Prototype
003 Capture System
004 Board Collapse Prototype
005 Piece Destruction
006 Collapse Scheduler
007 Edge Selection Rules
008 Full Shogi Lite
009 Promotion System
010 Hand Pieces
011 Collapse Strategy Layer
012 Sudden Death
013 AI Opponent
014 Replay System
015 Rule DSL
```

預計完成 Proposal 005 後，即可得到第一個可遊玩的 MVP 版本。

---

想不到提高中毒性的玩法
[将棋が流行らない理由](https://www.youtube.com/watch?v=Dc_qe-RUJ7Q&ab_channel=%E3%80%90%E5%B0%86%E6%A3%8B%E3%80%91%E5%8F%B3%E5%9B%9B%E9%96%93%E9%A3%9B%E8%BB%8A%E3%83%81%E3%83%A3%E3%83%B3%E3%83%8D%E3%83%AB%E3%81%9D%E3%82%89)

---

- https://www.chessprogramming.org/Main_Page
- https://sebastian.itch.io/tiny-chess-bots
- https://www.youtube.com/watch?v=Ne40a5LkK6A
- https://lishogi.org/
- [Help Make Esports Better: The Good Game Project](https://www.youtube.com/watch?v=iyvkIBA7pNE)
- https://www.youtube.com/watch?v=XSCFrzA3psE
- https://www.youtube.com/watch?v=NotXnKh5F6s
- [【連載】評価関数を作ってみよう！その3 , やねうら王 公式サイト](https://yaneuraou.yaneu.com/2020/11/20/make-evaluate-function-3)
- [コンピュータ将棋の本 ＠将棋 棋書ミシュラン！](https://rocky-and-hopper.sakura.ne.jp/Kisho-Michelin/package/computer.htm)
- [「現代将棋を読み解く７つの理論」あらきっぺさんインタビュー プロ棋士はどんな思考プロセスを踏むのか？ ｜好書好日](https://book.asahi.com/article/14230780)
- [文部科学大臣杯第5回電竜戦は氷彗が初優勝 , コンピュータ将棋協会blog](http://blog.computer-shogi.org/hisui_wins_denryu-sen-5)
- [fairy-stockfish/Fairy-Stockfish: chess variant engine supporting Xiangqi, Shogi, Janggi, Makruk, S-Chess, Crazyhouse, Bughouse, and many more](https://github.com/fairy-stockfish/Fairy-Stockfish)
- [SebLague/Chess-Coding-Adventure: A work-in-progress chess bot written in C#](https://github.com/SebLague/Chess-Coding-Adventure)
- [Chaosus/ModernShogi: Modern Shogi is free, advanced 3D japanese chess client, with AI and multiplayer, made in Godot 3.1](https://github.com/Chaosus/ModernShogi)
- [yaneurao/YaneuraOu: YaneuraOu is the World's Strongest Shogi engine(AI player) , WCSC29 1st winner , educational and USI compliant engine.](https://github.com/yaneurao/YaneuraOu/tree/master)
- [Coding Adventure: Making a Better Chess Bot - YouTube](https://www.youtube.com/watch?v=_vqlIPDR2TU&t=372s)
- [将棋ったー](https://shogitter.com)
- [「将棋」人気ランキング , フリーゲーム投稿サイト unityroom](https://unityroom.com/rankings/tags/121)

- [[Shogi Opening]]
- [[Tsume Shogi]]
- [[Shogi Tool]]
