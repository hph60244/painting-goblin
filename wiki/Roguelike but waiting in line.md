---
tags: ['#idea', '#task/suspend', '#game', '#wip']
---

# 一維排隊 Yomi RPG（MVP完整規格）

---

# 🧠 1. 核心概念

本遊戲是一個：

> 基於 Yomi（同步猜拳戰鬥）的「一維排隊生存RPG」

核心由三件事構成：
- ⚔️ Yomi戰鬥（決策）
- 🚶 隊列推進（壓力）
- 🔁 規則變化（環境 + 夥伴）

---

# 📏 2. 世界結構（一維隊列）

[終點獎品（有限）]
↑
敵人隊列
↑
玩家隊列（含夥伴）
↑
入口

規則：
- 只有最前線進入戰鬥
- 所有單位單向前進
- 玩家永遠在隊列中

---

# ⚔️ 3. 戰鬥系統（Yomi）

## 🃏 最小牌組（3張）

### Attack（攻擊）
- 勝利：造成2傷害
- 平手：雙方各受1傷害
- 失敗：無效果

---

### Block（防禦）
- 勝利：免疫傷害 + 停止推進
- 平手：減傷1
- 失敗：受到1傷害

---

### Support（支援）
- 勝利：減少疲勞 / 延緩推進
- 平手：無效果
- 失敗：觸發敵方小推進

---

## 流程
1. 同時選牌
2. 揭示
3. 結算Yomi
4. 影響HP / 推進 / 疲勞

---

# 🚶 4. 隊列推進系統

每 N 次玩家行動 → 隊列前進 1 格

建議 N：
- 緊張：2～3
- 標準：3～4
- 策略：5

---

# 💀 5. 玩家系統（疲勞/插隊）

## 核心規則

- 玩家永遠在隊列中
- 戰敗不死亡，而是累積疲勞

---

## 疲勞效果

HP歸零 → 疲勞 +1

疲勞效果：
- 排隊順位下降
- 被NPC插隊
- 支援能力下降（可選）

---

## 插隊機制

- 疲勞越高 → 被插隊機率越高
- 或直接後退1～2格

---

# 👾 6. 敵人設計模板

名稱
HP
行為傾向
特殊規則
掉落效果

---

## 範例

### 哥布林
- HP: 2
- Attack型
- 攻擊失敗仍推進
- 無掉落

---

### 盾兵
- HP: 3
- Block型
- Block成功反擊
- 消除疲勞

---

### 狂戰士
- HP: 2
- Attack型
- 平手仍造成1傷害
- 解鎖Rush

---

### Boss
- HP: 6
- 不可擊退
- 每回合額外推進
- 解鎖環境

---

# 🤝 7. 夥伴系統

## 本質

> 夥伴 = 改變Yomi規則，而非數值

---

## 能力池（20種）

### 戰鬥型
- 騎士：Block成功反擊
- 狂戰士：平手仍傷害
- 刺客：無視Block
- 獵人：先手
- 守衛：減傷1

---

### 節奏型
- 僧侶：減少疲勞
- 鼓手：推進減緩
- 工程師：降低推進速度
- 時間術士：凍結推進
- 舞者：Support強化

---

### 資訊型
- 斥候：預覽敵人
- 占卜師：提示Yomi
- 間諜：偷看牌
- 記錄者：顯示克制
- 賭徒：高風險高回報

---

### 戰術型
- 鍛造師：穿透攻擊
- 鍊金術士：Support轉傷害
- 弓手：打後排
- 破壞者：Block推進敵人
- 靈媒：免疫疲勞

---

# 🌪️ 8. 環境系統

## 本質

> 改變Yomi規則

---

## 15種環境

### 節奏變化
- 暴風雨：Support削弱
- 黑夜：資訊不完整
- 地震：Block失效
- 大霧：隨機行動
- 乾旱：Support無效

---

### 壓力型
- 崩塌通道：額外推進
- 擁擠隊列：插隊+50%
- 饑荒：每回合疲勞+1
- 瘟疫：全體HP-1
- 混亂：順序打亂

---

### 規則型
- 攻擊強化：Attack +1
- 防禦時代：Block停止推進
- 支援時代：Support強化
- 高速通道：推進減少
- 崩壞秩序：隊列隨機交換

---

# 📊 9. 平衡推進公式

每 N 次玩家行動 → 隊列前進 1 格

---

## N值修正

N = 基礎值 + 環境 + 夥伴

---

