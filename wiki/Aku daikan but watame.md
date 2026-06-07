---
tags: ['#idea', '#task/suspend', '#game']
---

# Spec

## window

用滑鼠滾輪縮放
用滑鼠中鍵拖曳畫面
遊戲整體用2d地圖呈現3d效果
物體的基準點的y座標決定顯示順序，越下方越靠近玩家，會顯示在越上層
物體滯空時影子縮放呈現高度變化

## map struct

2d grid map，可以設定長寬，預設先用16x9格，零點在左上角
每格大小可設定，預設先用25x25 pixel
格子為空時顯示為純白方形
格子有牆時，顯示為純黑方形，預設把地圖最外圈圍住，只留內部14x7格可活動

## character

角色位置基準點用一個(x,y)決定，以此為中心碰撞判定可以設定長寬，預設先用9x9 pixel
角色顯示時用一個sprite，大小可設定，預設先用25x25 pixel
角色腳底用灰色橢圓顯示影子，大小可設定，預設先用11x7 pixel
角色sprite顯示順序在影子上
角色飛空時影子會縮小，落下時影子放大，落地後影子會復正常
角色與牆有判定，不可通過
預設先設定一個玩家角色在地圖上，在座標1x1

## trap

TBD

# Reference

- [[Deception IV The Nightmare Princess]]
- [[Aku Daikan]]
