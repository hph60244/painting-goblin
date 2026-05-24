# Pygame Demo Games for AI Coding Agent — Ultimate Report

**Date:** 2026-05-04
**Objective:** 尋找數十個適合讓Coding Agent用Pygame做成demo的小遊戲

---

## Complete Game Catalog (35+ Games)

### Category 1: Classic Arcade Games (14 games)

| Game | Complexity | Est. Lines | Files | Core Mechanic |
|------|-----------|-----------|-------|---------------|
| Pong | Simple | 120-180 | 1 | Ball physics, paddle AI, collision rebound |
| Snake | Simple-Medium | 150-200 | 1 | Grid movement, growing linked list, self-collision |
| Breakout/Arkanoid | Medium | 200-300 | 1-2 | Angled ball deflection, brick grid, powerups |
| Space Invaders | Medium | 250-350 | 1-2 | Formation movement, shooting, increasing difficulty |
| Asteroids | Medium | 250-350 | 1-2 | Vector rotation, thrust, screen wrapping, splitting |
| Frogger | Medium | 250-350 | 1-2 | Lane-based movement, moving platforms, multiple hazards |
| Centipede | Medium | 300-400 | 1-2 | Segmented enemies, terrain interaction, splitting |
| Joust | Medium-Complex | 300-450 | 1-2 | Flight physics, vertical collision priority |
| Galaga | Medium-Complex | 350-500 | 2-3 | Formation patterns, dive-bomb AI, bullet-hell |
| Tetris | Medium-Complex | 300-400 | 1-2 | Block rotation (SRS), grid management, line clearing |
| Pac-Man | Complex | 400-600 | 2-4 | Ghost pathfinding AI, maze, state machine |
| Donkey Kong | Complex | 400-600 | 2-3 | Platform physics, gravity, multi-screen levels |
| Dig Dug | Complex | 400-550 | 2-3 | Terrain modification, tunnel pathfinding |
| Defender | Complex | 400-600 | 2-3 | Side-scrolling, radar HUD, multi-objective |

### Category 2: Modern Casual & Mobile Games (10 games)

| Game | Complexity | Est. Lines | Files | Core Mechanic |
|------|-----------|-----------|-------|---------------|
| Flappy Bird | Simple | 150-250 | 1-2 | Gravity + tap, procedural pipes |
| 2048 | Simple | 150-300 | 1 | Grid merge logic, no physics |
| Piano Tiles | Simple | 100-200 | 1 | Timed tap, lane scrolling |
| Doodle Jump | Simple | 200-350 | 1-2 | Bounce physics, vertical platform gen |
| Geometry Dash | Medium | 300-500 | 2-3 | Rhythm auto-scroll, instant restart |
| Crossy Road (simplified) | Medium | 300-500 | 2-3 | Lane hopping, procedural generation |
| Fruit Ninja (simplified) | Medium | 300-500 | 2-3 | Swipe detection, particle effects |
| Subway Surfer (simplified) | Medium | 350-550 | 2-3 | 3-lane runner, parallax scrolling |
| Candy Crush (simplified) | Medium | 400-600 | 2-3 | Match-3 swap, cascade logic |
| Angry Birds (simplified) | Complex | 500-800+ | 3-4 | Physics simulation (Pymunk), destructible |

### Category 3: Puzzle, Board & Novelty Games (14 games)

| Game | Complexity | Est. Lines | Files | Core Mechanic |
|------|-----------|-----------|-------|---------------|
| Tic-Tac-Toe | Simple | ~80-120 | 1 | 3x3 grid, minimax AI |
| Hangman | Simple | ~100-150 | 1 | Text rendering, keyboard input |
| Wordle | Simple | ~120-180 | 1 | 6x5 grid, color feedback |
| Memory Cards | Simple | ~150-200 | 1-2 | Flip animation, pair matching |
| Simon Says | Simple | ~100-150 | 1 | Timer events, sequence memory |
| Minesweeper | Medium | 200-350 | 1-2 | Flood-fill, mine generation |
| Connect Four | Medium | 200-350 | 1-2 | Gravity discs, 4-way win check |
| Sokoban | Medium | 250-400 | 2 | Level files, undo stack, push logic |
| Bubble Shooter | Medium | 300-450 | 2-3 | Hex grid, projectile aim, flood-fill |
| Bejeweled (simplified) | Medium | 300-450 | 2-3 | Swap validation, cascade chains |
| Othello/Reversi | Medium | 300-400 | 2-3 | 8-dir flanking, heuristic AI |
| Sudoku | Medium | 300-500 | 2 | Backtracking solver, puzzle generation |
| Checkers | Medium | 350-500 | 2-3 | Jump captures, king promotion, minimax |
| Solitaire (Klondike) | Complex | 500-800+ | 3-5 | Drag-drop, multi-state validation |

