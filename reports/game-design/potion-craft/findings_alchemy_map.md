# Potion Craft: Alchemist Simulator — 炼金术地图与草药机制研究报告

## 一、炼金术地图（Alchemy Map）概述

炼金术地图是《Potion Craft》中最核心的机制，它是一个**抽象的二维空间**，药水酿造过程以可视化路径的方式在此展开。炼药师将草药投入坩埚后，草药的"路径"会被绘制到地图上，从当前**药水标记（Potion Marker）** 的位置开始延伸。搅拌坩埚会使药水标记不可逆地沿路径前进；使用**长柄勺（Ladle）** 则使标记向地图原点（中心）移动。

**核心机制：**
- 每株草药都有特定的**方向向量**，投入后会在地图上绘制一段路径
- 草药的**研磨程度（0%~100%）** 影响路径的长度和方向
- **搅拌（Stir）** 使药水标记沿已绘制的路径移动
- **风箱（Bellows）** 用于加热坩埚，使药水标记最终注入效果

参考来源：
- https://potion-craft.fandom.com/wiki/Alchemy_Map
- https://www.gamezebo.com/walkthroughs/potion-craft-maps/

---

## 二、地图上的元素

### 1. 效果标记（Effect Markers）
地图上散布着各种效果图标（如心形代表治疗、雪花代表冰冻）。初次遇见时显示为**问号**，首次用药水触碰并使用风箱注入后，会永久显示对应效果符号。效果分为**三级（Tier I/II/III）**：
- 药水标记**触碰**效果标记 → Tier I（弱效）
- 药水标记**覆盖大部分**效果标记 → Tier II（中效）
- 药水标记**完全对齐**效果标记轮廓 → Tier III（强效）

效果标记的**朝向**决定可达到的最高等级：
- **瓶口朝上** → 可达到 Tier III
- **瓶口斜上** → 最高 Tier II
- **瓶口朝下** → 最高 Tier I（需使用 Moon Salt 旋转瓶身提升等级）

### 2. 漩涡（Whirlpools）
螺旋形标记，用风箱加热后沿螺旋方向旋转。药水标记触碰漩涡时会被吸引向中心，到达中心后**传送**到地图的另一个位置。合理利用漩涡可以**节省大量草药**。

### 3. 骨头（Bones）
危险区域。药水标记触碰骨头时，瓶中药水会逐渐流失；**完全流失则酿造失败**，所有投入的草药归零。离开骨头区域后药水会立即恢复。

### 4. 经验书（Experience Books）
散布在地图上的棕色书本标记（1~5本），触碰即可获得经验点数，一次性消耗后消失。

参考来源：
- https://potion-craft.fandom.com/wiki/Alchemy_Map_(0.4.7)
- https://roonby.com/2023/09/25/potion-craft-map-and-how-to-read-the-map/

---

## 三、草药与材料的分类及机制

### 基础分类
- **草药（Herbs）**：如 Firebell、Waterbloom、Terraria、Windbloom 等，**不能穿越障碍**（如骨头墙），路径较柔和
- **蘑菇（Mushrooms）**：如 Mad Mushroom、Witch Mushroom，行为类似草药
- **水晶/矿石（Crystals/Stones）**：如 Cloud Crystal、Fire Citrine，**可以穿越骨头等障碍**，路径长且笔直，价格昂贵

### 研磨机制
草药在投入前可使用**研钵（Mortar & Pestle）** 研磨。研磨程度（0%~100%）**精确影响路径的长度和方向**：
- 0% 研磨（整株投入）：路径最长，方向最纯
- 100% 研磨（完全粉碎）：路径最短
- 部分研磨（如 46%、52%）：产生介于中间的长度和方向

高级配方中，**精确控制研磨百分比**是到达特定效果节点的关键。

### 四大基础草药的方向
| 草药 | 方向 |
|------|------|
| Firebell | 东北/东 |
| Waterbloom | 西北/西 |
| Terraria | 东南/南 |
| Windbloom | 西南/北 |

组合使用基础草药可以在地图上朝任意方向移动药水标记。

参考来源：
- https://gameplay.tips/guides/potion-craft-alchemist-simulator-ultimate-alchemy-guide.html
- https://potion-craft.fandom.com/wiki/Potions

---

## 四、药水基底系统（Water / Oil / 进阶）

### 水基底（Water Base）
- 游戏初期默认使用
- **水地图**包含游戏中**所有效果**
- 地图由**骨头墙**分为内环和外环两部分
- **内环**效果：瓶口朝上，无需盐即可达到 Tier III
- **外环**效果：瓶口旋转朝向，需要使用 Moon Salt 旋转后才能达到 Tier III

