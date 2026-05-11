---
name: pygame-space-invaders
description: Classic Space Invaders game prototype built with Pygame. Use when asked to play Space Invaders, test the Space Invaders game, or debug game logic. Supports formation movement, player shooting, alien shooting, increasing difficulty, and score tracking.
---

# Pygame Space Invaders

A minimal Space Invaders game prototype built with Pygame.

## When to Use

- Play a game of Space Invaders
- Test or debug the Space Invaders game logic
- Verify game rules: formation movement, shooting, increasing difficulty

## Prerequisites

- Python 3.10+
- Pygame (see requirements.txt)

## Usage

```
python pygame-space-invaders.py [--width N] [--height N] [--fps N] [--alien-speed N]
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--width` | 800 | Window width in pixels |
| `--height` | 600 | Window height in pixels |
| `--fps` | 60 | Frame rate |
| `--alien-speed` | 2.0 | Alien movement base speed |

### Controls

- **Left/Right arrows or A/D**: Move player
- **Space**: Shoot
- **R key**: Restart after game over
- **ESC / Close window**: Exit

## Game Rules

- Player moves left/right at the bottom of the screen
- Aliens move in formation, stepping down when reaching screen edges
- Shooting an alien destroys it and increases score
- Aliens randomly shoot back at the player
- Alien movement speed increases as more aliens are destroyed
- Clearing all aliens advances to the next level with increased difficulty
- Losing all 3 lives ends the game
