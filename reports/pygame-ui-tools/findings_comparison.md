# Pygame UI Tools Comparison

**Date:** 2026-05-11
**Scope:** Actively maintained Pygame GUI libraries/toolkits

---

## Top Tools Overview

The two dominant, actively maintained Pygame GUI libraries are **pygame_gui** and **pygame-menu**. Smaller/less active tools (PyGVisuals, quack-gui) exist but lack the feature set, documentation, and community. These two are the only ones with substantial GitHub communities, regular releases, dedicated documentation sites, and pip distribution.

---

## Comparison Table

| Feature | pygame_gui | pygame-menu | PyGVisuals | quack-gui |
|---|---|---|---|---|
| **GitHub Stars** | 806 | 601 | 11 | 8 |
| **Forks** | 92 | 147 | 5 | 0 |
| **Commits** | 1,729 | 2,677 | 129 | 77 |
| **Releases** | 27 | 104 | 1 | 0 |
| **Open Issues** | ~60 | ~4 | ~6 | 0 |
| **Last Release** | May 30, 2025 | Apr 25, 2025 | Apr 23, 2020 | N/A |
| **License** | MIT | MIT | BSD-2-Clause | MIT |
| **Python Req.** | 3.10+ | 3.9+ | 3.x | 3.x |
| **Pygame Req.** | pygame-ce 2.5.3+ | pygame 1.9.3+/2.0+ | pygame 1.9.6/2.0 | pygame |
| **pip install** | `pygame_gui` | `pygame-menu` | source only | source only |
| **Doc Site** | readthedocs.io | readthedocs.io | GitHub Pages | README only |
| **Examples** | Separate repo (162 stars) | Included in repo | Included in repo | Included in repo |

---

## 1. pygame_gui (MyreMylar)

**URL:** https://github.com/MyreMylar/pygame_gui

### Widget Set
Extensive: buttons, text boxes (multi-line), sliders, dropdowns, scrollbars, file dialogs, colour pickers, status bars, UI forms, scrolling containers, text consoles, camera windows, checkboxes, radio buttons, image widgets, progress bars, separators, tooltips, draggable windows.

### Documentation
- Full ReadTheDocs site: https://pygame-gui.readthedocs.io/
- Separate examples repo: https://github.com/MyreMylar/pygame_gui_examples (162 stars)
- ~30+ example scripts covering individual features
- In-code docstrings

### Ease of Integration
- Designed to slot into existing pygame-ce game loops
- Event-driven: processes pygame events and generates its own UI events
- Minimal boilerplate: create `UIManager`, pass events, call `update()` and `draw()`
- Requires pygame-ce (not vanilla pygame)

### Styling/Theming
- Theme files in JSON format
- Per-widget-class styling (colours, borders, fonts, images)
- Can override individual widget or class defaults
- Supports images for button states (idle, hovered, pressed)
- HTML-style text formatting in labels

### Community & Activity
- 806 stars, 92 forks
- 1,729 commits, 27 releases
- Latest release: v0.6.14 (May 30, 2025) -- very active
- 60 open issues, 5 open PRs
- Single primary maintainer (MyreMylar / Dan Lawrence)
- codecov, CI, readthedocs integration

### Dependencies
- pygame-ce >= 2.5.3
- python-i18n (localization)

---

## 2. pygame-menu (ppizarror)

**URL:** https://github.com/ppizarror/pygame-menu

### Widget Set
Menu-focused: buttons, text inputs, colour inputs, clock/selectors, drop selectors (dropdowns), frames, images, labels, selectors, tables, colour switches. Strong on menu/menu-bar systems with submenus and transitions.

### Documentation
- Full ReadTheDocs site: https://pygame-menu.readthedocs.io/
- Detailed README.rst with examples
- Examples included in repository
- API docs auto-generated

### Ease of Integration
- Sits on top of pygame, wraps your game loop
- Menu-based paradigm (create menus, add widgets, then `mainloop()` or pump events)
- Works with both vanilla pygame (1.9.3+) and pygame-ce (via separate branch)
- Very low boilerplate for menu screens

### Styling/Theming
- Theme objects with ~30+ customizable parameters
- Supports background images, colours, borders, shadows, widget alignment, padding
- Multiple built-in themes
- Can create custom theme classes
- Top-level menu theming

### Community & Activity
- 601 stars, 147 forks
- 2,677 commits, 104 releases -- very high release frequency
- Latest release: v4.5.4 (Apr 25, 2025) -- very active
- Only 4 open issues -- well-maintained
- 0 open PRs
- Single primary maintainer (ppizarror / Pablo Pizarro R.)
- Ko-fi sponsorship
- codecov, CI, readthedocs, FOSSA integration

### Dependencies
- pygame >= 1.9.3 (or pygame-ce via `pygame-menu-ce` branch)
- No other runtime dependencies

---

## 3. PyGVisuals (Impelon)

**URL:** https://github.com/Impelon/PyGVisuals

### Widget Set
Basic: buttons, text labels, input fields, sliders, checkboxes. Functional but limited compared to the top two.

### Documentation
- GitHub Pages site: https://impelon.github.io/PyGVisuals/
- API documentation page
- README with basic usage
- Examples included in repository

### Ease of Integration
- Pure pygame, no special game loop requirements
- Can install via pip from git (no PyPI package)
- Lightweight and minimal

### Styling/Theming
- Basic colour/position customization
- No theme system or JSON configuration
- Styling done programmatically in code

### Community & Activity
- 11 stars, 5 forks
- 129 commits
- 1 release (v0.7, Apr 2020) -- effectively unmaintained
- 6 open issues, 0 open PRs
- Developer notes lack of motivation to continue

### Dependencies
- pygame (any modern version)
- Python 3

---

## 4. quack-gui (biggus-developerus)

**URL:** https://github.com/biggus-developerus/quack-gui

### Widget Set
Basic: buttons, text labels, simple inputs. Very early stage.

### Documentation
- README only with minimal usage
- Example apps included

### Ease of Integration
- Simple pip install from source
- Pure pygame
- Very early development, API likely unstable

### Styling/Theming
- Minimal, code-based only

### Community & Activity
- 8 stars, 0 forks
- 77 commits
- No releases
- Last updated May 2024
- Effectively a personal/hobby project

### Dependencies
- pygame
- Python 3

---

## Summary & Recommendations

### Choose pygame_gui if:
- You need a complete GUI system (not just menus) with many widget types
- You need file dialogs, colour pickers, draggable windows, scrollable containers
- You want JSON-based theming/theming files
- You're using pygame-ce (the modern, maintained pygame fork)
- You need HTML-style text formatting and localization support

### Choose pygame-menu if:
- Your primary need is menu screens (main menu, settings, options, pause menus)
- You want the simplest possible API for menus
- You use vanilla pygame (not pygame-ce), or want both options
- You want minimal dependencies (just pygame)
- You need the most battle-tested, release-stable option (104 releases)

### Don't choose PyGVisuals or quack-gui if:
- You need long-term support or active maintenance
- You need anything beyond basic widgets
- You want pip-installable packages from PyPI

### For new projects, the decision is:
- **Use pygame-ce + pygame_gui** for a full GUI desktop-application-like experience
- **Use pygame + pygame-menu** for game menus specifically, or if sticking with vanilla pygame
