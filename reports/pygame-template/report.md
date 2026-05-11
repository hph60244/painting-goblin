# Pygame Game Jam Starter Templates — Research Report

**Date:** 2026-05-11
**Goal:** Find Pygame game jam starter templates updated within the last 3 years, providing prototyping features (scene management, video/audio settings, input mapping, save/load, etc.)

---

## Executive Summary

**No single template or framework provides all requested features out of the box.** The pygame ecosystem is fragmented — a game jam starter must be assembled from individual libraries. The closest existing template is **The-Ultimate-Pygame-Structure** (scene management + input mapping + project scaffolding), but it lacks save/load and audio settings.

---

## Top Candidates

### 1. The-Ultimate-Pygame-Structure (Best Overall Template)
| | |
|---|---|
| **URL** | https://github.com/SebZanardo/The-Ultimate-Pygame-Structure |
| **Stars** | 6 |
| **Last Updated** | Apr 2025 |
| **License** | MIT |
| **Features** | Scene management (`scenes/`), input mapping (`core/input.py`), asset management, configurable constants, pygbag web export |
| **Missing** | Save/load system, audio settings, configurable video settings (only constants) |

### 2. game-state (Best Scene Management Library)
| | |
|---|---|
| **URL** | https://github.com/Jiggly-Balls/game-state |
| **Stars** | 10 |
| **Last Updated** | Apr 2026 |
| **PyPI** | `pip install game_state` |
| **Features** | Type-safe state machine with lifecycle hooks, shared state attributes, well-documented |
| **Note** | Pygame-agnostic library, not a full template |

### 3. tyraziel/pygame-ce-template (Simplest Single-File Starter)
| | |
|---|---|
| **URL** | https://github.com/tyraziel/pygame-ce-template |
| **Stars** | 0 |
| **Last Updated** | Jan 2025 |
| **License** | CC0 |
| **Features** | Single 1560-line `template.py`, embedded Kenney assets (fonts, sprites, SFX), basic game loop |
| **Missing** | Scene management, configurable settings, save/load |

---

## Ecosystem Building Blocks

| Library | Stars | Last Update | Purpose | pip |
|---|---|---|---|---|
| **pygame-ce** | 1.5k | 2026-03 | Active SDL2 base library | `pygame-ce` |
| **pgzero** | 602 | 2025-01 | Zero-boilerplate game framework | `pgzero` |
| **pygame-menu** | 601 | 2025-04 | Menu/GUI widgets | `pygame-menu` |
| **pygame_gui** | 806 | Active | Full GUI system | `pygame_gui` |
| **pygbag** | 496 | 2026-03 | WebAssembly/itch.io export | `pygbag` |
| **PyTMX** | 420 | 2023 | Tiled map loader | `pytmx` |
| **pyscroll** | 188 | 2021 | Animated scrolling maps | `pyscroll` |
| **Pymunk** | 1.1k | 2026-05 | 2D physics | `pymunk` |
| **game-state** | 10 | 2026-04 | State machine (scene mgmt) | `game_state` |

---

## Recommended Stack for a Game Jam Starter

If you need to BUILD a starter template (rather than find one), the recommended combination is:

1. **Base:** `pygame-ce` (active fork, SDL2)
2. **Scene Management:** `game-state` (type-safe state machine) or custom scene stack
3. **UI/Menus:** `pygame-menu` (settings screens, pause menu)
4. **Input Mapping:** Custom module (`core/input.py` style from The-Ultimate-Pygame-Structure)
5. **Audio/Video Settings:** Custom modules (JSON config file + pygame-menu UI)
6. **Save/Load:** Custom JSON/pickle persistence module
7. **Web Export:** `pygbag` (itch.io deployment)
8. **Maps (optional):** `pytmx` + `pyscroll`

---

## Gap Analysis

| Feature | Available In | Status |
|---|---|---|
| Scene Management | game-state, The-Ultimate-Pygame-Structure | ✅ Covered |
| Input Mapping | The-Ultimate-Pygame-Structure | ✅ Covered |
| Video Settings | Partial (constants) | ⚠️ Needs custom work |
| Audio Settings | Not in any template | ❌ Needs custom work |
| Save/Load System | Not in any template | ❌ Needs custom work |
| GUI/Menus | pygame-menu, pygame_gui | ✅ Covered |
| Web Export | pygbag | ✅ Covered |

---

## Community Resources

- **Awesome list:** https://github.com/kadir014/awesome-pygame (15★)
- **Reddit:** /r/pygame — active community, regular game jams
- **Active Jams:** Pygame Community Jam, GMTK Jam, Pirate Software Jam
- **Key Contributors:** DaFluffyPotato (tutorials), MyreMylar (pygame_gui/ce), ppizarror (pygame-menu), bitcraft (pytmx/pyscroll), pmp-p (pygbag)

---

## Conclusion

For the painting-goblin project, the recommended approach is to **use The-Ultimate-Pygame-Structure as a foundation** (it already has scene management + input mapping + project structure) and **extend it** with:
- `game-state` for more robust scene transitions
- `pygame-menu` for settings UI
- Custom save/load and audio settings modules
- `pygbag` for web export

This is more efficient than building from scratch, and all components are MIT-licensed and actively maintained.
