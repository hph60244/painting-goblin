# Pygame-CE Starter Templates & Boilerplate Projects: Research Findings

**Date:** 2026-05-11
**Scope:** GitHub repositories tagged or described as pygame-ce templates/boilerplate, updated since 2023

---

## Key Finding

Pygame-ce (community edition) is still relatively new compared to classic pygame. Dedicated pygame-ce starter templates with advanced prototyping features (scene management, video/audio settings, input mapping, save/load) are **scarce**. Most pygame-ce repositories are finished games or library utilities rather than structured templates. The most feature-complete template found is **The-Ultimate-Pygame-Structure**, while **game-state** provides the best reusable scene management library.

---

## Project 1: The-Ultimate-Pygame-Structure

| Attribute | Detail |
|---|---|
| **URL** | https://github.com/SebZanardo/The-Ultimate-Pygame-Structure |
| **Stars** | 6 |
| **Last Updated** | Apr 15, 2025 |
| **Commits** | 30 |
| **License** | MIT |
| **Topics** | pygame, pygame-ce, python3, pygbag |

### Description
A full project template / structure for organizing and building Pygame (CE) games. Designed to help developers quickly scaffold a maintainable project with clear separation of concerns. Includes pygbag support for building to web (Itch.io).

### Features
- **Scene Management** -- `scenes/` folder with a `Scene` base class; example scenes provided: `menu.py`, `game.py`, `global.py`
- **Video Settings** -- `core/setup.py` for window initialization; `core/constants.py` for display constants
- **Input Mapping** -- `core/input.py` for keybind definitions
- **Asset Management** -- `core/assets.py` for loading and organizing assets
- **Configurable Settings** -- `core/app.py` for application-level configuration
- **Web Export** -- `pygbag` integration with custom template (`custom.tmpl`)
- **Project Structure:**
  - `src/assets/` -- All game assets
  - `src/components/` -- Reusable game components
  - `src/core/` -- Init, settings, keybinds, assets, constants
  - `src/scenes/` -- Scene classes (menu, game, global)
  - `src/utilities/` -- Helper functions

### Prototyping Features Checklist
| Feature | Status |
|---|---|
| Scene Management | YES |
| Video Settings (configurable) | PARTIAL (via constants/setup) |
| Audio Settings | Not present |
| Input Mapping | YES (core/input.py) |
| Save/Load System | Not present |
| Web Export | YES (pygbag) |

---

## Project 2: game-state (Library)

| Attribute | Detail |
|---|---|
| **URL** | https://github.com/Jiggly-Balls/game-state |
| **Stars** | 10 |
| **Last Updated** | Apr 29, 2026 |
| **Commits** | 399 |
| **Releases** | 14 (latest: v2.4.1) |
| **License** | MIT |
| **PyPI** | `pip install game_state` |

### Description
A state machine library for organizing different in-game screens in Python. Not a full project template, but a well-maintained reusable library that can be dropped into any pygame or pygame-ce project. Pygame-agnostic -- works with pygame, pygame-ce, or any other library.

### Features
- **State & StateManager classes** -- Type-safe using generics (`State[T]`)
- **State lifecycle** -- `process_event()`, `process_update()` methods
- **State transitions** -- `change_state()`, `is_running` flag
- **Shared state attributes** -- Base state class for attributes shared across all states
- **Documentation** -- Full readthedocs site at https://game-state.readthedocs.io/
- **Python support** -- 3.8 through 3.14
- **CI/CD** -- pre-commit hooks, pytest, Makefile

### Prototyping Features Checklist
| Feature | Status |
|---|---|
| Scene Management | YES (core focus) |
| Video Settings | No (template-agnostic) |
| Audio Settings | No |
| Input Mapping | No |
| Save/Load System | No |

---

## Project 3: pygame-ce-template (tyraziel)

| Attribute | Detail |
|---|---|
| **URL** | https://github.com/tyraziel/pygame-ce-template |
| **Stars** | 0 |
| **Last Updated** | Jan 18, 2025 |
| **Commits** | 1 |
| **License** | CC0 1.0 (code), Kenney license (assets) |