## 疲勞影響

- 每層疲勞 → 插隊機率 +10%
- 3層以上 → 推進加速

---

# 🏁 10. 終點系統

- 終點獎品有限
- 敵人到達會消耗獎品
- 形成競爭壓力

---

# 🧍 11. 玩家死亡規則

HP歸零 → 疲勞 +1 → 排隊順位下降 → 被插隊

本質：
> 玩家不是死亡，而是失去排隊優先權

---

# 🎮 12. 核心循環

隊列推進
↓
Yomi戰鬥
↓
勝利 → 推進 / 獎勵
↓
失敗 → 疲勞 + 插隊風險
↓
夥伴 / 環境改變規則
↓
重複直到終點

---

# 🧠 13. 一句話總結

這是一個以 Yomi 戰鬥為核心，在一維排隊壓力中推進，透過夥伴與環境改變規則，並在有限終點資源競爭下進行的策略型生存遊戲。

---

# 🃏 Yomi卡牌強化方案設計（規格）

---

# 🎯 核心概念

Yomi卡牌的強化不是數值升級，而是：

> 改變「勝負判定方式」與「戰鬥規則結構」

強化只影響三件事：
- ⚔️ 勝負結果如何結算
- 🤝 平手如何處理
- 🌪️ 卡牌如何影響隊列 / 疲勞 / 環境

---

# 🧩 強化設計維度（6種）

---

# 🥇 1. 結果強化（Outcome Boost）

提升「勝利/平手/失敗」的效果。

## Attack+
- 勝利：2 → 3傷害

## Block+
- 勝利：免傷 + 反擊1

## Support+
- 勝利：疲勞 -2 或推進延後

---

👉 特點：最基礎強化，不改規則，只改結果

---

# 🥈 2. 勝負改寫（Rule Break）

改變Yomi對抗關係。

## Feint型
- 對 Block：視為勝利
- 對 Attack：視為失敗
- 對 Support：平手→勝利

## Counter型
- 對指定行動自動勝利

---

👉 特點：改心理戰與預判

---

# 🥉 3. 平手強化（Tie Enhancement）

強化Yomi最常見區間（平手）。

## Stable Attack
- 平手 → 2傷害

## Safe Block
- 平手 → 無傷 + 不推進

## Soft Support
- 平手 → 減1疲勞

---

👉 特點：讓「猜平手」變成策略核心

---

# ⚡ 4. 隊列互動強化（Queue Impact）

影響排隊系統（核心特色）。

## Push Attack
- 勝利：+1隊列推進

## Anchor Block
- Block成功 → 後方敵人停止1次

## Flow Support
- Support成功 → 推進延後（N + 1）

---

👉 特點：讓戰鬥影響整條隊列

---

# 💀 5. 疲勞操控強化（Fatigue System）

影響插隊與順位。

## Clean Mind
- 勝利 → 疲勞 -2

## Pressure Strike
- 勝利 → 對手疲勞 +1

## Last Stand
- HP越低 → 攻擊越強

---

👉 特點：控制「排隊順位壓力」

---

# 🌪️ 6. 規則改寫強化（System Override）

最高級強化，直接改系統。

## Weather Control
- 改變當前環境效果

## Rule Override
- 忽略本回合環境

## Safe Path
- 推進延後一次

---

👉 特點：改變整局遊戲節奏

---

# 🏁 強化等級分類

---

## 🟢 普通強化（數值型）
- +傷害
- 小幅疲勞變動
- 平手小強化

---

## 🟡 稀有強化（規則型）
- 改平手結果
- 特定克制關係
- 反擊機制
- Yomi條件變更

---

## 🔴 傳說強化（系統型）
- 改隊列推進N值
- 改插隊規則
- 改環境效果
- 改勝負判定邏輯

---

# 🧠 設計核心原則

## ✔ 強化必須做到其中一件：
- 改變勝負結果
- 改變平手行為
- 改變隊列結構
- 改變疲勞機制
- 改變環境規則

## ❌ 禁止：
- 純數值膨脹（無系統影響）
- 永久壓制型效果
- 不影響Yomi決策的buff

---

# 🎮 一句話總結

> Yomi卡牌的強化，是在擴展「猜拳規則本身」，而不是單純提升數值。

---

