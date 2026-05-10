---
name: pygame-simon-says
description: Simon Says memory game implemented in Pygame. Use when asked to build a memory game prototype, demonstrate Pygame 2D game development, or create a minimalist Simon Says clone with sequence playback and player input.
---

# Pygame Simon Says

A minimalist Simon Says memory game prototype built with Pygame. Features four colored buttons in a 2x2 grid with sequence playback, player input validation, and score tracking.

## When to Use This App

- Playing or testing the Simon Says memory game
- Demonstrating Pygame 2D game concepts
- Prototyping memory/pattern games

## Running

```bash
python apps/pygame-simon-says/pygame-simon-says.py
```

Or double-click the batch file:
```
apps/pygame-simon-says/pygame-simon-says.bat
```

## Arguments

| Argument | Description |
|----------|-------------|
| `--hard`  | Faster sequence playback (300ms flash -> 150ms) |

## Controls

- **Mouse click**: Press buttons to repeat the sequence
- **R key**: Restart when game over

## Gameplay

1. Watch the sequence of flashing colors
2. Repeat it by clicking the buttons in the same order
3. Each correct round adds one more step
4. A wrong click ends the game

## File Structure

```
pygame-simon-says/
├── SKILL.md
├── pygame-simon-says.py
├── pygame-simon-says.bat
└── requirements.txt
```
