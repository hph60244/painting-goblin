# 《Potion Craft: Alchemist Simulator》藥草與藥水分析報告

## 一、遊戲概述

《Potion Craft》是由 niceplay games 開發、tinyBuild 發行的煉金術模擬經營遊戲（2022年12月發售）。玩家扮演煉金術士，通過研磨原料、攪拌、加熱等方式製作藥水，並出售給來訪的顧客。核心亮點是以**二維煉金地圖**來可視化藥水釀造過程，原料搭配與研磨精度決定了最終藥水的品質與種類。

---

## 二、藥草系統

### 2.1 素材分類

遊戲中素材分為三大類：

| 類別 | 特性 | 代表素材 |
|------|------|---------|
| 草藥（Herbs） | 不能穿越障礙，路徑較柔和 | Firebell, Windbloom, Terraria |
| 蘑菇（Mushrooms） | 行為類似草藥，移動速度較慢 | Witch Mushroom, Mudshroom |
| 水晶/礦物（Crystals/Minerals） | **可穿越骨頭障礙**，路徑長且筆直 | Cloud Crystal, Fire Citrine |

### 2.2 完整素材列表（28 種草藥 + 其他素材）

| 名稱 | 售價（基礎） | 解鎖章節 | 屬性/方向 |
|------|------------|---------|----------|
| Firebell（火鈴鐺） | 16.4/32.8 | 1 | 火/西 |
| Windbloom（風花） | 19.4/38.8 | 1 | 風/北 |
| Waterbloom（水花） | 16.4/32.8 | 1 | 水/東 |
| Terraria（泰拉草） | 13.4/26.8 | 1 | 土/南 |
| Lifeleaf（生命葉） | 12/24 | 1 | 生命/東南 |
| Tangleweed（纏藤） | 25.8/51.6 | 1 | 水/東 |
| Goldthorn（金荊棘） | 38.4/76.8 | 2 | 土/南 |
| Goodberry（好漿果） | 18/36 | 2 | 生命/東南 |
| Hairy Banana（毛香蕉） | 31.2/62.4 | 2 | — |
| Icefruit（冰果） | 23.4/46.8 | 2 | 水/東 |
| Thunder Thistle（雷薊） | 35/70 | 2 | 風·冰/東北 |
| Bloodthorn（血荊棘） | 32.6/65.2 | 3 | 爆炸/西北 |
| Dream Beet（夢甜菜） | 36.8/73.6 | 3 | — |
| Druid's Rosemary（德魯伊迷迭香） | 25.2/50.4 | 3 | 土·冰/東南 |
| Featherbloom（羽花） | 41.6/83.2 | 3 | 風/北 |
| Lava Root（熔岩根） | 28.8/57.6 | 3 | 火/西 |
| Coldleaf（冷葉） | 38.8/77.6 | 4 | — |
| Flameweed（火雜草） | 35.2/70.4 | 4 | 火/西 |
| Grasping Root（抓握根） | 37.8/75.6 | 4 | — |
| Thornstick（刺棍） | 36.4/72.8 | 4 | 死亡/西南 |
| Whirlweed（旋草） | 52/104 | 4 | — |
| Boombloom（爆爆花） | 56.6/113.2 | 5 | 風·火/西北 |
| Dragon Pepper（龍椒） | 56.4/112.8 | 5 | — |
| Fluffbloom（絨花） | 49.8/99.6 | 5 | — |
| Healer's Heather（治癒石楠） | 38.6/77.2 | 5 | 土·火/西南 |
| Spellbloom（咒花） | 66/132 | 5 | 風·冰/東北 |
| Evergreen Fern（常青蕨） | 43.2/86.4 | 6 | — |
| Mageberry（法師漿果） | 76.2/152.4 | 6 | — |
| Terror Bud（恐怖芽） | 32.6/65.2 | 6 | 爆炸/西北 |

### 2.3 八元素系統

所有素材歸屬於 **8 種元素**，每種元素對應一個羅盤方向和藥水效果：

