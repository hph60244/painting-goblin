---
name: pygame-asteroids
description: Classic Asteroids game prototype built with Pygame. Use when asked to play Asteroids, test the Asteroids game, or debug game logic. Supports vector rotation, thrust, screen wrapping, and asteroid splitting.
---

# Pygame Asteroids

A minimal Asteroids game prototype built with Pygame.

## When to Use

- Play a game of Asteroids
- Test or debug the Asteroids game logic
- Verify game mechanics: vector rotation, thrust, screen wrapping, asteroid splitting

## Prerequisites

- Python 3.10+
- Pygame (see requirements.txt)

## Usage

```
python pygame_asteroids.py [--fps N] [--width N] [--height N] [--asteroids N] [--lives N]
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--fps` | 60 | Frame rate |
| `--width` | 1024 | Window width |
| `--height` | 768 | Window height |
| `--asteroids` | 4 | Number of asteroids per level |
| `--lives` | 3 | Number of lives |

### Controls

- **Left/Right arrows**: Rotate ship
- **Up arrow**: Thrust
- **Space**: Shoot
- **R key**: Restart after game over
- **ESC / Close window**: Exit

## Game Rules

- Destroy all asteroids to advance to the next level
- Large asteroids split into two medium asteroids
- Medium asteroids split into two small asteroids
- Small asteroids are destroyed
- Ship is destroyed on contact with any asteroid
- Game over when all lives are lost
