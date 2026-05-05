---
name: pygame-snake
description: Classic Snake game prototype built with Pygame. Use when asked to play Snake, test the Snake game, or debug game logic. Supports grid movement, growing snake, self-collision, wall collision, and score tracking.
---

# Pygame Snake

A minimal Snake game prototype built with Pygame.

## When to Use

- Play a game of Snake
- Test or debug the Snake game logic
- Verify game rules: grid movement, growing snake on food, self-collision game over, wall collision game over

## Prerequisites

- Python 3.10+
- Pygame (see requirements.txt)

## Usage

```
python pygame_snake.py [--cell-size N] [--cols N] [--rows N] [--speed SECONDS]
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--cell-size` | 30 | Cell size in pixels |
| `--cols` | 20 | Number of grid columns |
| `--rows` | 15 | Number of grid rows |
| `--speed` | 0.15 | Seconds between moves (lower = faster) |

### Controls

- **Arrow keys**: Change snake direction
- **R key**: Restart after game over
- **ESC / Close window**: Exit

## Game Rules

- Snake moves continuously on a grid
- Eating food makes the snake grow and increases score
- Hitting a wall or yourself ends the game
- Filling the entire grid wins the game
