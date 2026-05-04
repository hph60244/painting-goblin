# Puzzle & Board Game Research for Pygame Demos

**Date:** 2026-05-04
**Source Research:** pygame.org, GitHub (pygame-games topic, puzzle-game topic), Real Python Pygame Primer

---

## Game Candidates

### 1. Tic-Tac-Toe (Noughts & Crosses)
- **Core mechanics:** Two players alternately place X/O marks on a 3x3 grid; first to align three marks wins.
- **Complexity:** Simple
- **Files/classes:** 1 file, 2 classes (Game, Board)
- **Why good for AI agent:** Minimal state, trivial AI (minimax in ~30 lines), excellent first demo. Grid-based drawing teaches pygame.Rect and event handling.
- **Source:** Real Python "Pygame: A Primer on Game Programming" (https://realpython.com/pygame-a-primer/)

### 2. Memory Card Matching (Concentration)
- **Core mechanics:** Cards laid face-down; player flips two per turn to find matching pairs.
- **Complexity:** Simple
- **Files/classes:** 1-2 files, 2-3 classes (Card, Board, Game)
- **Why good for AI agent:** Teaches image loading, flip animations, state management (face-up/face-down), and turn logic. Clear discrete states.
- **Source:** Games collection by CharlesPikachu (github.com/CharlesPikachu/Games) — includes "flipcardbymemory" implementation at 5.4k stars.

### 3. Hangman
- **Core mechanics:** Player guesses letters to reveal a hidden word; each wrong guess adds a body part to the gallows.
- **Complexity:** Simple
- **Files/classes:** 1 file, 2 classes (Game, WordBank)
- **Why good for AI agent:** Text-heavy, teaches pygame.font rendering, keyboard input handling, and simple progressive drawing. No grid math needed.
- **Source:** pygame.org puzzle tag (https://www.pygame.org/tags/puzzle) — 342 projects tagged "puzzle"

### 4. Simon Says (Memory Sequence)
- **Core mechanics:** Computer plays a light/sound sequence of increasing length; player must repeat it exactly.
- **Complexity:** Simple
- **Files/classes:** 1 file, 2 classes (SimonGame, Button)
- **Why good for AI agent:** Teaches timer-based events (pygame.time.set_timer), color/sound playback (pygame.mixer), and sequence comparison. Pure visual/audio feedback loop.
- **Source:** pygame docs time module (https://www.pygame.org/docs/ref/time.html) — custom event pattern for timed sequences

### 5. Wordle
- **Core mechanics:** Player guesses a 5-letter word in 6 tries; letter tiles color-coded green/yellow/gray for correct/misplaced/wrong.
- **Complexity:** Simple
- **Files/classes:** 1 file, 2 classes (Wordle, Tile)
- **Why good for AI agent:** Fixed grid (6x5), no movement logic, pure state machine. Teaches keyboard input, color feedback, and word list filtering. Extremely well-defined rules.
- **Source:** GitHub topic puzzle-game Python repos (github.com/topics/puzzle-game?l=python)

### 6. Minesweeper
- **Core mechanics:** Grid of hidden mines; reveal cells with number hints indicating adjacent mine count. Flag mines, avoid detonations.
- **Complexity:** Medium
- **Files/classes:** 1-2 files, 2-3 classes (Cell, Board, Game)
- **Why good for AI agent:** Recursive flood-fill algorithm, right-click flagging, mine generation with first-click safety. Teaches 2D array grid management and recursive algorithms.
- **Source:** CharlesPikachu/Games "minesweeper" (github.com/CharlesPikachu/Games) — 25 games implemented in pure Python with pygame

### 7. Connect Four
- **Core mechanics:** Two players drop colored discs into a 7x6 vertical grid; first to connect four in any direction wins.
- **Complexity:** Medium
- **Files/classes:** 1-2 files, 2-3 classes (Board, Disc, Game)
- **Why good for AI agent:** Physics-like gravity for disc dropping, win-checking in 4 directions, good minimax AI exercise (depth-limited). Teaches column-based grid and collision.
- **Source:** Real Python Pygame Primer — sprite groups and collision detection patterns

### 8. Checkers (Draughts)
- **Core mechanics:** Two players move pieces diagonally on 8x8 board; mandatory captures, king promotion at far rank.
- **Complexity:** Medium
- **Files/classes:** 2-3 files, 4 classes (Piece, Board, Game, AI)
- **Why good for AI agent:** Turn-based AI with minimax, piece jumping/capture logic, king promotion. Teaches complex rule validation, board coordinate systems, and AI search trees.
- **Source:** GitHub pygame-games topic (github.com/topics/pygame-games) — 1,059 public repositories

### 9. Sudoku
- **Core mechanics:** Fill 9x9 grid so each row, column, and 3x3 subgrid contains digits 1-9 exactly once. Pre-filled clues constrain placement.
- **Complexity:** Medium
- **Files/classes:** 2 files, 2-3 classes (Cell, Board, Generator/Solver)
- **Why good for AI agent:** Backtracking solver algorithm, puzzle generation with unique solution, cell selection with keyboard input. Pure logic puzzle — no randomness during play.
- **Source:** pygame.org project "sudoku" (https://www.pygame.org/project/270) — "nice little script for sudoku" with save/load

### 10. Othello / Reversi
- **Core mechanics:** Players place discs on 8x8 board; captured discs flip. Highest disc count wins. "Minute to learn, lifetime to master."
- **Complexity:** Medium
- **Files/classes:** 2-3 files, 3-4 classes (Disc, Board, Game, AI)
- **Why good for AI agent:** Flanking detection in 8 directions, strong positional AI (heuristic-based evaluation), clear endgame. Teaches direction vectors and board evaluation functions.
- **Source:** GitHub topic pygame-games — strategy board games are well-represented

### 11. Sokoban
- **Core mechanics:** Player pushes boxes onto target tiles in a grid-based warehouse. One box at a time, no pulling.
- **Complexity:** Medium
- **Files/classes:** 2 files, 3 classes (Level, Crate, Player)
- **Why good for AI agent:** Level loading from text files, undo mechanics (state stack), A* pathfinding exercise. Teaches file I/O for levels, state management, and movement constraints.
- **Source:** CharlesPikachu/Games "sokoban" (github.com/CharlesPikachu/Games) — 5.4k star collection; GitHub topic puzzle-dungeon includes sokoban (github.com/mig0/puzzle-dungeon)

### 12. Solitaire (Klondike)
- **Core mechanics:** Move cards between tableau columns, foundations, and stock to build ascending suits from Ace to King.
- **Complexity:** Complex
- **Files/classes:** 3-5 files, 5-7 classes (Card, Deck, Tableau, Foundation, Stock, Game, GameState)
- **Why good for AI agent:** Complex drag-and-drop, multi-state validation (alternating colors, descending ranks), auto-complete logic. Teaches OOP hierarchy, card game architecture, and complex state machines.
- **Source:** Real Python Pygame Primer — sprite groups and image blitting for card rendering; pygame docs for mouse event handling

### 13. Bubble Shooter
- **Core mechanics:** Aim and shoot colored bubbles to form groups of 3+ matching colors; attached bubbles fall if orphaned.
- **Complexity:** Medium
- **Files/classes:** 2-3 files, 4 classes (Bubble, Grid, Shooter, Game)
- **Why good for AI agent:** Hex-grid math, projectile physics (aiming line), flood-fill cluster detection, gravity logic. Teaches geometric grid systems and real-time aiming with mouse.
- **Source:** pygame.org puzzle tag (342 projects tagged puzzle) — includes bubble/puzzle hybrids

### 14. Bejeweled (Simplified Match-3)
- **Core mechanics:** Swap adjacent gems to form lines of 3+ matching gems; matched gems disappear and new gems fall from above.
- **Complexity:** Medium
- **Files/classes:** 2-3 files, 4 classes (Gem, Board, Game, Animator)
- **Why good for AI agent:** Swap validation, cascade/chain detection, gravity fill, animation tweening. Teaches grid swapping algorithms, chain reaction logic, and simple particle/score effects.
- **Source:** CharlesPikachu/Games "gemgem" (github.com/CharlesPikachu/Games) — "消消乐" match-3 game in pure Python

---

## Summary Table

| Game | Complexity | Files/Classes | Pygame Concepts Used |
|------|-----------|---------------|---------------------|
| Tic-Tac-Toe | Simple | 1 file, 2 cls | Rect, draw, MOUSEBUTTONDOWN |
| Memory Cards | Simple | 1-2 files, 2-3 cls | image.load, flip animation, event queue |
| Hangman | Simple | 1 file, 2 cls | font.render, KEYDOWN, progressive draw |
| Simon Says | Simple | 1 file, 2 cls | time.set_timer, mixer.Sound, color animation |
| Wordle | Simple | 1 file, 2 cls | font, keyboard input, color feedback |
| Minesweeper | Medium | 1-2 files, 2-3 cls | grid, mouse clicks, recursive flood-fill |
| Connect Four | Medium | 1-2 files, 2-3 cls | gravity, 4-way win check, minimax |
| Checkers | Medium | 2-3 files, 4 cls | board coords, jump logic, AI search |
| Sudoku | Medium | 2 files, 2-3 cls | grid, backtracking, cell selection |
| Othello | Medium | 2-3 files, 3-4 cls | direction vectors, heuristic AI, endgame |
| Sokoban | Medium | 2 files, 3 cls | tile maps, undo stack, collision |
| Bubble Shooter | Medium | 2-3 files, 4 cls | hex grid, projectile, flood-fill |
| Bejeweled | Medium | 2-3 files, 4 cls | swap validation, cascades, gravity fill |
| Solitaire | Complex | 3-5 files, 5-7 cls | drag-and-drop, multi-state validation, OOP |

---

## Recommendations for AI Coding Agent Demos

**Best first projects** (progressive difficulty):
1. **Tic-Tac-Toe** — smallest scope, teaches the game loop + grid
2. **Wordle** — no grid math, pure state machine + font rendering
3. **Memory Cards** — image handling + flip state management
4. **Simon Says** — timer events + sound/multimedia

**Best medium projects** (demonstrate real architecture):
5. **Minesweeper** — recursive algorithms + right-click UX
6. **Sokoban** — level file loading + undo/state management
7. **Connect Four** — simple AI (minimax) + gravity mechanics
8. **Othello** — strong AI showcase + directional logic

**Best complex project** (full architecture demo):
9. **Solitaire** — drag-and-drop, complex validation, card game framework

---

## Key Sources
- https://www.pygame.org/docs/ — official Pygame documentation with tutorials
- https://www.pygame.org/tags/puzzle — 342 Pygame projects tagged "puzzle"
- https://realpython.com/pygame-a-primer/ — Real Python's comprehensive Pygame primer (sprite groups, events, collision detection)
- https://github.com/CharlesPikachu/Games — 5.4k star collection of 29 Pygame games including minesweeper, sokoban, memory cards, gemgem
- https://github.com/topics/pygame-games — 1,059 public Pygame game repositories
- https://github.com/topics/puzzle-game?l=python — 198 Python puzzle game repositories