| 元素 | 羅盤方向 | 對應效果 | 基礎素材 |
|------|---------|---------|---------|
| 風 Air | 北 | Swiftness（迅捷） | Windbloom, Featherbloom |
| 魔法 Magic | 東北 | Mana（法力） | Witch Mushroom, Thunder Thistle |
| 水 Water | 東 | Frost（冰霜） | Waterbloom, Tangleweed |
| 生命 Life | 東南 | Healing（治療） | Lifeleaf, Goodberry |
| 土 Earth | 南 | Strength（力量） | Terraria, Goldthorn |
| 死亡 Death | 西南 | Poisoning（中毒） | Stink Mushroom, Thornstick |
| 火 Fire | 西 | Fire（火焰） | Firebell, Lava Root |
| 爆炸 Explosion | 西北 | Rage（狂怒） | Bloodthorn, Terror Bud |

### 2.4 魔法花園種植系統（v2.0）

玩家可在實驗室右側的花園種植素材，實現可持續供應：

| 區域 | 解鎖條件 | 可種植類型 | 特點 |
|------|---------|-----------|------|
| 主花園 | 初始可用 | 大部分草藥和蘑菇 | 地面 46 格，樹幹可種蘑菇 |
| 池塘 | 技能"水下種植" | Tangleweed, Flameweed, Terror Bud 等 | 不需要澆水 |
| 洞穴 | 技能"洞穴草藥" | 多數蘑菇 + 部分草藥 | 根系統可種 Grave Truffles |
| 水晶洞 | 技能"水晶種植" | 全部礦物/水晶 | 不需要澆水，47 格 |

- 草藥/蘑菇生長週期：**5 天**；水晶：**9 天**
- 基礎產量：草藥/蘑菇 **4** 個，水晶 **3** 個
- 滿技能後最高：草藥/蘑菇 **24 個/天**，水晶 **12 個/天**

---

## 三、藥水系統

### 3.1 品質分級

| 等級 | 名稱 | 描述 | 參考售價 |
|------|------|------|---------|
| I 級 | Weak（弱效） | 瓶身僅部分對齊效果輪廓 | ~20 金幣 |
| II 級 | Normal（普通） | 中等對齊度 | ~60 金幣 |
| III 級 | Strong（強效） | 精確對齊效果輪廓 | 數百金幣 |

### 3.2 全部 41 種藥水效果

| 編號 | 英文 | 中文 | 基礎價格 | 可用基底 |
|------|------|------|---------|---------|
| 1 | Acid | 酸液 | 720 | Water / Wine |
| 2 | Acid Protection | 酸性防護 | 760 | Water / Oil |
| 3 | Anti-Magic | 反魔法 | 1540 | Water / Oil |
| 4 | Charm | 魅惑 | 755 | Water / Wine |
| 5 | Curse | 詛咒 | 900 | Water / Wine |
| 6 | Dexterity | 靈巧 | 460 | Water / Wine |
| 7 | Enlargement | 變大 | 1180 | Water / Oil |
| 8 | Explosion | 爆炸 | 435 | Water / Oil |
| 9 | Fear | 恐懼 | 1100 | Water / Wine |
| 10 | Fire | 火焰 | 245 | Water / Oil |
| 11 | Fire Protection | 火焰防護 | 790 | Water / Oil |
| 12 | Fragrance | 芳香 | 700 | Water / Wine |
| 13 | Frost | 冰霜 | 200 | Water / Wine |
| 14 | Frost Protection | 冰霜防護 | 770 | Water / Oil |
| 15 | Gluing | 黏合 | 640 | Water / Oil |
| 16 | Hallucinations | 幻覺 | 1200 | Water / Wine |
| 17 | Healing | 治療 | 100 | Water / Oil / Wine |
| 18 | Inspiration | 靈感 | 1400 | Water / Wine |
| 19 | Invisibility | 隱形 | 1150 | Water / Oil |
| 20 | Levitation | 漂浮 | 1320 | Water / Wine |
| 21 | Libido | 性慾 | 1120 | Water / Wine |
| 22 | Light | 光芒 | 545 | Water / Oil |
| 23 | Lightning | 閃電 | 615 | Water / Oil |
| 24 | Lightning Protection | 閃電防護 | 830 | Water / Oil |
| 25 | Luck | 幸運 | 1700 | Water / Wine |
| 26 | Magical Vision | 魔法視覺 | 920 | Water / Wine |
| 27 | Mana | 法力 | 365 | Water / Wine |
| 28 | Necromancy | 死靈術 | 2370 | Water / Wine |
| 29 | Poisoning | 中毒 | 130 | Water / Oil |
| 30 | Poison Protection | 毒素防護 | 515 | Water / Oil |
| 31 | Rage | 狂怒 | 870 | Water / Wine |
| 32 | Rejuvenation |  rejuvenation | 980 | Water / Oil |
| 33 | Shrinking | 縮小 | 1215 | Water / Oil |
| 34 | Sleep | 睡眠 | 495 | Water / Wine |
| 35 | Slipperiness |  slippery | 685 | Water / Oil |
| 36 | Slowness | 遲緩 | 660 | Water / Wine |
| 37 | Stench | 惡臭 | 645 | Water / Oil |
| 38 | Stone Skin | 石膚 | 495 | Water / Oil |
| 39 | Strength | 力量 | 290 | Water / Wine |
| 40 | Swiftness | 迅捷 | 480 | Water / Wine |
| 41 | Wild Growth | 野蠻生長 | 330 | Water / Oil |

