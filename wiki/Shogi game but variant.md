---
tags: ['#idea', '#task/suspend', '#game', '#wip']
---

將棋環境變化設計（完整版）
一、地形 / 空間改變類
流沙／沼澤
棋盤上特定格子（如中央 3×3）為流沙區。任何棋子進入後，每回合結束時自動下沉一格（向王將方向移動一排）。沉到最後一排時移除遊戲（不可打入）。

成子（と金）不受流沙影響。

鏡像空間
每 4 回合觸發一次，棋盤左右反轉。所有棋子的位置映射到另一側（1 列 ↔ 9 列）。持駒不受影響。

觸發前 1 回合預告。

升降梯
特定列（如 3、5、7 列）每回合可讓棋子向上或向下「傳送」2 排（不視為移動，不消耗回合，不能穿過敵棋）。傳送後該回合不能再移動。

傾斜棋盤（風）
每回合結束時，所有棋子向棋盤某一側移動一格（風向每 3 回合改變：東／西／南／北）。移出棋盤則移除，王將被推出即敗北。

風向提前 1 回合顯示。

黑洞
棋盤中央（如 5 五）出現黑洞，任何棋子進入即被移除（不可打入）。黑洞每 4 回合向敵方王將方向移動一格。移動前預告路徑。

進階：黑洞吸入棋子後成長為 2×2。

磁極
棋盤四角設磁極（++、--）。金將、飛車：正極；銀將、角行：負極；步卒等：中性。相鄰正負極互相吸引，同性互相排斥。

可消耗持駒「消磁」一個棋子一回合。

二、生態 / 生物類
棋盤花園（荊棘）
空格每回合 30% 機率長出荊棘。進入荊棘格需消耗 2 步移動力，停留一回合損失一個持駒。連續 3 回合荊棘則長成大樹（完全阻擋）。

停留一回合可清除（仍損失持駒）；飛車、角行可遠程砍伐。

遷徙季節
每 5 回合，所有成子棋子（と金、成銀等）自動向敵陣移動一格。

王將成子不受影響。

共生與寄生
不同種類棋子相鄰 → 共生：移動力 +1。

相同種類相鄰超過 2 回合 → 寄生：其中一個被吸收（移除），另一個獲得被吸收者的移動方式。

王將若被寄生則立即敗北。

三、時間 / 回合節奏類
慢動作領域
棋盤上半區（敵陣 7～9 段）為時間緩慢區。進入該區的棋子下一回合無法移動。王將不受影響。

時光倒流
每 8 回合，棋盤狀態倒回 2 回合前（所有棋子位置、持駒恢復）。王將若在回溯期間被將死，回溯後仍算敗北。

四、資源 / 持駒與棋子狀態類
詛咒寶箱
打入持駒時隨機觸發效果：30% 正常打入、30% 立刻成子、20% 被詛咒（移動後回到持駒區）、20% 變成炸彈（三回合後爆炸，移除周圍 8 格內所有棋子）。

可選擇「安全打入」（放棄隨機）。

飢餓模式
每 5 回合，持駒數量最多的一方必須棄掉一半持駒給對手。棄掉的持駒隨機選擇。

棋子疲勞
棋子在場上連續停留超過 4 回合後，移動力減 1（最少 1 格）。打入後重新計算。王將、金將不受影響。

通貨膨脹
持駒價值隨遊戲進行改變：

前 10 回合：步卒=1，金將=5

10–20 回合：步卒=2，金將=8

20 回合後：步卒=4，金將=12

打入棋子需消耗價值點數（每回合恢復固定點數）。

黑市
每回合可選擇：

賣出：2 個步卒 → 1 個隨機棋子

買入：消耗 3 個持駒 → 選擇一個已被吃的棋子（對方可截標）。

五、隨機 / 機率類
迷霧戰爭
每回合隨機隱藏棋盤上 3 個敵方棋子的種類（用蓋牌表示），只能看到位置。王將永遠可見，成子後自動揭露。

占卜師
每回合可選擇不移動，改為預測下一回合的環境變化。預測正確 → 獲得一個額外持駒步卒；預測失敗 → 該回合直接結束。

六、氣候 / 天象類
日蝕與月蝕
日蝕（每 8 回合）：所有棋子移動力減半（最少 1 格），持續 2 回合。

月蝕（日蝕後 2 回合）：所有棋子移動範圍變成 L 型（如桂馬），持續 1 回合。

酸雨
每回合隨機 3 格下酸雨。停留效果：

1 回合：移動力 -1

2 回合：降級（と金→步卒）

3 回合：移除

酸雨區提前 1 回合標記。

七、觸發式陷阱（與玩家行動掛鉤）
血債
每當吃掉對方一個棋子，自己必須棄掉一個同類型的持駒（若無則損失一個隨機持駒）。成子後吃子仍算原棋子類型。

復仇火焰
棋子被吃掉後，原本的位置變成火焰格，停留一回合會損失一個隨機持駒。火焰 3 回合後熄滅。

連鎖成子
當一個步卒成子（と金）時，與它相鄰（上下左右）的己方步卒強制也成子（若未成子）。連鎖成子的と金不再觸發連鎖。

回聲
移動棋子後，原位置產生「回聲」。下回合若敵方棋子進入該位置，會被彈回原位（不消耗對方回合）。

鏡像反擊
吃掉對方棋子後，自己下回合必須以相同方式移動一次（例如用桂馬吃，下回合必須再用桂馬移動）。

八、極簡快速變化（短對局）
名稱	機制	節奏
潮汐	每 2 回合，棋盤下半部與上半部的棋子交換位置（整排移動）	極快
計時炸彈	每方有一個炸彈棋子（取代一個步兵）。每停留一回合爆炸範圍 +1，3 回合後炸掉周圍 3×3	壓力
九、最後一排燒毀（原核心機制）
焚毀方式
定時焚毀：每固定回合數（如每 5 回合），最後一排最左／最右一格消失。

逐格擴散：從角落開始，每回合一格火焰蔓延，不可逆。

條件觸發：棋子被吃掉時，該棋子原本所在直線的最後一排燃燒一格。

效果
該格永久無法進入或停留（視同牆壁）。

若棋子停留在即將燒毀的格子：

提前一回合警告（火焰標記）

若不撤退：棋子與格子一起消失（不得打入）

王將特殊規則
王將所在格即將被燒 → 必須在燃燒回合前離開，否則直接敗北。

與打入互動
被燒毀的格子不能打入棋子。

可補充規則：步卒在倒數第二排就直接成子，補償底線消失。

推薦組合包
組合	內含機制	對局長度
天災	傾斜棋盤 + 酸雨 + 時間裂縫	中
經濟戰	通貨膨脹 + 黑市 + 共生/寄生	長
快速派對	潮汐 + 命運輪盤 + 計時炸彈	短（10分鐘）
火焰末日	最後一排燒毀 + 復仇火焰 + 血債	中短

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
