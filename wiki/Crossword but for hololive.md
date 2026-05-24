---
tags: ['#idea', '#task/suspend', '#game', '#wip']
---

# Requirement

- https://www.youtube.com/watch?v=ndFsdgpoJl0&ab_channel=VOGUETaiwan
- http://dict.idioms2.moe.edu.tw/bookView.jsp?ID=-1
- https://www.edu.tw/Content_List.aspx?n=83D8D70FE4468412
- https://play.google.com/store/apps/details?id=com.wordpuzzle.chengyu

# Document

- generate crossword board
- implement simple ui
- design ui and rwd
    - [[https://gn02214231.pixnet.net/blog/post/211524319-unity-如何去設定行動裝置的畫面翻轉]]
    - cell size, cell space, cell ltr pad, cell char space, char size, char space, char lr pad, char option space, option size, option space, option lrb pad
    - width = cell size x 10 + cell space x 9 + cell lr pad = char size x 6 + char space x 5 + char  lr pad = option size x 2 + option space x 1 + option lr pad
    - height = cell t pad + cell size x 8 + cell space x 7 + cell char space + char size x 3 + char space x 2 + char option space + option size + option b pad
    - 320*(0.8*1.5+0.2) = 448
- test mobile build
- auto focus
- design difficulty and better puzzle setup
- calendar view : [[EugeneKim/SimpleUnityCalendar: Unity project to show how to implement a simple calendar|https://github.com/EugeneKim/SimpleUnityCalendar]]
- https://github.com/rayaldeo/UnityCalendar
- https://github.com/meaf75/Calendar-UIElements
- https://github.com/Gahshomar/gahshomar
- https://github.com/Soulside44/UnityCalendar
- https://github.com/caseyryan/unity_app_gui
- https://github.com/adrianiainlam/indicator-lunar-calendar
- https://github.com/fragmental/BasicCalendar
- https://github.com/psynut/DatePick-WallCalendar
- fix lua bug when indexing data from cell
- check nil and false logic
- fix auto focus on game Index 6
- choose stage ui
- restart game
- crossword ui add color
- stage selection add color
- >find ui template
- >crossword ui add focus anime
- >crossword ui add wrong vfx
- >polish stage selection ui
- >polish calendar ui
- >auto focus along movement or nearby, if move to left, choose horizontal word first
- >puzzle setup prevent bunch of empty cells
- >better drop number for balancing
- >test google play
- >add se
- >add music
- >save player data
- >donation
- >sso
- >remove ticks
- >write lua test, unify indent