### 3.3 按章節解鎖順序

| 章節 | 可解鎖效果 |
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

---

## 四、煉金地圖：藥草與藥水的核心關聯

### 4.1 地圖機制

煉金地圖是藥水釀造過程的抽象空間可視化，每株草藥在地圖上繪製一段**方向路徑**：

1. **選擇基底** → 水（Water）、油（Oil）或酒（Wine），決定使用哪張地圖
2. **研磨素材** → 研磨程度（0%~100%）精確控制路徑長度（100%研磨 = 最短路徑）
3. **投入坩堝** → 素材的**元素屬性**決定路徑方向
4. **攪拌** → 藥水標記沿路徑不可逆地前進
5. **風箱加熱** → 到達效果標記時注入效果
6. **長柄勺微調** → 向地圖中心回拉，精確對齊效果輪廓

### 4.2 效果標記與品質判定

效果標記的**瓶身朝向**決定可達到的最高品質：
- **瓶口朝上** → 可達 Tier III（強效）
- **瓶口斜上** → 最高 Tier II（普通）
- **瓶口朝下** → 最高 Tier I（弱效，需用 Moon Salt 旋轉提升）

### 4.3 水基底 vs 油基底

| 特性 | 水基底（Water） | 油基底（Oil） |
|------|---------------|--------------|
| 解鎖方式 | 初始可用 | ~第 23 天後 8000 金幣購買 |
| 地圖佈局 | 內環直立 + 外環旋轉 | 外環直立 + 內環旋轉 |
| 特殊區域 | 骨牆分內外兩環 | 沼澤（Swamp）減速區 |
| 優勢 | 包含全部效果 | 防護藥水更容易達 Tier III |

### 4.4 地圖元素

- **漩渦（Whirlpools）**：加熱後旋轉吸引藥水標記，到達中心可傳送到地圖另一位置
- **骨頭（Bones）**：危險區域，接觸後藥水逐漸流失，完全流失則釀造失敗
- **經驗書（Experience Books）**：棕色書本標記，觸碰獲得經驗值

---

## 五、配方示例：藥草如何組合成藥水

### 5.1 水基底基礎配方（Tier III）

| 藥水 | 配方 |
|------|------|
| 治療藥水（Healing） | 1× Waterbloom（全研磨）+ 1× Mudshroom（全研磨） |
| 火焰藥水（Fire） | 4× Firebell（全研磨）+ 1× Terraria（整株） |
| 閃電藥水（Lightning） | 4× Windbloom（全研磨）+ 2× Waterbloom（全研磨） |
| 睡眠藥水（Sleep） | 4× Waterbloom（全研磨）+ 1× Terraria（全研磨） |
| 爆炸藥水（Explosion） | 3× Mad Mushroom（全研磨） |
| 冰霜藥水（Frost） | 3× Waterbloom（全研磨）+ 1× Windbloom（整株） |
| 力量藥水（Strength） | 3× Terraria（全研磨）+ 1× Firebell（整株） |
| 迅捷藥水（Swiftness） | 4× Windbloom（全研磨）+ 1× Waterbloom（全研磨） |
| 法力藥水（Mana） | 3× Witch Mushroom（全研磨）+ 1× Windbloom（整株） |
| 狂怒藥水（Rage） | 3× Bloodthorn（全研磨）+ 1× Firebell（整株） |