### Description
Single-file starter template for pygame-ce, created for CodeMash 2025 "So you want to make video games?" session. Provides a self-contained 1560-line `template.py` with embedded Kenney assets (fonts, input prompt sprites, sound effects). Designed as a drop-in starting point for game jams.

### Features
- **Single-file design** -- Everything in one `template.py` for simplicity
- **Kenney assets** -- Includes fonts, sprite sheets (input prompts, pixel-16), sound effects
- **Basic game loop** -- Event handling, update, render pattern
- **Input handling** -- Keyboard input via key constants
- **Sound support** -- Kenney sound effects included
- **Sprite rendering** -- Sprites/input-prompts for UI

### Prototyping Features Checklist
| Feature | Status |
|---|---|
| Scene Management | No (single file) |
| Video Settings | No |
| Audio Settings | PARTIAL (assets included) |
| Input Mapping | PARTIAL (basic key handling) |
| Save/Load System | No |

---

## Project 4: Code-Play-Pygame

| Attribute | Detail |
|---|---|
| **URL** | https://github.com/bijiyiqi2017/Code-Play-Pygame- |
| **Stars** | 2 |
| **Last Updated** | Apr 7, 2025 |
| **License** | MIT |

### Description
A collaborative Hacktoberfest 2024 project collecting community-contributed game templates and resources for learning Pygame. Not specifically focused on pygame-ce. More of a learning collection than a structured template.

### Features
- Collection of game templates in `/templates/`
- Resource links in `/resources/`
- Community-driven, beginner-focused

### Prototyping Features Checklist
| Feature | Status |
|---|---|
| Scene Management | Varies per template |
| Video Settings | No |
| Audio Settings | No |
| Input Mapping | Varies per template |
| Save/Load System | No |

---

## Notable pygame-ce Projects (Not Templates, but Relevant for Reference)

| Project | Stars | Description | URL |
|---|---|---|---|
| **nodezator** | 2.8k | Python node editor built with pygame-ce | https://github.com/IndieSmiths/nodezator |
| **nevu-ui** | 7 | Declarative GUI multibackend framework (pygame-ce backend) | https://github.com/GolemBebrov/nevu-ui |
| **pyretro-gui** | 74 | Retro GUI framework built with pygame-ce | https://github.com/bendikMichal/pyretro-gui |
| **repod** | 9 | Lightweight multiplayer network library for Python games | https://github.com/Walkercito/repod |
| **mili** | 10 | Minimal immediate-mode UI library for pygame-ce | https://github.com/damusss/mili |

---

## Summary & Recommendations

### Best Template for Prototyping Features
**The-Ultimate-Pygame-Structure** is the closest match to a full-featured boilerplate with scene management, input mapping, and configurable settings. It provides a cleanly separated project structure that can be extended with save/load and audio config.

### Best Scene Management Library
**game-state** is the most mature, well-documented, and actively maintained standalone scene management library for pygame(-ce). It can be pip-installed into any project.

### Gaps Observed
- **No single template** provides all five prototyping features (scene management + video settings + audio settings + input mapping + save/load).
- **Save/load systems** are entirely absent from existing pygame-ce templates.
- **Audio settings** (volume control, audio device selection) are not handled by any template found.
- Most pygame-ce tagged repos are complete games or utility libraries, not starter templates.

### Recommended Approach for painting-goblin
Consider combining **The-Ultimate-Pygame-Structure** (project scaffolding + scene management + input mapping) with **game-state** (for more robust state transitions) as a foundation, then add custom save/load and audio settings modules.

---

## Search Queries Used

1. `pygame-ce starter template` (GitHub repositories)
2. `pygame community edition boilerplate game jam` (GitHub repositories)
3. `pygame scene manager template` (GitHub repositories)
4. `pygame game template 2024` (GitHub repositories)
5. `pygame template scene manager` (GitHub repositories, sorted by stars)
6. `pygame-ce` topic page on GitHub (164 repos)
