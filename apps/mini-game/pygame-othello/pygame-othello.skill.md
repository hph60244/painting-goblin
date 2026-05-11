---
name: pygame-othello
description: Othello/Reversi game prototype built with Pygame. Use when asked to play or run Othello/Reversi, test AI heuristic strategies, or demonstrate 8-direction flanking game logic.
---

# Pygame Othello / Reversi

A minimal Othello/Reversi game prototype with heuristic AI opponent.

## Quick Start

```bash
apps\pygame-othello\pygame-othello.bat
```

## Usage

```
python apps/pygame-othello/pygame-othello.py [--two-player] [--depth {1,2,3}] [--first {black,white}]
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--two-player` | off | 雙人模式 (vs AI by default) |
| `--depth` | 2 | AI 搜索深度 (1-3) |
| `--first` | black | 玩家執棋顏色 |

## Controls

| Key | Action |
|-----|--------|
| Mouse click | Place piece |
| H | Toggle valid-move hints |
| R | Restart (when game over) |
| ESC | Quit |

## Architecture

- **OthelloGame**: Core 8-dir flanking logic, move validation, game-over detection
- **ai_move()**: Position-weight heuristic with negamax search (configurable depth)
- **OthelloUI**: Minimal Pygame rendering with hints overlay
