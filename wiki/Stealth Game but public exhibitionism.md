---
tags: ['#idea', '#task/suspend', '#game', '#wip']
---

- [[Job Description]]
- [[Open world place]]
- [[Modern Tileset]]
- [[DLsite Tags]]

-

# 基本概念

- 生物需求按照[馬斯洛分級](https://en.wikipedia.org/wiki/Maslow%27s_hierarchy_of_needs)
- 需求的高低影響[情緒](https://en.wikipedia.org/wiki/Emotion_classification#Plutchik's_wheel_of_emotions)
- 需求與情緒[培養關係](https://en.wikipedia.org/wiki/Interpersonal_relationship)
- 行為根據需求分類
- 感知與行為都有LOD

# 時間(Time)

- 可互動時遊戲內1分鐘等於現實1秒
	- 遊戲內1秒 = 1 [tick](https://dwarffortresswiki.org/index.php/Time#Basic_mechanics)
	- 現實1秒 = 60 tick
- 純模擬時，現實1秒跑的tick沒上限
- 每日時段
	- Morning : 6:00 — 9:59
	- Day : 10:00 — 17:59
	- Evening : 18:00 — 20:59
	- Night : 21:00 — 5:59
- 暫時沒有[曆法](https://dwarffortresswiki.org/index.php/Calendar)

# 空間(Space)

- 代表一個3維格狀空間
- 用3個整數定義長寬高

# 實體(Entity)

- 表示可以互動的物件
- 實體可包含其他實體
- 實體可查詢內部實體的資料
- 有空間屬性就可限制所包含的實體
	- 實體不超出所屬空間
	- 實體移動時可作碰撞判定

# Role - Creature
## 參數(Parameter)

- Max Health : 血量上限
- Max Stamina : 體力上限
- Max Food : 進食上限
- Max Waste : 排泄物上限
- Recovery Speed : 恢復速度
- Digestion Speed : 消化速度
- Waste Rate : 代謝物生成比

## 狀態(State)

- Food
	- 根據Digestion Speed減少
	- 減少時增加Stamina
	- 減少時增加Waste
- Waste
	- 全滿時強制排出
- Stamina
	- 根據Recovery Speed減少減少時增加Health
- Health
	- 歸零時死亡

## 需求([Need](https://sims.fandom.com/wiki/Motive#The_Sims_4))

- Hunger
	- = Food / Max Food
	- Need 'Eat'
	- 歸零時餓死
- Bladder
	- = Waste / Max Waste
	- Need 'Toilet'
- Energy
	- = Stamina / Max Stamina
	- Need 'Sleep'
	- 歸零時昏倒
- Hygiene
	- Need 'Clean'

## 感知(Sensor)
## 行為(Action)

- Low Hunger找Food吃
- Low Blasser找地方排泄
- Low Energy找地方Sleep
- Low Hygiene找地方Clean

# Role - Creature - Human

需求([Need](https://sims.fandom.com/wiki/Motive#The_Sims_4))

- Social?
	- decreased mood
- Fun?
	- decreased mood

- Component
	- Graphic
	- Inventory
	- Role
	- Interaction
	- Zone
- Role
	- Need
	- Sensor
	- Activity
- Place???
	- Room
	- Building
	- Theme Park
	- Vehicle
		- overlay地圖
		- 背景移動
- Entity
	- Charactor
		- Graphic
		- Inventory
		- Role
		- Interaction
	- Item
		- Graphic
		- Interaction
	- Smart Object
		- Graphic
		- Interaction
		- Inventory?
	- Smart Zone
		- Zone
		- Sensor
		- Assign Role
	- Group
		- Assign Role

# 系統

- 靜態地圖尋路 : [Flow Field](https://github.com/D2klaas/Godot-4-VectorFieldNavigation)
- 長距離尋路 : Hierarchical A*
- 團體移動 : Flocking
- 內在需求 : [[Utility AI]]
- 特質偏好 : Trait System
- 警戒狀態 : FSM
- 紙娃娃 : [LPC](https://godotengine.org/asset-library/asset/2212),[Layer](https://web.archive.org/web/20250814073702/https://bztsrc.gitlab.io/lpc-refined/#modular_layers),[gen](https://github.com/LiberatedPixelCup/Universal-LPC-Spritesheet-Character-Generator),addon,[tool](https://github.com/bluecarrot16/lpctools/blob/main/tests/arrange_files/layout/universal.png)
- 玩家互動 : Reaction Matrix
- NPC互動 : Reaction Matrix
- 行程規劃 : Schedule Template
- 任務規劃 : [HTN](https://github.com/fnaith/godot-fluid-hierarchical-task-network)
- 團隊任務 : Group Agent
- 感知係數 : [ADSR](https://github.com/Boyquotes/godot-adsr-envelope)
- 感知玩家 : Stim Event([視](https://github.com/d-bucur/godot-vision-cone)/聽/[嗅覺](https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms))
- 感知NPC : Stim Event
- 互動物件 : Smart Object
- 人流控制 : Smart Zone
- 部位屬性 : emuera
- 人際關係 : the simes ???

# 整合系統

- 工作
	- 工作場所提供職位
	- 職位需要完成各種活動
	- NPC選擇活動
	- 工作場所指示活動如何執行
	- Ex. [Casher](https://www.mymajors.com/career/cashiers/)

# 野外露出

- 遊戲體驗 : 提供高自由度的露出場景與互動方式
- 背景設定 : 轉生蘿莉沉迷露出自慰
- 遊戲核心
	- 接受指定任務
	- 野外露出拍片
	- 回家賣影片
- End Game : 完成全任務
- 玩家行動
	- 家中活動
		- 接任務
		- 賣影片
		- 購買衣裝
	- 戶外活動 : 拍露出影片
- 玩法
	- 單一存檔
	- NPC偵測
	- NPC誘導
	- NPC無力化
	- 定義安全場所
	- 隱蔽移動
	- 被感知時
		- 擺脫感知+換裝 : 繼續任務
		- 立刻逃離 : 暫時無法進入該區域

- 任務內容
	- 指定活動地點(直接傳送)
	- 衣裝 : 感知係數
	- 行動 : 感知係數
	- 其他 : 被感知程度
- 活動地點
	- 包含多個互動物件
	- 人流控制
- NPC設置
	- 靜態地圖尋路
	- 感知玩家
	- 玩家互動
	- 警戒狀態
	- 任務規劃
		- 提供服務
		- 維護工作區

# 透明人間

- 遊戲體驗 : 提供高自由度的調教NPC方式
- 背景設定 : 無知魔女收集素材破解存在消除詛咒
- 遊戲核心 :
	- 選擇目標NPC
	- 使用技能影響NPC
	- 收集素材
		- 男 : 精液
		- 女 : 調教刻印(恥情之珠)
- End Game : 收集足夠素材
- 玩家行動

- 刺激NPC消除抵抗
	- 調教NPC收集素材
	- 用素材升級技能 : 敏感度等
- 玩法
	- 單一存檔
	- NPC鑑定
	- NPC誘導
	- NPC無力化
	- 定義安全場所
	- 被感知時
		- NPC逃走 : 警戒升級
		- NPC警戒 : 無法調教
		- 使用技能 : 繼續調教
- 地圖設置
	- 世界地圖
		- 包含多個活動地點
		- 道路 : 地點間轉移用
	- 活動地點
		- 包含多個互動物件
		- 人流控制
		- NPC住家
- NPC設置
	- 部位屬性
	- 行程規劃
	- 長距離尋路
	- 靜態地圖尋路
	- 感知玩家
	- 玩家互動
	- 感知NPC
	- NPC互動

- 警戒狀態
	- 任務規劃
		- 工作時段
- 提供服務
- 維護工作區
		- 生活時段
- 使用服務
- 內在需求
- 特質偏好
		- 回家時段
- 其他活動

催眠?憑依/常識變換

- 遊戲體驗 : 提供高自由度侵蝕NPC生活的方式
- 背景設定 : 邪神與信徒間建立連結，增強力量
- 遊戲核心 :
	- 選擇目標NPC
	- 使用技能調教NPC
	- 收集素材
		- 男 : 精液
		- 女 : 調教刻印
- End Game : 收集足夠素材
- 玩家行動
	- 刺激NPC消除抵抗
	- 調教NPC收集素材
	- 用素材升級技能 : 敏感度等
- 玩法

- 單一存檔
	- NPC鑑定
	- NPC誘導
	- NPC無力化
	- 定義安全場所
	- 被感知時
		- NPC逃走 : 警戒升級
		- NPC警戒 : 無法調教
		- 使用技能 : 繼續調教
- 地圖設置
	- 世界地圖
		- 包含多個活動地點
		- 道路 : 地點間轉移用
	- 活動地點
		- 包含多個互動物件
		- 人流控制
		- NPC住家
- NPC設置
	- 人際關係
	- 團隊任務
	- 部位屬性
	- 團體移動
	- 行程規劃
	- 長距離尋路
	- 靜態地圖尋路
	- 感知玩家
	- 感知NPC
	- 警戒狀態
	- 任務規劃
		- 工作時段

- 提供服務
- 維護工作區
	- 生活時段
- 使用服務
- 內在需求
- 特質偏好

- 以下還不知道怎麼弄成遊戲------

- NPC姦
- ABO
- 模擬交通
- 模擬經濟
- 模擬建築
- 模擬都市規劃
- 模擬新生世代
- 模擬產業升級
- 模擬政治
