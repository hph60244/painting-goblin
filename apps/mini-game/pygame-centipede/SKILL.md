---
name: pygame-centipede
description: Classic Centipede game prototype built with Pygame. Use when asked to play Centipede, test the Centipede game, or debug game logic. Supports segmented enemies, terrain interaction, and centipede splitting.
---

# Pygame Centipede

A minimal Centipede game prototype built with Pygame.

## When to Use

- Play a game of Centipede
- Test or debug the Centipede game logic
- Verify game mechanics: segmented centipede movement, mushroom terrain interaction, centipede splitting

## Prerequisites

- Python 3.10+
- Pygame (see requirements.txt)

## Usage

```
python pygame_centipede.py [--fps N]
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--fps` | 60 | Frame rate |

### Controls

- **Left/Right arrows**: Move player
- **Space**: Shoot
- **R key**: Restart after game over
- **ESC / Close window**: Exit

## Game Rules

- Shoot centipede segments to destroy them
- Hit segments split the centipede into two smaller centipedes
- Centipedes move horizontally and drop down when hitting mushrooms or walls
- Destroyed segments turn into mushrooms
- Player loses a life on contact with any centipede segment
- Game over when all lives are lost
