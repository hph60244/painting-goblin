---
tags: ['#idea', '#task/suspend', '#game']
---

- 玩家在一個無限深的垂直洞穴掉落中，需要在掉落的同時收集資源...等生存遊戲會作的事
- 使用道具調整落下物

# Falling Survival MVP 開發規格

"玩家不斷落下，在空中水平移動
收集資源，躲避危險
生命隨時間消耗
有背包管理資源
資源用於維生
偶爾有平台可以活動"

## 遊戲概念

玩家持續向下墜落，在有限生命下收集資源、躲避危險，利用取得的資源維持生存，並盡可能到達更深處。

---

# 核心玩法循環

```text
下墜
 ↓
收集資源
 ↓
生命持續消耗
 ↓
使用資源維持生命
 ↓
躲避危險
 ↓
利用平台喘息
 ↓
繼續下墜
```

## 勝負條件

### 失敗

- HP歸零
- 碰觸致命危險物

### 目標

- 生存更長時間
- 到達更深深度
- 獲得更高分數

---

# MVP功能範圍

## 玩家

### 操作

| 按鍵 | 功能 |
|--------|--------|
| A / ← | 左移 |
| D / → | 右移 |

### MVP不包含

- 跳躍
- 攻擊
- 技能
- 建造

### 玩家數值

```yaml
MoveSpeed: 300
FallSpeed: 200

MaxHP: 100
CurrentHP: 100
```

---

# 生命系統

生命會持續流失。

```yaml
HPDrain: 1 HP/s
```

範例：

```text
初始HP = 100

100秒後死亡
(若未取得補給)
```

---

# 資源系統

## 食物

```text
🍎
```

用途：

```yaml
Heal: +20 HP
```

使用方式：

- 從背包點擊使用
- 立即恢復生命

---

## 金屬

```text
⛓
```

用途：

```yaml
ScoreValue: 50
```

功能：

- 作為分數來源
- MVP階段不具其他用途

---

# 背包系統

## 容量

```yaml
Slots: 8
```

範例：

```text
[🍎][🍎][⛓][ ]
[ ][ ][ ][ ]
```

---

## 操作

### 支援

- 自動拾取
- 點擊使用食物

### 不支援

- 拖曳排序
- 堆疊拆分
- 丟棄物品
- 合成

---

# 掉落物生成

## 生成規則

每秒生成一次。

```yaml
Food:
  Weight: 60

Metal:
  Weight: 40
```

生成位置：

```text
畫面上方隨機X座標
```

---

# 危險物

## 尖刺岩石

```text
▲
```

效果：

```yaml
Damage: 20
```

碰撞後：

- 立即扣血

---

## 毒氣球

```text
●
```

效果：

```yaml
Damage: 10
PoisonDuration: 5s
PoisonDamage: 2 HP/s
```

碰撞後：

- 立即扣血
- 套用中毒效果

---

# 平台系統

## 普通平台

功能：

```yaml
FallSpeed: 0
```

玩家站立時：

- 停止下墜
- 可左右移動

---

## 崩塌機制

```yaml
CollapseTime: 5s
```

流程：

```text
玩家站上平台
↓
倒數5秒
↓
平台消失
↓
繼續下墜
```

---

# 世界生成

採用Chunk系統。

## Chunk規格

```yaml
ChunkHeight: 1000
```

每個Chunk內容：

```yaml
Resources: 5~10
Hazards: 2~5
Platforms: 0~2
```

---

## 無限生成

```text
玩家接近Chunk底部
↓
生成下一Chunk
↓
刪除最上方Chunk
```

保持固定記憶體使用量。

---

# 深度系統

玩家持續下墜時增加深度。

```yaml
DepthUnit: meter
```

顯示：

```text
Depth: 1240m
```

---

# 分數系統

## 計算公式

Score：

```text
Depth + Metal × 50
```

範例：

```text
Depth = 2000

Metal = 12

Score
= 2000 + (12 × 50)
= 2600
```

---

# UI規格

## 左上角

```text
HP: 83/100
Depth: 1240m
```

---

## 右上角

```text
Time: 02:34
```

---

## 底部

```text
[🍎][🍎][⛓][ ]
```

顯示：

- 背包內容
- 物品數量

---

# Godot場景架構

```text
Main
 ├─ Player
 ├─ Camera2D
 ├─ World
 ├─ ChunkManager
 ├─ SpawnManager
 ├─ UI
 └─ GameManager
```

---

# 資料結構

## ItemData

```gdscript
class_name ItemData

enum ItemType {
    FOOD,
    METAL
}

var item_name
var icon
var stack_size
```

---

## Inventory

```gdscript
class_name Inventory

var slots = []
var max_slots = 8
```

---

## PlayerStats

```gdscript
class_name PlayerStats

var max_hp = 100
var hp = 100

var move_speed = 300
var fall_speed = 200
```

---

# 物件類別

```text
Collectible
 ├─ Food
 └─ Metal

Hazard
 ├─ SpikeRock
 └─ PoisonBalloon

Platform
 └─ BasicPlatform
```

---

# MVP驗收標準

## 玩家

- [ ] 左右移動
- [ ] 持續下墜
- [ ] 攝影機追蹤

## 生存

- [ ] HP持續流失
- [ ] HP歸零死亡

## 資源

- [ ] 撿取食物
- [ ] 撿取金屬
- [ ] 使用食物回血

## 背包

- [ ] 8格背包
- [ ] 顯示內容

## 危險

- [ ] 尖刺傷害
- [ ] 中毒效果

## 平台

- [ ] 可站立
- [ ] 5秒崩塌

## 世界

- [ ] Chunk生成
- [ ] 無限下墜
- [ ] 自動卸載舊Chunk

## UI

- [ ] HP顯示
- [ ] 深度顯示
- [ ] 時間顯示
- [ ] 分數顯示

---

# 開發時程

## Day 1

- 玩家控制
- 下墜機制
- Camera追蹤

---

## Day 2

- 資源生成
- 撿取系統
- 背包UI

---

## Day 3

- HP系統
- 食物回血
- 危險物傷害

---

## Day 4

- 平台系統
- Chunk生成
- 無限世界

---

## Day 5

- 分數系統
- UI完成
- 遊戲平衡調整

---

# MVP完成定義

玩家能夠：

1. 在無限下墜世界中移動。
2. 收集資源並存入背包。
3. 使用食物維持生命。
4. 躲避危險物。
5. 利用平台短暫停留。
6. 持續向下探索更深區域。
7. 透過深度與收集物獲得分數。
8. 在死亡後顯示最終成績。

即視為 MVP 完成。
