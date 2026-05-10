---
name: pygame-memory-cards
description: Memory Cards matching game prototype built with Pygame. Use when asked to play Memory Cards, test matching logic, or debug the flip animation. Supports configurable grid size and mismatch delay.
---

# Pygame Memory Cards

A minimal memory card matching game prototype built with Pygame.

## When to Use

- Play a game of Memory Cards
- Test or debug the card matching and flip animation logic
- Verify game rules: flip two cards, match pairs, win condition

## Prerequisites

- Python 3.10+
- Pygame (see requirements.txt)

## Usage

```
python pygame-memory-cards.py [--rows ROWS] [--cols COLS] [--delay DELAY] [--debug]
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--rows` | 4 | Number of rows (total cards must be even) |
| `--cols` | 4 | Number of columns |
| `--delay` | 1.0 | Seconds before unmatched cards flip back |
| `--debug` | false | Enable debug logging |

### Controls

- **Left click**: Flip a card
- **Close window**: Exit

## Game Rules

- Grid contains pairs of matching cards shuffled randomly
- Click a card to flip it and reveal its value
- Click a second card to find a match
- Matching pair stays face up; non-matching pair flips back after delay
- Match all pairs to win
