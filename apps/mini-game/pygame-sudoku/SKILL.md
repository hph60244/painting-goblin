---
name: pygame-sudoku
description: Minimal Sudoku game prototype built with Pygame featuring backtracking solver, puzzle generation, and keyboard/mouse input. Use when asked to play Sudoku, test the Sudoku game, or debug puzzle logic.
---

# Pygame Sudoku

A minimal Sudoku game prototype built with Pygame.

## When to Use

- Play a game of Sudoku
- Test or debug the Sudoku game logic
- Verify game rules: number placement, conflict detection, backtracking solver, puzzle generation

## Prerequisites

- Python 3.10+
- Pygame (see requirements.txt)

## Usage

```
python pygame_sudoku.py [--difficulty DIFFICULTY] [--cell-size N] [--log-level LEVEL]
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--difficulty` | medium | Puzzle difficulty: easy, medium, hard |
| `--cell-size` | 60 | Cell size in pixels |
| `--log-level` | INFO | Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL |

### Controls

- **Arrow keys**: Move selection
- **Mouse click**: Select cell
- **1-9 keys**: Place number in selected cell
- **Backspace/Delete**: Clear selected cell
- **R key**: Reset puzzle (same difficulty)
- **N key**: New puzzle (same difficulty)
- **ESC / Close window**: Exit

## Game Rules

- Fill the 9x9 grid so each row, column, and 3x3 box contains digits 1-9
- Pre-filled clues are fixed (shown in black)
- Player-entered numbers appear in gray
- Conflicts are highlighted in red
- Completing the grid without conflicts wins the game
