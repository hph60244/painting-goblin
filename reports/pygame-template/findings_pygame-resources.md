# Pygame Game Jam Resources & Starter Template Research

## Key Findings

### 1. Curated Awesome Lists

**kadir014/awesome-pygame** (15 stars, 2 forks)
- URL: https://github.com/kadir014/awesome-pygame
- A curated list of Pygame tools, libraries, and frameworks.
- Categories covered:
  - **Graphics**: `pygame_shaders` — integrate shaders into pygame projects
  - **User Interfaces**: `mili` (immediate-mode UI), `pygame_gui` (full GUI system), `pygame-menu-ce` (menu library), `nevu-ui` (declarative game UI)
  - **Multimedia**: `pygame-video`, `richyplayer` (video player for pygame-ce)
  - **Gameplay Systems**: `pygbag` (WASM/web export), `pgcooldown` (cooldown/counter), `pytmx` (Tiled map loader, 420 stars), `pyscroll` (scrolling maps, 188 stars), `game-state` (state machine for screen management)

### 2. Direct Game Jam Starter Templates

**nick-cash/ldpygame** (0 stars)
- URL: https://github.com/nick-cash/ldpygame
- "A simple starter template for game jams using the Pygame library"
- Includes folders for: `fonts/`, `images/`, `sounds/`, and a core `ldpygame/` module
- Designed specifically for Ludum Dare-style game jams

**IEEE-CC-CSUDH/Example-Games-With-Pygame** (0 stars)
- URL: https://github.com/IEEE-CC-CSUDH/Example-Games-With-Pygame
- Template created as reference for IEEE CC's Game Jams
- Includes: `player.py`, `enemy.py`, `example.py`, `setup.py`
- Designed to run on Replit.com for easy collaboration

### 3. Major Pygame Ecosystem Libraries (for building a template)

| Library | Stars | Description | URL |
|---------|-------|-------------|-----|
| `pygame_gui` | 806 | Full GUI system (buttons, panels, etc.) | https://github.com/MyreMylar/pygame_gui |
| `pygame-menu` | 601 | Menu/GUI library (buttons, selectors, text input) | https://github.com/ppizarror/pygame-menu |
| `pygbag` | 496 | Package Pygame games to WASM for web (itch.io deploy) | https://github.com/pygame-web/pygbag |
| `pytmx` | 420 | Tiled Map Editor TMX loader | https://github.com/bitcraft/pytmx |
| `pyscroll` | 188 | Animated scrolling maps | https://github.com/bitcraft/pyscroll |
| `pygame_shaders` | — | Shader integration | https://github.com/ScriptLineStudios/pygame_shaders |
| `game-state` | — | State machine for screen management | https://github.com/Jiggly-Balls/game-state |

### 4. Reddit Discussions & Community Sentiment

Source: https://old.reddit.com/r/pygame/search/?q=template+game+jam&restrict_sr=on&sort=relevance&t=all

Key observations from the /r/pygame community:

- **Pygame Community Game Jams** are actively run: New Year's Jam, Spring Jam, Summer Jam — all organized via the Pygame Discord and hosted on itch.io.
- **Pygame vs. Godot debate**: Users note that Pygame requires manually implementing features (scene management, input handling) that engines provide out of the box, but prefer it for the learning experience and control (source: "Pygame vs Engine like Godot for game jams" thread).
- **Web export is a requirement** for many jams (itch.io). `pygbag` + `pygame-ce` is the standard solution.
- **DaFluffyPotato** is a well-known community figure who has completed multiple 48-hour game jams with Pygame.
- Users actively seek templates with: scene/state management, input mapping, save/load, and audio/video settings pre-built.

### 5. Recommended Feature Set for a Pygame Game Jam Template

Based on community discourse and library offerings, an ideal template should include:

1. **Scene/State Management** — `game-state` library or custom state stack
2. **GUI/Menus** — `pygame-menu` or `pygame_gui` for settings screens
3. **Input Mapping** — configurable key bindings
4. **Audio Settings** — volume control, mute toggle
5. **Video Settings** — resolution, fullscreen toggle
6. **Save/Load System** — JSON or pickle-based persistence
7. **Map Loading** — `pytmx` + `pyscroll` for Tiled map support
8. **Web Export** — `pygbag` for WASM/itch.io deployment
9. **Asset Management** — organized folder structure (fonts/, images/, sounds/)
10. **Cooldown/Timer System** — `pgcooldown` for time-based events

### 6. Game Jams Actively Using Pygame

- Pygame Community Jam (itch.io): https://itch.io/jam/pygame-community-jam
- GMTK Game Jam (multiple Pygame entries documented on Reddit)
- Pirate Software Game Jam
- Boss Rush Game Jam
- Simplicity Game Jam
- FishFest Game Jam
- Global Game Jam (2026 entry documented)

### 7. Notable Community Contributors

| Handle | Contribution |
|--------|------------|
| DaFluffyPotato | Multiple 48h jam completions, active tutorial creator |
| MyreMylar | Maintainer of `pygame_gui` and `pygame-ce` |
| ppizarror | Creator of `pygame-menu` |
| bitcraft | Creator of `pytmx` and `pyscroll` |
| pmp-p | Creator of `pygbag` (Pygame WASM) |
| kadir014 | Maintainer of awesome-pygame list and `pygame-video` |

### 8. Gaps in the Ecosystem

- **No single "standard" game jam template** exists with broad adoption
- Most templates are old, unmaintained, or very minimal
- No template currently bundles all the recommended features (scene management, input mapping, save/load, video/audio settings) in one package
- Community relies on fragmenting across individual libraries rather than a cohesive starter kit

## Sources

- https://github.com/kadir014/awesome-pygame
- https://github.com/nick-cash/ldpygame
- https://github.com/IEEE-CC-CSUDH/Example-Games-With-Pygame
- https://github.com/MyreMylar/pygame_gui
- https://github.com/ppizarror/pygame-menu
- https://github.com/pygame-web/pygbag
- https://github.com/bitcraft/pytmx
- https://github.com/bitcraft/pyscroll
- https://github.com/Jiggly-Balls/game-state
- https://github.com/ScriptLineStudios/pygame_shaders
- https://old.reddit.com/r/pygame/
