# Potion Craft: Alchemist Simulator — 药水研究报告

## 一、游戏概述

- **开发商**: niceplay games（俄罗斯独立工作室）
- **发行商**: tinyBuild
- **发行日期**: 2022年12月13日（PC / Xbox），2023年12月12日（Switch / PS）
- **游戏类型**: 炼金术模拟经营游戏
- **核心玩法**: 玩家扮演炼金术士，经营药水店铺，通过研磨原料、搅拌、加热等方式制作药水，并出售给来访的顾客。

## 二、药水品质等级系统

游戏中存在 **三级品质体系**：

| 等级 | 名称 | 描述 |
|------|------|------|
| I 级 | Weak（弱效） | 药水瓶标记仅部分对齐药水轮廓，售价约 20 金币 |
| II 级 | Normal（普通） | 中等对齐度，售价约 60 金币 |
| III 级 | Strong（强效） | 精确对齐，售价可达数百金币 |

**关键机制**: 在炼金地图上，药水瓶标记与目标药水轮廓的重合度越高，药水品质越强。使用水龙头（Water Spout）微调位置可以优化对齐度，制作强效药水以获取更高利润。

## 三、所有药水效果（共 41 种，截至 v2.0）

按字母顺序排列：

| 编号 | 英文名称 | 中文译名 | 基础价格 | 可用基底 |
|------|----------|----------|----------|----------|
| 1 | Acid | 酸液 | 720 | Water / Wine |
| 2 | Acid Protection | 酸性防护 | 760 | Water / Oil |
| 3 | Anti-Magic | 反魔法 | 1540 | Water / Oil |
| 4 | Charm | 魅惑 | 755 | Water / Wine |
| 5 | Curse | 诅咒 | 900 | Water / Wine |
| 6 | Dexterity | 灵巧 | 460 | Water / Wine |
| 7 | Enlargement | 变大 | 1180 | Water / Oil |
| 8 | Explosion | 爆炸 | 435 | Water / Oil |
| 9 | Fear | 恐惧 | 1100 | Water / Wine |
| 10 | Fire | 火焰 | 245 | Water / Oil |
| 11 | Fire Protection | 火焰防护 | 790 | Water / Oil |
| 12 | Fragrance | 芳香 | 700 | Water / Wine |
| 13 | Frost | 冰霜 | 200 | Water / Wine |
| 14 | Frost Protection | 冰霜防护 | 770 | Water / Oil |
| 15 | Gluing | 粘合 | 640 | Water / Oil |
| 16 | Hallucinations | 幻觉 | 1200 | Water / Wine |
| 17 | Healing | 治疗 | 100 | Water / Oil / Wine |
| 18 | Inspiration | 灵感 | 1400 | Water / Wine |
| 19 | Invisibility | 隐形 | 1150 | Water / Oil |
| 20 | Levitation | 漂浮 | 1320 | Water / Wine |
| 21 | Libido | 性欲 | 1120 | Water / Wine |
| 22 | Light | 光芒 | 545 | Water / Oil |
| 23 | Lightning | 闪电 | 615 | Water / Oil |
| 24 | Lightning Protection | 闪电防护 | 830 | Water / Oil |
| 25 | Luck | 幸运 | 1700 | Water / Wine |
| 26 | Magical Vision | 魔法视觉 | 920 | Water / Wine |
| 27 | Mana | 法力 | 365 | Water / Wine |
| 28 | Necromancy | 死灵术 | 2370 | Water / Wine |
| 29 | Poisoning | 中毒 | 130 | Water / Oil |
| 30 | Poison Protection | 毒素防护 | 515 | Water / Oil |
| 31 | Rage | 狂怒 | 870 | Water / Wine |
| 32 | Rejuvenation |  rejuvenation | 980 | Water / Oil |
| 33 | Shrinking | 缩小 | 1215 | Water / Oil |
| 34 | Sleep | 睡眠 | 495 | Water / Wine |
| 35 | Slipperiness |  slippery | 685 | Water / Oil |
| 36 | Slowness | 迟缓 | 660 | Water / Wine |
| 37 | Stench | 恶臭 | 645 | Water / Oil |
| 38 | Stone Skin | 石肤 | 495 | Water / Oil |
| 39 | Strength | 力量 | 290 | Water / Wine |
| 40 | Swiftness | 迅捷 | 480 | Water / Wine |
| 41 | Wild Growth | 野蛮生长 | 330 | Water / Oil |

