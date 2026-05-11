---
name: pygame-dig-dug
description: Run the Dig Dug arcade game prototype built with Pygame. Use when asked to play or run the Dig Dug game.
---

# Pygame Dig Dug

A minimalist Dig Dug game prototype built with Pygame. The player navigates underground tunnels, digs through dirt, inflates enemies with a pump, and avoids being caught.

## How to Run

```bash
python apps/pygame-dig-dug/pygame_dig_dug.py
```

Or double-click `apps/pygame-dig-dug/pygame_dig_dug.bat`.

## Controls

| Key | Action |
|-----|--------|
| Arrow Keys | Move Dig Dug |
| Space | Activate pump (inflate enemies) |
| P | Pause/Resume |
| R | Restart (after game over/level clear) |
| ESC | Quit |

## Gameplay

- **Digging**: Walk into dirt tiles to create tunnels
- **Enemies**: Pooka enemies chase you through tunnels; they can also dig through dirt (slower)
- **Pump**: Face an enemy and press Space to inflate it until it pops
- **Rocks**: Clear the dirt below rocks to make them fall and crush enemies
- **Scoring**: 2000 points per crushed enemy
- **Lives**: 3 lives; lose one when an enemy catches you

## Command Line Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--cell-size` | 24 | Cell size in pixels |
| `--speed` | 0.1 | Time between player moves (seconds) |
| `--enemies` | 3 | Number of enemies per level |
| `--log-level` | INFO | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |

## Design Notes

- Minimal visual style with basic shapes and colors
- Grid-based movement (26x22 tiles)
- BFS pathfinding for enemy AI
- Logger used for debugging
- No external assets required
