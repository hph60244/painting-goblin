# Potion Craft: Alchemist Simulator — 草药系统与基础机制研究报告

## 一、草药（Herbs）列表与基本属性

Potion Craft 中的素材分为三大类：**草药（Herbs）**、**蘑菇（Mushrooms）** 和 **矿物（Minerals）**。以下是游戏中全部草药品种及其基本属性：

| 名称 | 售价 (基础) | 解锁章节 | 属性/方向 | 获取途径 |
|------|-----------|---------|----------|---------|
| Firebell (火铃铛) | 16.4/32.8 | 1 | 火/西 | 花园、商人 |
| Windbloom (风花) | 19.4/38.8 | 1 | 风/北 | 花园、商人 |
| Waterbloom (水花) | 16.4/32.8 | 1 | 水/东 | 花园、商人 |
| Terraria (泰拉草) | 13.4/26.8 | 1 | 土/南 | 花园、商人 |
| Lifeleaf (生命叶) | 12/24 | 1 | 生命/东南 | 花园、商人 |
| Tangleweed (缠藤) | 25.8/51.6 | 1 | 水/东 | 商人 |
| Goldthorn (金荆棘) | 38.4/76.8 | 2 | 土/南 | 商人 |
| Goodberry (好浆果) | 18/36 | 2 | 生命/东南 | 商人 |
| Hairy Banana (毛香蕉) | 31.2/62.4 | 2 | — | 商人 |
| Icefruit (冰果) | 23.4/46.8 | 2 | 水/东 | 商人 |
| Thunder Thistle (雷蓟) | 35/70 | 2 | 风·冰/东北 | 商人 |
| Bloodthorn (血荆棘) | 32.6/65.2 | 3 | 爆炸/西北 | 商人 |
| Dream Beet (梦甜菜) | 36.8/73.6 | 3 | — | 商人 |
| Druid's Rosemary (德鲁伊迷迭香) | 25.2/50.4 | 3 | 土·冰/东南 | 商人、花园 |
| Featherbloom (羽花) | 41.6/83.2 | 3 | 风/北 | 商人 |
| Lava Root (熔岩根) | 28.8/57.6 | 3 | 火/西 | 商人 |
| Coldleaf (冷叶) | 38.8/77.6 | 4 | — | 商人 |
| Flameweed (火杂草) | 35.2/70.4 | 4 | 火/西 | 商人 |
| Grasping Root (抓握根) | 37.8/75.6 | 4 | — | 商人 |
| Thornstick (刺棍) | 36.4/72.8 | 4 | 死亡/西南 | 商人 |
| Whirlweed (旋草) | 52/104 | 4 | — | 商人 |
| Boombloom (爆爆花) | 56.6/113.2 | 5 | 风·火/西北 | 商人 |
| Dragon Pepper (龙椒) | 56.4/112.8 | 5 | — | 商人 |
| Fluffbloom (绒花) | 49.8/99.6 | 5 | — | 商人 |
| Healer's Heather (治愈石楠) | 38.6/77.2 | 5 | 土·火/西南 | 商人 |
| Spellbloom (咒花) | 66/132 | 5 | 风·冰/东北 | 商人 |
| Evergreen Fern (常青蕨) | 43.2/86.4 | 6 | — | 商人 |
| Mageberry (法师浆果) | 76.2/152.4 | 6 | — | 商人 |
| Terror Bud (恐怖芽) | 32.6/65.2 | 6 | 爆炸/西北 | 商人 |

> 售价列中 A/B 分别对应 0.5 倍和 1.0 倍售价模式。

### 八元素系统（Element Sorting）

所有素材归属于 **8 种元素**，每种元素对应一个罗盘方向和对应的药水效果：

| 元素 | 罗盘方向 | 基础素材 | 对应效果 |
|------|---------|---------|---------|
| 风 Air | 北 | Windbloom, Featherbloom | Swiftness |
| 魔法 Magic | 东北 | Witch Mushroom, Thunder Thistle | Mana |
| 水 Water | 东 | Waterbloom, Tangleweed | Frost |
| 生命 Life | 东南 | Lifeleaf, Goodberry | Healing |
| 土 Earth | 南 | Terraria, Goldthorn | Strength |
| 死亡 Death | 西南 | Stink Mushroom, Thornstick | Poisoning |
| 火 Fire | 西 | Firebell, Lava Root | Fire |
| 爆炸 Explosion | 西北 | Bloodthorn, Terror Bud | Rage |