### 5.2 油基底進階配方

| 藥水 | 配方 |
|------|------|
| 強效黏合藥水 | 1× Thornstick（68%研磨）+ 1× Mudshroom（80%研磨）+ 1× Goldthorn（34%研磨）+ 1× Lifeleaf（全研磨） |
| 強效滑溜藥水 | 1× Witch Mushroom（全研磨）+ 1× Druid's Rosemary（全研磨）+ 1× Coldleaf（37%研磨）+ 1× Healers Heather |

---

## 六、藥草與藥水關聯總結

### 核心規則

1. **元素決定方向**：每種草藥所屬元素決定了它在煉金地圖上的行進方向（如 Firebell → 向西、Windbloom → 向北）
2. **研磨控制距離**：研磨程度精確控制路徑長度——完全研磨路徑最短，整株投入路徑最長
3. **組合導航**：組合不同方向的草藥，可在煉金地圖上繪製路徑到達任意效果節點
4. **對齊決定品質**：藥水標記與效果標記的**重疊精度**決定藥水品質（Tier I / II / III）
5. **基底切換地圖**：水/油/酒三種基底對應不同的煉金地圖佈局，同一藥水在不同基底地圖上的製作難度不同

### 系統關聯圖

```
草藥（元素+研磨度） → 煉金地圖路徑（方向+距離） → 到達效果標記 → 注入效果 → 藥水
                          ↑                            ↑
                      基底選擇（水/油/酒）          風箱加熱
```

---

## 七、進階技巧

### 7.1 多效混合藥水

到達一個效果節點注入效果後**不結束釀造**，繼續添加草藥前往第二個效果節點再注入，可製作出多種效果的混合藥水。注意部分效果互斥（如治療和毒藥）。

### 7.2 煉金機器（Alchemy Machine）

地下室的煉金機器可製作高級材料：

| 材料 | 功能 |
|------|------|
| Void Salt | 逐漸擦除已繪製的路徑 |
| Moon Salt | 逆時針旋轉藥水及其路徑（改變瓶身朝向） |
| Sun Salt | 順時針旋轉藥水及其路徑 |
| Life Salt | 恢復藥水生命值 |
| Philosopher's Salt | 將藥水拉向最近的效果 |
| Philosopher's Stone | 終極材料，完成 Magnum Opus |

### 7.3 顧客限制條件

部分訂單對素材類型有限制，影響配方設計：
- **Mixed**：允許所有素材 | **Organic**：禁止水晶
- **Herbal**：僅草藥 | **Fungal**：僅蘑菇
- **Cardinal**：僅 8 種基礎素材 | **Crystalline**：僅水晶

---

## 八、參考來源

- Potion Craft Fandom Wiki - Ingredients: https://potion-craft.fandom.com/wiki/Ingredients
- Potion Craft Fandom Wiki - Element Sorting: https://potion-craft.fandom.com/wiki/Element_Sorting
- Potion Craft Fandom Wiki - Alchemy Map: https://potion-craft.fandom.com/wiki/Alchemy_Map
- Potion Craft Fandom Wiki - Effects: https://potion-craft.fandom.com/wiki/Effects
- Potion Craft Fandom Wiki - Enchanted Garden: https://potion-craft.fandom.com/wiki/Enchanted_Garden
- Potion Craft Fandom Wiki - Oil Map: https://potion-craft.fandom.com/wiki/Oil_Map
- Potion Craft Fandom Wiki - Alchemy Machine: https://potion-craft.fandom.com/wiki/Alchemy_Machine
- Gamezebo - Potion Craft Maps: https://www.gamezebo.com/walkthroughs/potion-craft-maps/
- Gamezebo - Potion Craft Recipes: https://www.gamezebo.com/walkthroughs/potion-craft-recipes/
- Gameplay.tips - Ultimate Alchemy Guide: https://gameplay.tips/guides/potion-craft-alchemist-simulator-ultimate-alchemy-guide.html
- SuperCheats - Ingredients Guide: https://www.supercheats.com/potion-craft-alchemist-simulator-walkthrough-guide/ingredients-guide
- Steam Community Guide: https://steamcommunity.com/sharedfiles/filedetails/?id=2843913467

---

*報告生成日期：2026-06-10*