- one dimension rpg
- goal is beating people in the waiting line for prize
- 需要排隊遊戲獨特的挑戰
    - 群落發展
    - 排隊時抵抗環境變化
        - project zomboid
            - [https://pzwiki.net/wiki/Moodles/zh](https://pzwiki.net/wiki/Moodles/zh)
            - [https://playgame.wiki/projectzomboid/gonglue/all](https://playgame.wiki/projectzomboid/gonglue/all)
            - 失血
            - 感冒
            - 負重
            - 過熱
            - 受寒
            - 飢餓 Hunger
            - 受傷 [https://pzwiki.net/wiki/Health#Types_of_Injuries](https://pzwiki.net/wiki/Health#Types_of_Injuries)
            - 生病
            - 口渴 Thirst
            - 淋濕
        - don't starve
            - 機制
                - [https://dontstarve.fandom.com/zh/wiki/生命](https://dontstarve.fandom.com/zh/wiki/%E7%94%9F%E5%91%BD)
                - [https://dontstarve.fandom.com/zh/wiki/理智](https://dontstarve.fandom.com/zh/wiki/%E7%90%86%E6%99%BA)
                - [https://dontstarve.fandom.com/zh/wiki/潮濕](https://dontstarve.fandom.com/zh/wiki/%E6%BD%AE%E6%BF%95)
                - [https://dontstarve.fandom.com/zh/wiki/過熱](https://dontstarve.fandom.com/zh/wiki/%E9%81%8E%E7%86%B1)
                - [https://dontstarve.fandom.com/zh/wiki/寒冷](https://dontstarve.fandom.com/zh/wiki/%E5%AF%92%E5%86%B7)
                - [https://dontstarve.fandom.com/zh/wiki/飢餓](https://dontstarve.fandom.com/zh/wiki/%E9%A3%A2%E9%A4%93)
                - [https://dontstarve.fandom.com/zh/wiki/光源類](https://dontstarve.fandom.com/zh/wiki/%E5%85%89%E6%BA%90%E9%A1%9E)
                - [https://dontstarve.fandom.com/zh/wiki/中毒](https://dontstarve.fandom.com/zh/wiki/%E4%B8%AD%E6%AF%92)
            - 環境
                - [https://dontstarve.fandom.com/zh/wiki/日夜週期](https://dontstarve.fandom.com/zh/wiki/%E6%97%A5%E5%A4%9C%E9%80%B1%E6%9C%9F)
                - [https://dontstarve.fandom.com/zh/wiki/雨天](https://dontstarve.fandom.com/zh/wiki/%E9%9B%A8%E5%A4%A9)
                - [https://dontstarve.fandom.com/zh/wiki/強風](https://dontstarve.fandom.com/zh/wiki/%E5%BC%B7%E9%A2%A8)
                - [https://dontstarve.fandom.com/zh/wiki/閃電](https://dontstarve.fandom.com/zh/wiki/%E9%96%83%E9%9B%BB)
                - [https://dontstarve.fandom.com/zh/wiki/火山](https://dontstarve.fandom.com/zh/wiki/%E7%81%AB%E5%B1%B1)
    - 選定道具，可贈與點到的夥伴，強化他們的抗性
        - 每個夥伴顯示需求按鈕，減少查看操作
    - 狀態影響
        - progress bar ui
        - game control script
        - day and night : sanity
        - item ui
        - 插隊系統
        - rain : stamina
        - ice land and snow : hp
        - desert and heat : hp
        - lightening : hp
        - load : stamina
        - storm : stamina
        - fog : hp
- 可郵購道具ubersheep, 晚上發生插隊事件, 限量
- Reference
    - [pet](https://assetstore.unity.com/packages/3d/characters/animals/animal-pack-deluxe-v2-144071)
    - [define game goal](https://assetstore.unity.com/packages/vfx/shaders/heat-haze-effect-53714)
    - [https://www.youtube.com/watch?v=0jexhkwCGOc&ab_channel=阿津](https://www.youtube.com/watch?v=0jexhkwCGOc&ab_channel=%E9%98%BF%E6%B4%A5)
- iso map
    - [https://blog.unity.com/technology/isometric-2d-environments-with-tilemap](https://blog.unity.com/technology/isometric-2d-environments-with-tilemap)
    - [https://www.youtube.com/watch?v=tW744Zgc1YY&ab_channel=Sykoo](https://www.youtube.com/watch?v=tW744Zgc1YY&ab_channel=Sykoo)
    - [https://www.youtube.com/watch?v=tywt9tOubEY&ab_channel=Unity](https://www.youtube.com/watch?v=tywt9tOubEY&ab_channel=Unity)
