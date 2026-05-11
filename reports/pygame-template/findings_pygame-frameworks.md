# Findings: Pygame Frameworks & Engines (Subtopic 2)

_Research conducted: 2026-05-11_

## Overview

Higher-level Python frameworks and engines built on top of pygame/pygame-ce that provide rapid prototyping features for game jams. Filtered for projects updated since 2023.

---

## 1. Pygame Zero (pgzero)

| Field | Info |
|---|---|
| **URL** | https://github.com/lordmauve/pgzero |
| **Stars** | ~602 |
| **Last Release** | v1.2.1 (Jan 18, 2025) |
| **Last Commit** | Sep 6, 2025 |
| **License** | LGPL-3.0 |
| **pip** | `pip install pgzero` |

**Description:** Zero-boilerplate games programming framework for Python 3, based on Pygame. Designed for education and rapid prototyping. No imports needed — `pgzrun` provides a full game loop with `draw()`, `update()`, and event handlers (`on_mouse_down`, etc.) automatically.

**Key Features:**
- Automatic game loop via `pgzrun` runner
- Built-in `screen` object (drawing, blitting, clearing)
- `Actor` class with sprite loading, positioning, collision
- Automatic sound loading via `sounds.eep.play()` convention
- Built-in keyboard/mouse input handling
- No boilerplate imports required
- Excellent documentation at pygame-zero.readthedocs.io

**Game Jam Fit:** Excellent for rapid prototyping — minimal setup, great for small teams/new programmers. Lacks built-in scene management but can be layered on.

**Note:** Works with both pygame and pygame-ce as the underlying SDL2 wrapper.

---

## 2. PursuedPyBear (ppb)

| Field | Info |
|---|---|
| **URL** | https://github.com/ppb/pursuedpybear |
| **Stars** | ~264 |
| **Last Release** | v3.2.0 (Dec 21, 2023) |
| **License** | Artistic-2.0 |
| **pip** | `pip install ppb` |

**Description:** Education-focused Python game engine built on pygame. Provides a `GameEngine` with pluggable subsystem architecture, scene stack, and event-driven design. Goal is to be "idiomatic Python" and fun to use.

**Key Features:**
- Scene management via state stack (`Scene` objects)
- Pluggable `System` architecture for adding features
- Event-driven: `on_update(self, update_event, signal)` pattern
- Vector math support (`ppb.Vector`)
- Hardware-library agnostic design
- Built-in sprite classes (`TargetSprite`)
- `ppb.run()` entry point

**Game Jam Fit:** Good fit for jams requiring structured scene management. The pluggable system architecture allows rapid extension. Last release Dec 2023 — moderately active.

---

## 3. pygame-menu

| Field | Info |
|---|---|
| **URL** | https://github.com/ppizarror/pygame-menu |
| **Stars** | ~601 |
| **Last Release** | v4.5.4 (Apr 25, 2025) |
| **License** | MIT |
| **pip** | `pip install pygame-menu` |

**Description:** Full-featured menu/GUI library for pygame and pygame-ce. Provides widgets (buttons, text inputs, selectors, sliders, dropdowns, tables, color pickers, clocks) for building game menus and UIs quickly.

**Key Features:**
- 15+ widget types (button, text input, selector, drop select, color input, table, frame, image, label, etc.)
- Theme support with customization
- Sound effects on widget interaction
- Background image support
- Keyboard/joystick navigation
- Works with both pygame and pygame-ce (separate branch)
- Comprehensive documentation

**Game Jam Fit:** Essential library for adding polished menus (main menu, settings, pause screen) quickly without building UI from scratch.

---

## 4. PyTMX

| Field | Info |
|---|---|
| **URL** | https://github.com/bitcraft/pytmx |
| **Stars** | ~420 |
| **Last Release** | v3.31 (Dec 1, 2021) |
| **Last Commit Activity** | 2023 (fixes) |
| **License** | LGPL-3.0 |
| **pip** | `pip install pytmx` |

**Description:** Python library to read Tiled Map Editor's TMX maps. Supports loading tile maps with metadata, properties, animations, objects, colliders, and multiple layer types. Compatible with pygame-ce.

**Key Features:**
- Load TMX maps from Tiled Map Editor
- Smart tile loading with efficient storage
- Supports all Tiled object types (polygon, polyline, ellipse, tile objects)
- Tile animations loaded automatically
- Tile collider groups
- Properties metadata for tiles, layers, objects
- Multiple image backends (pygame, pyglet, pysdl2)
- Supports base64, csv, gzip, zlib, uncompressed XML

**Game Jam Fit:** Must-have if using Tiled for level design. Not a framework itself but pairs with pyscroll for rendering.

---

## 5. pyscroll

