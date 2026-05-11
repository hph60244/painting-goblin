---
name: pygame-piano-tiles
description: Minimal Piano Tiles game prototype built with Pygame. Use when asked to play Piano Tiles, test the game, or debug tile-falling mechanics. Supports configurable lanes, speed, mouse click input, and score tracking.
---

# Pygame Piano Tiles

A minimal Piano Tiles game prototype built with Pygame.

## When to Use

- Play a game of Piano Tiles
- Test or debug the Piano Tiles game logic
- Verify game rules: timed tapping, lane scrolling, miss detection, score tracking, speed increases

## Prerequisites

- Python 3.10+
- Pygame (see requirements.txt)

## Usage

```
python pygame_piano_tiles.py [--lanes N] [--speed PX_PER_SEC] [--speed-increment PX_PER_SEC]
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--lanes` | 4 | Number of lanes |
| `--speed` | 300 | Initial tile fall speed in px/s |
| `--speed-increment` | 15 | Speed increase per successful tap in px/s |

### Controls

- **Mouse click**: Tap a tile in the hit zone to score
- **R key**: Restart after game over
- **ESC / Close window**: Exit

## Game Rules

- Black tiles scroll down from the top in multiple lanes
- Click a tile while it is inside the gray hit zone to score
- Missing a tile or clicking an empty lane ends the game
- Speed increases with each successful tap
- Minimalist black-and-white aesthetic
