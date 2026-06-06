# 《Deception IV: Blood Ties》陷阱細節規格報告

## 概述

《Deception IV: Blood Ties》（日版名《影牢 ダークサイド・プリンセス》）是 Tecmo Koei 於 2014 年發售的策略遊戲，屬於《 Deception 》系列（影牢系列）的第四代作品。遊戲核心玩法為運用各種陷阱來擊敗敵人。

---

## 一、陷阱分類與完整列表

### 1. 物理/撞擊類陷阱

| 陷阱名稱 | 效果描述 | 觸發方式 |
|---------|---------|---------|
| 滾動巨石 (Rolling Boulder) | 巨大岩石滾動碾壓路徑上所有敵人 | 地面觸發 |
| 彈簧板 (Spring Board) | 將敵人彈飛至空中或撞向其他陷阱 | 踩踏觸發 |
| 釘牆 (Spiked Walls) | 牆壁伸出尖刺攻擊敵人 | 靠近觸發 |
| 擺錘 (Pendulum) | 巨大擺錘橫向擺動撞飛敵人 | 經過觸發 |
| 人體大砲 (Human Cannon) | 將敵人發射出去 | 踩踏觸發 |
| 掉落浴缸 (Falling Bathtub) | 浴缸從天而降砸中敵人 | 下方經過觸發 |
| 魔法列車 (Magic Train) | 列車高速衝撞路徑上所有敵人 | 地面觸發 |
| 火車頭 (Locomotive) | 火車頭碾壓敵人 | 地面觸發 |
| 格林箭矢 (Gatling Arrow) | 連續發射多支箭矢射穿敵人 | 經過觸發 |
| 圓鋸 (Circular Saw) | 旋轉鋸片切割敵人 | 地面觸發 |
| 斷頭台刀刃 (Guillotine Blade) | 刀刃從天而降斬擊 | 下方觸發 |

### 2. 電擊/火焰類陷阱

| 陷阱名稱 | 效果描述 | 觸發方式 |
|---------|---------|---------|
| 電擊 (Electrocution) | 高壓電流電擊敵人使其痙攣 | 踩踏觸發 |
| 火焰 (Fire) | 噴射火焰焚燒敵人 | 經過觸發 |
| 火花棒 (Spark Rod) | 電擊棒攻擊敵人 | 靠近觸發 |

### 3. 束縛/控制類陷阱

| 陷阱名稱 | 效果描述 | 觸發方式 |
|---------|---------|---------|
| 捕獸夾 (Bear Trap) | 夾住敵人腿部使其無法移動 | 踩踏觸發 |
| 真空牆 (Vacuum Wall) | 產生強大吸力吸附敵人 | 靠近觸發 |
| 夾頭旋轉金屬器 (Head-grabbing Spinner) | 夾住敵人頭部旋轉 | 經過觸發 |

### 4. 趣味/羞辱類陷阱

| 陷阱名稱 | 效果描述 | 觸發方式 |
|---------|---------|---------|
| 香蕉皮 (Banana Peel) | 使敵人踩到滑倒 | 踩踏觸發 |
| 飛翔蛋糕 (Flying Cake) | 射出蛋糕砸向敵人臉部 | 經過觸發 |
| 生日蛋糕 (Birthday Cake) | 蛋糕陷阱攻擊 | 踩踏觸發 |
| 南瓜頭 (Pumpkin Head) | 給敵人戴上南瓜頭 | 經過觸發 |

### 5. 經典刑具類陷阱

| 陷阱名稱 | 效果描述 | 觸發方式 |
|---------|---------|---------|
| 鐵處女 (Iron Maiden) | 將敵人關入尖刺囚籠 | 靠近觸發 |
| 廚房用具 (Kitchen Utensils) | 將廚具插在敵人頭上 | 經過觸發 |

### 6. DLC/特典陷阱 (The Nightmare Princess)

| 陷阱名稱 | 備註 |
|---------|------|
| 黃金馬桶 (Golden Toilet) | 日版預購特典 |
| 懷舊陷阱系列 (Nostalgia Traps) | 來自前作《Trapt》、《Deception III》等經典陷阱 |