**说明**:
- 治疗药水（Healing）是所有基底（Water / Oil / Wine）都可制作的药水
- 基础价格 ÷ 10 = 玩家实际出售时的参考售价（受难度和天赋影响）
- Necromancy（死灵术）是基础价格最高的药水（2370）

## 四、药水效果分类（按章节 Chapter 排列）

| 章节 | 可解锁效果 |
|------|-----------|
| I | Healing |
| II | Fire, Frost, Poisoning, Strength |
| III | Explosion, Wild Growth, Dexterity, Swiftness |
| IV | Lightning, Mana, Stone Skin, Sleep, Light |
| V | Charm, Hallucinations, Rage, Magical Vision |
| VI | Acid, Slowness, Invisibility, Necromancy |
| VII | Poison Protection, Fire Protection, Frost Protection, Lightning Protection, Anti-Magic |
| VIII | Inspiration, Libido, Levitation, Gluing, Slipperiness |
| IX | Fragrance, Fear, Curse, Enlargement, Shrinking, Stench, Rejuvenation |
| X | Luck, Acid Protection |

## 五、药水制作机制

### 5.1 制作流程

1. **选择基底**: 水（Water）、油（Oil）或酒（Wine），不同基底决定可抵达的炼金地图区域
2. **研磨原料**: 在研钵中使用研杵研磨植物、蘑菇、矿石等原料，研磨程度影响药水在炼金地图上的移动方向和距离
3. **加入大锅**: 将研磨好的原料加入大锅（Cauldron）
4. **搅拌**: 使用勺子（Ladle）搅拌，使药水在炼金地图上行进
5. **加热**: 使用风箱（Bellows）加热炭火，影响药水走向
6. **精确定位**: 使用水龙头（Water Spout）加水稀释，微调药水位置使其对齐目标效果
7. **完成药水**: 对齐后在效果节点上制作完成

### 5.2 炼金地图（Alchemy Map）

- 游戏核心机制是以 **2D 地图探索** 的方式呈现的
- 每种原料具有各自的元素属性（风、火、冰、地等）和方向性
- 原料在炼金地图上沿特定方向推进，探索隐藏区域
- 地图上分布着 **漩涡（Whirlpool）** 可以快速传送到其他区域
- 不同基底（水/油/酒）对应不同的地图版本

### 5.3 原料类型

- **草药**: Firebell（火铃花）、Terraria（泰拉草）、Waterbloom（水花）、Windbloom（风花）等
- **蘑菇**: Witch Mushroom（女巫蘑菇）、Weirdshroom（怪异蘑菇）、Mudshroom（泥蘑菇）等
- **矿石**: Cloud Crystal（云水晶，风元素/北向）等
- **特殊原料**: 某些原料提供传送能力（如云水晶可以跳过"骨区"）

### 5.4 原料方向属性示例

| 原料 | 元素 | 方向 |
|------|------|------|
| Cloud Crystal | Wind（风） | 北 |
| Thunder Thistle | Air/Ice（气/冰） | 东北 |
| Boombloom | Air/Fire（气/火） | 西北 |
| Mudshroom | Earth（地） | 南 |
| Terraria | Earth（地） | 南 |

## 六、参考来源

- https://potion-craft.fandom.com/wiki/Effects
- https://potion-craft.fandom.com/wiki/Strength
- https://www.supercheats.com/potion-craft-alchemist-simulator-walkthrough-guide/beginner-tips-and-tricks
- https://www.supercheats.com/potion-craft-alchemist-simulator-walkthrough-guide/ingredients-guide
- https://steamcommunity.com/sharedfiles/filedetails?id=2844840511
- https://en.wikipedia.org/wiki/Potion_Craft
- https://store.steampowered.com/app/1210320/Potion_Craft_Alchemist_Simulator
