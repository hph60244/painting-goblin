---
name: pygame-crossy-road
description: Crossy Road-like endless hopper game built with Pygame. Use when asked to run the Crossy Road prototype, play the lane-hopping game, or test the procedural lane generation implementation. Supports keyboard controls for movement.
---

# Pygame Crossy Road

A minimal Crossy Road game prototype built with Pygame-ce. The player controls a character that hops across procedurally generated lanes while avoiding obstacles.

## How to Run

```bash
python apps/pygame-crossy-road/pygame-crossy-road.py
```

Or double-click `apps/pygame-crossy-road/pygame-crossy-road.bat`

## Controls

| Key | Action |
|-----|--------|
| Up / W | Jump forward |
| Down / S | Jump backward |
| Left / A | Jump left |
| Right / D | Jump right |
| R | Restart after game over |
| Escape | Quit |

## Command Line Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--width` | 480 | Window width |
| `--height` | 720 | Window height |
| `--fps` | 60 | Frame rate |
| `--debug` | false | Enable debug logging |

## Game Features

- Lane hopping mechanic
- Procedural lane generation (grass, road, water, rail)
- Obstacle avoidance (cars, trucks, trains, water)
- Score tracking
- Game over and restart