### 油基底（Oil Base）
- 在游戏后期（约第23天后）从 Fellow Alchemist 处以 8000 金币购买
- **油地图**比水地图小
- 部分在水地图上**旋转**的效果，在油地图上呈**直立**状态（更易达到 Tier III）
- 油地图独有的**沼泽（Swamp）** 区域：移动速度减半，消耗更多路径
- 适合制作各类 **防护药水**（Acid Protection、Fire Protection 等）

### 效果分布对照
- 水地图内环效果的瓶身，在油地图上会旋转
- 水地图外环效果的瓶身，在油地图上恢复直立
- 6种效果在两幅地图上均为直立：**幻觉（Hallucination）、香气（Fragrance）、幸运（Luck）、诅咒（Curse）、恐惧（Fear）、灵感（Inspiration）**

参考来源：
- https://potion-craft.fandom.com/wiki/Oil_Map
- https://steamcommunity.com/app/1210320/discussions/0/599641286096505580/

---

## 五、药水效果与配方示例

### 基础配方（水基底）
| 药水 | 配方 |
|------|------|
| 治疗药水（Tier III） | 1× Waterbloom（全研磨） + 1× Mudshroom（全研磨） |
| 火焰药水（Tier III） | 4× Firebell（全研磨） + 1× Terraria（整株） |
| 闪电药水（Tier III） | 4× Windbloom（全研磨） + 2× Waterbloom（全研磨） |
| 睡眠药水（Tier III） | 4× Waterbloom（全研磨） + 1× Terraria（全研磨） |
| 爆炸药水（Tier III） | 3× Mad Mushroom（全研磨） |

### 进阶配方（油基底）
| 药水 | 配方 |
|------|------|
| 强效胶水药水 | 1× Thornstick（68%研磨） + 1× Mudshroom（80%研磨） + 1× Goldthorn（34%研磨） + 1× Lifeleaf（全研磨） |
| 强效滑溜药水 | 1× Witch Mushroom（全研磨） + 1× Druid's Rosemary（全研磨） + 1× Coldleaf（37%研磨） + 1× Healers Heather（适量研磨） |

参考来源：
- https://www.gamezebo.com/walkthroughs/potion-craft-recipes/
- https://attackofthefanboy.com/guides/all-effects-for-potions-in-potion-craft/

---

## 六、高级炼金术技巧

### 1. 长柄勺（Ladle）微调
长柄勺可向地图中心**回拉**药水标记，用于微调位置以精确对齐效果标记，是达到 Tier III 的关键工具。

### 2. 多种效果混合
炼制**多效药水**的方法：先到达一个效果节点注入效果，**不结束酿造**，继续添加草药前往第二个效果节点再注入。注意部分效果**互斥**（如治疗和毒药）。

### 3. 配方保存与复用
存档配方后，只要拥有对应的草药存货，即可一键沿已记录的路径重现，无需重新摸索。

### 4. Alchemy Machine（炼金机器）
地下室中的炼金机器可制作高级材料：
- **Void Salt**：逐渐擦除已绘制的路径
- **Moon Salt**：逆时针旋转药水及其路径（改变效果瓶身朝向）
- **Sun Salt**：顺时针旋转药水及其路径
- **Life Salt**：恢复药水生命值
- **Philosopher's Salt**：将药水拉向最近的效果
- **Philosopher's Stone（贤者之石）**：终极材料，完成 Magnum Opus

升级炼金机器需要分阶段花费 2000 + 6000 + 12000 金币。

### 5. 配方限制条件（顾客需求）
顾客可能会提出以下限制，影响配方设计：
- **Mixed**：允许所有材料
- **Organic**：禁止水晶
- **Herbal**：仅草药
- **Fungal**：仅蘑菇
- **Cardinal**：仅8种基础材料
- **Crystalline**：仅水晶
- **Dry**：禁止使用药水基底
- **Wet**：允许使用药水基底

参考来源：
- https://potion-craft.fandom.com/wiki/Alchemy_Machine
- https://gameplay.tips/guides/potion-craft-alchemist-simulator-ultimate-alchemy-guide.html

---

## 七、总结

Potion Craft 的炼金术地图系统是一个**方向+距离+研磨精度**的三维策略空间：
1. 每种草药都有**固定方向**，研磨程度控制**路径长度**
2. 玩家通过组合多种草药在地图上"导航"，到达目标效果节点
3. 药水强度取决于药水标记与效果标记的**对齐精度**
4. 水/油两种基底提供**不同的地图布局**，各有优劣
5. 漩涡、骨头、沼泽等地形元素增加策略深度
6. 炼金机器和盐类材料提供**后期的高级操控能力**

游戏中目前共有 **43种药水效果**、**58种材料**，组合方式近乎无限，鼓励玩家不断实验与优化配方。
