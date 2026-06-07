---
tags: ['#idea', '#task/suspend', '#game']
---

# Spec

## window

用滑鼠滾輪縮放
用滑鼠中鍵拖曳畫面
遊戲整體用2d地圖加上滯空物體的影子縮小呈現3d效果

## map struct

2d grid map，可以設定長寬，預設先用16x9格，零點在左上角
每格大小可設定，預設先用25x25 pixel
地圖上的物件越下方越靠近玩家，會顯示在越上層

## character

角色位置用一個(x,y)決定，碰撞判定可以設定長寬，預設先用9x9 pixel
角色顯示時用一個sprite，大小可設定，預設先用25x25 pixel
角色腳底用灰色橢圓顯示影子，大小可設定，預設先用11x7 pixel
角色sprite顯示順序在影子上
角色飛空時影子會縮小，落下時影子放大，落地後影子會復正常

# Reference

- [[Deception IV The Nightmare Princess]]
- [[Aku Daikan]]
