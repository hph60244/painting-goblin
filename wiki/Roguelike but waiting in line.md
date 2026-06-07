---
tags: ['#idea', '#task/suspend', '#game', '#wip']
---

🥇 首選改造基底：Star Realms（極簡 Deck Combat Core）

Star Realms

為什麼適合你的遊戲

你的設計核心是：

排隊敵人（wave / queue）
快速戰鬥（short combat loop）
成長（群落發展 / 抗性）
道具給夥伴（buff transfer）

👉 這剛好對應 Star Realms 的三件事：

資源（Trade）
戰鬥（Combat）
HP（Authority）
🔪 你的「刪減版」做法（超重要）

把 Star Realms 壓縮成 「3種卡」版本：

① 攻擊卡（Red）
= 造成傷害
打倒「排隊的人」
② 防禦/抗性卡（Blue）
= 減少環境傷害 / boss aura / queue debuff
③ 成長卡（Green）
= 增加未來抽牌 / 永久buff / 給夥伴
⚡ 戰鬥流程（極簡版）

每回合：

抽 5 張
打出：
攻擊 → 打排隊最前方敵人
防禦 → 抵抗環境壓力（毒 / 壓迫 / 壓力條）
成長 → 強化群落
敵人前進一格（隊伍推進）

👉 這就變成：
“Slay the Spire，但沒有選路版，只剩線性隊列”

🧠 群落系統（你想要的核心）

你可以直接把 Star Realms Deck 改成：

個人牌庫 = 群落
每張卡 = 一個「角色 / 技能 / 生存能力」
群落成長：
卡可以升級（+1 damage / +shield）
或融合（兩張變一張進化卡）
🎁 道具給夥伴（你特別想要的點）

在 Star Realms 刪減版裡做：

「裝備卡」
不是打出，而是貼在某個單位上
效果：
+抗性
抗環境傷害
改變攻擊模式

👉 這會變成：
輕度 RPG 裝備系統（但仍是卡牌）

🥈 第二選擇：Yomi（最適合“快速戰鬥對戰”）

Yomi

為什麼它很適合你

Yomi 的核心其實是：

出牌 = 猜對手行為（攻 / 防 / 投）

非常適合你想要的：

快速戰鬥
排隊壓力
單次決策很重要
🔪 Yomi 刪減版（適配你的RPG）

把它砍成：

三種行動：
Attack（打前排）
Guard（減環境傷害）
Support（給隊友buff）
⚡ 戰鬥節奏（超快）

每一「排隊事件」：

每個玩家選 1 張牌
同時翻開
結算：
行動	結果
Attack vs no Guard	成功擊殺
Guard vs Environment	減傷
Support	buff下一輪

👉 這種版本可以做到：
1場戰鬥 30–60 秒

🥉 第三選擇（如果你想更 roguelike）

Scoundrel

適合點
已經是「一維 dungeon / card crawl」
很接近你的“排隊壓力 + 環境變化”

但缺點：

偏單人
戰鬥不是很“卡牌對戰”
🎯 給你的最推薦組合（實用答案）

如果你要做 MVP：

👉 用這個混合架構：
核心戰鬥
Yomi（快速決策）
成長系統
Star Realms（deck + upgrade）
地圖結構
Scoundrel（線性房間 = 排隊）
🧩 最終壓縮版設計（你的遊戲應該長這樣）
一維RPG：Queue Survivor
loop：
看排隊（敵人 1–5）
抽 3–5 張牌
出牌：
打前排
抗環境
強化群落
敵人推進
掉血（時間壓力）

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