**参考来源：**
- https://potion-craft.fandom.com/wiki/Ingredients
- https://potion-craft.fandom.com/wiki/Element_Sorting
- https://gamerjournalist.com/potion-craft-ingredients/
- https://www.supercheats.com/potion-craft-alchemist-simulator-walkthrough-guide/ingredients-guide

---

## 二、炼金地图（Alchemy Map）与素材放置机制

### 地图核心机制

炼金地图是药水酿造过程的抽象空间可视化表示。其核心元素包括：

1. **药水标记（Potion Marker）** — 一个瓶状图标，代表当前正在酿造的药水在地图上的位置。
2. **效果标记（Effect Marker）** — 地图上散布的各种药水效果图标（初始为问号），当药水标记与效果标记重叠时，使用风箱（Bellows）即可注入该效果。
3. **漩涡（Whirlpools）** — 螺旋形标记，使用风箱加热坩埚时漩涡会旋转，牵引药水标记向其中心移动。
4. **骨区（Bones/Dead Zones）** — 接触骨区会使药水液体逐渐耗尽，完全耗尽则酿造失败。
5. **经验书（Experience Books）** — 棕色圆圈，内含 1-3 本书，触碰即可获得经验。

### 素材如何影响药水标记的移动

- **草药与蘑菇**：在地图上绘制连续路径，药水标记沿路径移动。
- **矿物与水晶**：可以**传送**药水标记从 A 点到 B 点（跳过骨区），但不能穿越墙壁。
- 素材的**元素属性**决定其在地图上的**方向**：
  - 火属性素材 → 向西移动
  - 风属性素材 → 向北移动
  - 水属性素材 → 向东移动
  - 土属性素材 → 向南移动
  - 复合属性（如火·风）→ 向对角线方向（如西北）移动
- 素材的**研磨程度**影响路径长度：研磨越细，路径越长（完全研磨 = 100% 路径长度，整株放入 = 约 50%）。
- 蘑菇比草药在地图上移动速度更慢。

### 双地图系统

- **水基地图（Water Map）**：游戏开始时使用，高等级效果集中在中心区域。用骨墙分为内外两层，内部效果可做 III 级，外部需要盐（Salt）才能做 III 级。
- **油基地图（Oil Map）**：约第 23 天后从大师炼金术士处购买解锁，高等级效果在外围。油图有额外的**减速区（Slow Zones）**。

### 药水等级判定

效果瓶图标的方向决定了可制作的最高等级：
- **瓶口朝上**：可制作 III、II、I 级
- **瓶口朝上偏左/右**：仅可制作 II、I 级
- **瓶口朝下**：仅可制作 I 级

**参考来源：**
- https://potion-craft.fandom.com/wiki/Alchemy_Map
- https://www.gamezebo.com/walkthroughs/potion-craft-maps/
- https://gameplay.tips/guides/potion-craft-alchemist-simulator-ultimate-alchemy-guide.html
- https://steamcommunity.com/sharedfiles/filedetails/?id=2843913467

---

## 三、获取与种植草药（Enchanted Garden 系统）

### 2.0 版本"魔法花园"更新

花园位于实验室右侧，是玩家获得可再生素材的核心场所。

### 花园区域划分

| 区域 | 解锁条件 | 可种植类型 | 特点 |
|------|---------|-----------|------|
| 主花园（Ground & Tree Trunk） | 初始可用 | 大部分草药和蘑菇 | 地面 46 格，树干可种蘑菇 |
| 池塘（Pond） | 需要技能"水下种植" | Tangleweed, Flameweed, Kraken Mushroom, Terror Bud | 不需要浇水 |
| 洞穴（Cave） | 需要技能"洞穴草药" | 多数蘑菇 + 部分草药（Bloodthorn, Goldthorn, Lava Root） | 根系统可种 Grave Truffles |
| 水晶洞（Crystal Grotto） | 需要技能"水晶种植" | 全部矿物/水晶 | 不需要浇水，47 格 |

