---
name: pygame-tic-tac-toe
description: Run a Pygame Tic-Tac-Toe game with Minimax AI. Use when asked to play Tic-Tac-Toe, test game logic, or demonstrate Minimax algorithm with Pygame.
---

# Pygame Tic-Tac-Toe

A minimalist Tic-Tac-Toe game prototype using Pygame with a Minimax AI opponent.

## Usage

Run the game:

```bash
python apps/pygame-tic-tac-toe/pygame-tic-tac-toe.py
```

Or use the batch file:

```bash
apps\pygame-tic-tac-toe\pygame-tic-tac-toe.bat
```

## Arguments

| Argument | Choices | Default | Description |
|----------|---------|---------|-------------|
| `--first-player` | `human`, `ai` | `human` | Who plays first |
| `--human-side` | `X`, `O` | `X` | Human plays as X or O |
| `--log-level` | `DEBUG`, `INFO`, `WARNING`, `ERROR` | `INFO` | Logging verbosity |

## Controls

- Click a cell to place your mark
- Press `R` after game over to restart
- Close window to exit

## Requirements

- Python 3.10+
- Pygame 2.5+