---

## Recommended Learning Path for Coding Agent

### Phase 1: Foundation (Simple, 1 file each)
1. **Tic-Tac-Toe** — Teaches game loop, grid, mouse input, basic AI (minimax)
2. **Pong** — Teaches collision detection, keyboard input, simple AI opponent
3. **Snake** — Teaches grid-based movement, data structures (queue/list), self-collision
4. **Wordle** — Teaches font rendering, keyboard input, color feedback, state machine
5. **2048** — Teaches grid merge logic, arrow key input, game-over detection

### Phase 2: Mechanics (Simple-Medium, 1-2 files)
6. **Flappy Bird** — Gravity, procedural generation, sprite collision
7. **Simon Says** — Timed events, multimedia (sound), sequence logic
8. **Memory Cards** — Image handling, flip animation, turn management
9. **Breakout** — Sprite groups, angled physics, brick management
10. **Minesweeper** — Recursive algorithms, 2D array, right-click UX

### Phase 3: Architecture (Medium, 2-3 files)
11. **Space Invaders** — Formation movement, sprite groups, difficulty scaling
12. **Asteroids** — Vector math, rotation, screen wrapping, procedural splitting
13. **Tetris** — Rotation algorithms, grid state, line clearing, scoring
14. **Sokoban** — Level file loading, undo stack, movement constraints
15. **Connect Four** — Gravity simulation, win checking, minimax AI

### Phase 4: Showcase (Medium-Complex, 2-4 files)
16. **Pac-Man** — Pathfinding AI (ghosts), tile-based maze, state machines
17. **Othello** — Directional logic, heuristic evaluation, strong AI showcase
18. **Galaga** — Formation AI, dive-bomb patterns, bullet-hell mechanics
19. **Bubble Shooter** — Hex-grid math, projectile physics, cluster detection
20. **Geometry Dash** — Music sync, auto-scroll, particle effects, instant restart

### Phase 5: Capstone (Complex, 3-5 files)
21. **Solitaire** — Drag-and-drop, complex state validation, card game framework
22. **Angry Birds (simplified)** — Physics engine integration, destructible environments

---

## Key Technical Considerations

### Asset Strategy (No External Downloads)
All games can use Pygame's `draw` primitives (rect, circle, polygon, line) plus `font.render()` for text. No external images or sounds needed for a basic demo. Procedural generation of sprites (colored shapes) keeps the agent fully self-contained.

### Pygame Concepts by Game
- **Pygame core loop:** All games use `pygame.init()`, `display.set_mode()`, event loop, `display.flip()`
- **Sprite groups:** Breakout, Space Invaders, Frogger, Galaga, Geometry Dash, Crossy Road
- **Collision detection:** Pong, Breakout, Flappy Bird, Doodle Jump, Space Invaders
- **Timer events:** Simon Says, Geometry Dash, Space Invaders (spawn timing)
- **Vector/trig math:** Asteroids, Bubble Shooter, Angry Birds
- **Grid logic:** Snake, Tetris, 2048, Minesweeper, Sudoku, Connect Four, Candy Crush
- **AI algorithms:** Tic-Tac-Toe (minimax), Pac-Man (pathfinding), Othello (heuristic), Checkers (search tree)
- **State machines:** Pac-Man (frightened/scatter/chase), Wordle (guess states), Simon Says (sequence playback)

### Estimation Notes
- Line counts assume no external assets and minimal file structure
- Simpler games can be single-file; complex games benefit from 2-5 file separation
- AI agents benefit from clear modular structure (Game, Entity/Player, UI separated)
- Pygame Zero can reduce boilerplate by ~30% for most games

---

## Total: 38 Unique Games

| Complexity | Count |
|-----------|-------|
| Simple | 14 |
| Medium | 18 |
| Complex | 6 |

---

## Sources
- https://realpython.com/pygame-a-primer/
- https://realpython.com/top-python-game-engines/
- https://www.pygame.org/docs/
- https://www.pygame.org/docs/tut/PygameIntro.html
- https://github.com/mratanusarkar/Space-Invaders-Pygame
- https://github.com/wkeeling/arkanoid
- https://github.com/techwithtim/Flappy-Bird-In-Pygame
- https://github.com/CharlesPikachu/Games
- https://github.com/topics/pygame-games
- https://github.com/topics/puzzle-game?l=python
- https://www.pygame.org/tags/puzzle
- https://en.wikipedia.org/wiki/Flappy_Bird
- https://en.wikipedia.org/wiki/Doodle_Jump
- https://en.wikipedia.org/wiki/2048_(video_game)