### 种植流程

1. **学习技能**：至少需要"草药种植"和"蘑菇种植"技能。
2. **获取种子**：从商人处购买，或在收获时概率获得（1%-5%，取决于种子收获技能等级）。
3. **种植**：在花园中选择合适位置种植。
4. **生长周期**：
   - 草药/蘑菇：5 天成熟
   - 水晶：9 天成熟
   - 可通过技能"快速生长"缩短时间
5. **日常维护**：
   - 草药和蘑菇每天需要**浇水**（使用 Watering Can）
   - 水晶、池塘植物和洞穴根植物不需要浇水
6. **收获**：成熟后每天可收获一次，使用"施肥"技能（Wild Growth 药水）可在同一天获得第二次收获。
7. **初始花园植物**：Stink Mushroom、Dryad's Saddle、Lifeleaf、Windbloom、Waterbloom、Firebell、Terraria

### 重要种植技能

| 技能 | 效果 |
|------|------|
| 草药/蘑菇/水晶种植 | 允许在该区域种植 |
| 草药/蘑菇/水晶移栽 | 允许移动和收起植物 |
| 草药学/蘑菇收获 | 增加每次收获的素材量 |
| 细心照料（Careful ~ Care） | 成熟植物可能"过度生长"提供更多素材 |
| 快速生长（Quick ~ Growth） | 缩短生长时间 |
| 施肥（Fertilizing） | 可用 Wild Growth 药水加速生长或获得额外收获 |
| 种子收获（~ Seed Harvesting） | 收获时有概率获得种子（最高 5%） |

### 产量数据

- 基础产量：草药/蘑菇 **4** 个，水晶 **3** 个
- 满技能后产量：草药/蘑菇 **12** 个，水晶 **6** 个
- 施肥后（一日两次）：草药/蘑菇最高 **24** 个/天，水晶最高 **12** 个/天

**参考来源：**
- https://potion-craft.fandom.com/wiki/Enchanted_Garden
- https://potion-craft.fandom.com/wiki/Version_2.0:_The_Enchanted_Garden_Update
- https://potion-craft.fandom.com/wiki/Talent_Points
- https://yori-room.com/potioncraft-enchantedgarden/

---

## 四、基础游戏机制总结

### 游戏循环

1. **新的一天** → 去花园收获素材 + 浇水
2. **开店营业** → 接待顾客，接受订单
3. **炼制魔药** → 根据配方或在炼金地图上探索，选择合适的素材放入坩埚
4. **研磨素材** → 使用研钵和研杵研磨素材（研磨程度影响路径长度）
5. **搅拌酿造** → 搅拌坩埚使药水标记沿路径移动
6. **风箱加热** → 注入效果、激活漩涡
7. **装瓶出售** → 完成药水并出售给顾客

### 核心工具

| 工具 | 功能 |
|------|------|
| 坩埚（Cauldron） | 放入素材，绘制路径 |
| 研钵与研杵（Mortar & Pestle） | 研磨素材，改变路径长度 |
| 搅拌勺（Ladle） | 加水稀释，使药水标记向原点移动 |
| 风箱（Bellows） | 加热坩埚，注入效果 |

### 素材分类限制

部分顾客订单对素材类型有要求：
- **Mixed（混合）**：允许所有素材
- **Organic（有机）**：不允许水晶
- **Herbal（草药）**：只允许草药
- **Fungal（真菌）**：只允许蘑菇
- **Cardinal（基本）**：只允许 8 种基础素材
- **Crystalline（水晶）**：只允许水晶

### 药水效果

目前游戏共有 **41 种** 药水效果（截至 v2.0），包括：Healing、Poisoning、Fire、Frost、Explosion、Lightning、Mana、Strength、Swiftness、Dexterity、Sleep、Light、Charm、Invisibility、Levitation、Necromancy 等。

**参考来源：**
- https://potion-craft.fandom.com/wiki/Effects
- https://www.gamezebo.com/walkthroughs/potion-craft-effects/
- https://gameplay.tips/guides/potion-craft-alchemist-simulator-ultimate-alchemy-guide.html

---

*报告生成日期：2026-06-10*
