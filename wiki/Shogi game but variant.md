---
tags: ['#idea', '#task/suspend', '#game', '#wip']
---

把「將棋」加入「環境變化（Environmental Dynamics）」後，可以從純粹的盤面博弈，變成「局面＋地圖控制」的混合策略遊戲。

核心設計目標

傳統將棋：

變數主要來自玩家
棋盤永遠固定 9×9
駒性能固定

環境將棋：

變數來自地圖
棋盤會改變
駒性能可能受到影響
方案一：天候將棋

每隔 N 回合天氣變化。

晴天

正常規則。

雨天

飛車、龍王移動距離 -2

例如：

原本：

飛車
↑↑↑↑↑↑↑↑

變成：

飛車
↑↑↑

效果：

遠程火力下降
步兵與銀將價值上升
大霧

只能看到：

自己駒
周圍2格

變成半完全資訊遊戲。

暴風雪

所有駒移動力 -1

金將：

□○□
○金○
○○○

↓

□○□
○金○
□□□
方案二：地形生成將棋

棋盤存在地形。

森林
FFF
FFF
FFF

進入後：

移動停止
無法穿越
河流
~~~~

步兵：

不能通過

飛車：

可跨越

山岳
MMM

駒在山上：

防禦+1
被取需要兩次攻擊
方案三：地城將棋

每回合地圖變化。

地板崩塌
□□□
□■□
□□□

變成：

□□□
□X□
□□□

駒掉落即死亡。

牆壁生成
□□□□□

↓

□□#□□

形成新的障礙。

傳送門
A → B

駒進入A：

直接到B。

方案四：元素將棋

盤面累積元素。

火區域

每回合：

駒受1傷害

（引入HP系統）

冰區域

滑行規則：

→
→
→

直到撞牆。

雷區域

每3回合：

× × ×
× 雷 ×
× × ×

範圍傷害。

方案五：季節將棋

每10回合換季。

春

步兵移動+1

夏

飛車強化

秋

角行強化

冬

王將周圍獲得護盾

方案六：影牢式將棋

很適合你之前提到的《影牢》。

盤面有陷阱。

落穴
O

踩到：

直接死亡

彈簧
S

踩到：

彈飛3格

滾石

啟動後：

→→→→

路徑上全部撞飛。

火焰噴射
^^^^

直線攻擊。

方案七：活棋盤

棋盤本身會移動。

例如每5回合：

ABC
DEF
GHI

變成：

DEF
GHI
ABC

整列輪轉。

或者：

A B C

↓

C A B

行列移動。

玩家不只要算駒，還要算地圖未來變化。

最有潛力的組合

若目標是做成獨立遊戲，我會推薦：

將棋 + Into the Breach 式預告機制 + 影牢陷阱系統

特色：

完全資訊
無隨機
每回合顯示環境下一步變化
陷阱可被雙方利用
棋盤持續改變

例如：

回合 12

下回合：
第4列崩塌
第7行火焰噴射
傳送門移動

玩家必須同時考慮：

將棋吃子
王將安全
陷阱連鎖
地圖未來狀態

這樣會從傳統將棋進化成一種「環境戰術將棋（Environmental Shogi）」類型。

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