| Field | Info |
|---|---|
| **URL** | https://github.com/bitcraft/pyscroll |
| **Stars** | ~188 |
| **Last Release** | v2.29 (Dec 10, 2021) |
| **License** | GPL-3.0 |
| **pip** | `pip install pyscroll` |

**Description:** Fast module for animated scrolling maps in pygame. Designed to work with PyTMX and Tiled maps. Provides `PyscrollGroup` that acts like a camera, rendering sprites and map layers in correct order.

**Key Features:**
- Animated tile support
- Zoom in/out
- Camera-like `PyscrollGroup` for sprite/map rendering
- Layer-aware sprite drawing (sprites render over/under tiles correctly)
- Pixel alpha and colorkey tilesets
- Fast — speed not affected by map size
- Works with custom data structures (not tied to PyTMX)
- pygame-ce compatible

**Game Jam Fit:** Pairs with PyTMX for Tiled map rendering. Essential for any tile-based game in a jam.

---

## 6. pygame-ce (Community Edition)

| Field | Info |
|---|---|
| **URL** | https://github.com/pygame-community/pygame-ce |
| **Stars** | ~1.5k |
| **Last Release** | v2.5.7 (Mar 2, 2026) |
| **License** | LGPL-2.1+ |
| **pip** | `pip install pygame-ce` |

**Description:** The active community fork of pygame, maintained by former core developers. This is the base library that all the above frameworks build on. More frequent releases, continuous bugfixes, and new features compared to upstream pygame.

**Key Features (vs upstream pygame):**
- SDL2-based with SDL 2.0.14+ support
- Python 3.10+ required
- More frequent releases (32 releases to date)
- Active Discord community
- Bug fixes and enhancements over upstream
- Backward compatible with pygame code

**Game Jam Fit:** Recommended as the foundation for any new pygame project in 2024+. All the frameworks above work with it.

---

## 7. pygbag

| Field | Info |
|---|---|
| **URL** | https://github.com/pygame-web/pygbag |
| **Stars** | ~496 |
| **Last Updated** | Mar 17, 2026 |
| **License** | MIT |
| **pip** | `pip install pygbag` |

**Description:** Compiles Python/pygame code to WebAssembly for browser deployment. Packager + test server + simulator. Not a framework but enables pygame games to run in the browser.

**Key Features:**
- Compile any pygame game to WebAssembly
- Test server with simulator
- No code changes typically needed
- Supports pygame-ce

**Game Jam Fit:** Useful for jams requiring web deployment (itch.io browser play). Works with any pygame-based framework.

---

## 8. Pymunk

| Field | Info |
|---|---|
| **URL** | https://github.com/viblo/pymunk |
| **Stars** | ~1.1k |
| **Last Updated** | May 10, 2026 |
| **License** | MIT |
| **pip** | `pip install pymunk` |

**Description:** Easy-to-use 2D physics library that works with pygame. Not strictly a framework but commonly paired in game jams for physics simulation.

**Key Features:**
- Rigid body physics (2D)
- Collision detection
- Joints and constraints
- Space management
- Works with pygame/pygame-ce

**Game Jam Fit:** Add physics to any pygame-based game quickly.

---

## Summary Table

| Project | Stars | Last Update | Scene Mgmt | Audio | Input | Maps/Tiles | GUI/Menus | Physics | Web Export |
|---|---|---|---|---|---|---|---|---|---|
| pgzero | 602 | 2025-01 | No* | Auto | Auto | No | No | No | No |
| ppb | 264 | 2023-12 | Yes | No | Event | No | No | No | No |
| pygame-menu | 601 | 2025-04 | No | Sound FX | Widget | No | Yes | No | No |
| PyTMX | 420 | 2023 | No | No | No | Yes | No | No | No |
| pyscroll | 188 | 2021 | No | No | No | Yes (render) | No | No | No |
| pygame-ce | 1.5k | 2026-03 | No | Yes | Yes | No | No | No | No |
| pygbag | 496 | 2026-03 | No | No | No | No | No | No | Yes |
| Pymunk | 1.1k | 2026-05 | No | No | No | No | No | Yes | No |

*\* pgzero's `update()`/`draw()` structure can host custom scene management.*

## Recommendations for Game Jam Starter

For a complete game jam starter template, a combination would be needed:

1. **Base:** pygame-ce (the active SDL2 wrapper)
2. **Framework layer:** pgzero (for zero-boilerplate start) OR ppb (for scene management)
3. **Map/level editor:** PyTMX + pyscroll (if using Tiled maps)
4. **UI:** pygame-menu (for settings, menus, HUD)
5. **Physics:** Pymunk (optional, if needed)
6. **Web export:** pygbag (for browser distribution on itch.io)

No single project provides all features (scene management, audio, input mapping, save/load, video settings, asset handling) out of the box. A jam starter would need to be assembled from these building blocks.