---

## 二、陷阱系統機制

### 三種連鎖風格 (Trap Combo Styles)

遊戲中存在三種不同的陷阱連鎖風格，影響連鎖評價與獎勵：

| 風格 | 說明 | 獎勵對應 |
|------|------|---------|
| **Brutality（殘暴）** | 以暴力虐待為主的連鎖組合 | 取悅惡魔僕人 Caelea |
| **Magnificence（華麗）** | 以華麗表演為主的連鎖組合 | 取悅惡魔僕人 Veruza |
| **Humiliation（羞辱）** | 以羞辱敵人為主的連鎖組合 | 取悅惡魔僕人 Lilia |

### 連鎖系統

1. **基礎連鎖** - 兩個陷阱先後觸發：
   - 範例：捕獸夾 → 斷頭台刀刃（先固定再斬殺）
   - 範例：真空牆 → 魔法列車（先吸附再碾壓）

2. **三連鎖組合** - 三個陷阱接力：
   - 經典組合：香蕉皮（滑倒）→ 擺錘（撞飛）→ 鐵處女（穿刺）

3. **環境互動** - 地圖環境可用於增加額外傷害

### 陷阱操作機制

- **預先放置**：在關卡開始前或戰鬥中在指定位置設置陷阱
- **引誘觸發**：引導敵人走入陷阱範圍後手動或自動觸發
- **時機掌握**：太早或太晚觸發會影響連鎖效果與傷害輸出
- **自傷風險**：玩家也可能被自己設置的陷阱傷害
- **PS Vita 觸控**：Vita 版可透過觸控螢幕點選陷阱圖示來啟動

### 裝甲破壞系統 (Armor Break)

- 連續的陷阱連鎖可以破壞敵人的裝甲
- 裝甲破裂後敵人承受的傷害大幅提升
- 不同陷阱對裝甲的破壞效率不同

---

## 三、Nightmare Princess 新增要素

《Deception IV: The Nightmare Princess》（2015）新增以下內容：

### 新角色 Velguirie
- 可直接對敵人進行踢擊攻擊（不需依賴陷阱）
- 敵人倒地後可踩踏追加傷害
- 可將敵人踢入陷阱中啟動連鎖

### Quest Mode（任務模式）
- 收錄 100 個全新任務
- 可獲得新陷阱與能力
- 可解鎖前作女主角（Allura、Reina、Millennia）為可用角色

### Deception Studio（陷阱工作室）
- 自訂角色外觀
- 自訂敵人類型
- 自訂關卡配置
- 需透過 Quest Mode 收集零件

---

## 四、陷阱戰術建議

### 新手推薦組合
1. 捕獸夾 → 斷頭台 - 簡單有效的二連鎖
2. 香蕉皮 → 擺錘 → 鐵處女 - 基礎三連鎖

### 進階組合
1. 真空牆（固定）→ 圓鋸（切割）→ 魔法列車（碾壓）
2. 彈簧板（彈飛）→ 釘牆（撞擊）→ 火焰（焚燒）

### 刷分組合
- 華麗風格：使用多段陷阱連鎖，注重視覺效果
- 殘暴風格：選擇高傷害陷阱快速擊殺
- 羞辱風格：使用蛋糕、香蕉皮等搞笑陷阱

---

## 五、資料來源

- [Wikipedia - Deception IV: Blood Ties](https://en.wikipedia.org/wiki/Deception_IV:_Blood_Ties)
- [Siliconera - Every Form of Cartoon Torture](https://www.siliconera.com/deception-iv-every-form-cartoon-torture-youve-seen/)
- [Siliconera - Birthday Cake or Deadly Saw](https://www.siliconera.com/use-birthday-cake-deadly-saw-trap-deception-iv-blood-ties/)
- [Siliconera - Cute Ones That Always Trap You](https://www.siliconera.com/2013/12/30/cute-ones-always-trap-deception-iv-blood-ties/)
- [官方網站 - 特殊陷阱介紹](https://www.gamecity.ne.jp/kagero3-2/sp_trap.html)
