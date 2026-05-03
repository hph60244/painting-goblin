---
name: pygame-minesweeper
description: Classic Minesweeper game prototype built with Pygame. Use when asked to play Minesweeper, test the Minesweeper game, or debug the game logic. Supports Beginner (9x9, 10 mines), Intermediate (16x16, 40 mines), Expert (30x16, 99 mines), and Custom modes.
---

# Pygame Minesweeper

A minimal classic Minesweeper game prototype built with Pygame.

## When to Use

- Play a game of Minesweeper
- Test or debug the Minesweeper game logic
- Verify game rules: left-click reveal, right-click flag, number logic, flood fill, win/lose conditions

## Prerequisites

- Python 3.10+
- Pygame (see requirements.txt)

## Usage

```
python pygame-minesweeper.py [--beginner | --intermediate | --expert | --custom WIDTH HEIGHT MINES]
```

### Difficulty Modes

| Mode | Grid | Mines |
|------|------|-------|
| `--beginner` | 9x9 | 10 |
| `--intermediate` | 16x16 | 40 |
| `--expert` | 30x16 | 99 |
| `--custom W H M` | WxH | M |

### Controls

- **Left click**: Reveal a cell
- **Right click**: Toggle flag on a cell
- **R key**: Reset the game
- **Close window**: Exit

## Game Rules

- First click is always safe (mines placed after first click)
- Numbers show adjacent mine count
- Empty cells auto-reveal neighbors (flood fill)
- Revealing a mine ends the game
- Revealing all non-mine cells wins the game
