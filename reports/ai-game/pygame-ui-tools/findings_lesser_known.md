# Lesser-Known / Emerging Pygame UI Tools (Updated Since 2023)

Research conducted: May 11, 2026
Sources: GitHub repository search, PyPI, r/pygame, Stack Overflow

---

## 1. EasyPygameWidgets (pywidgets)

- **URL**: https://github.com/PizzaPost/pywidgets
- **PyPI**: `pip install easypygamewidgets`
- **Latest Update**: ~May 9, 2026 (active)
- **Stars**: 0 (very new)
- **License**: MIT

### Key Features
- Retained-mode widget library for pygame / pygame-ce
- Screen management system for grouping widgets
- Tooltip support
- Customizable styling (colors, sounds, cursors)
- Built-in timekeeper/stopwatch widget

### Widget Set
Button, Slider, Entry (text input), Label, Surface wrapper, Screen (container), Timekeeper, Tooltips

### Assessment
Very new (72 commits). Clean API with `epw.link_pygame_window()`, `epw.handle_event()`, `epw.flip()` pattern. On PyPI. Good for beginners needing simple UIs. Limited widget variety but well-documented with examples. Low maturity but promising.

---

## 2. ILoveUI.py

- **URL**: https://github.com/extlalala/ILoveUI.py
- **PyPI**: No (single-file library)
- **Latest Update**: ~April 22, 2026 (active)
- **Stars**: 1
- **License**: MIT

### Key Features
- Immediate-mode GUI (IMGUI) style - UI rebuilt every frame
- No external dependencies beyond pygame
- Flexible layout system: Box, Row, Column, Lazy List
- Animation support with coroutine-based transitions
- Popup system: Toast, Dialog, Draggable Windows
- Built-in debugging tools: render layer control, performance monitor, rect visualization
- Event system: mouse, keyboard, touch, scroll

### Widget Set
Text, Button (clickable text), TextField/Input, Slider, ScrollView, LazyScrollList, Popup/Toast/Dialog/Window

### Assessment
Feature-rich immediate-mode library. Unique IMGUI approach differentiates it from retained-mode alternatives. Strong layout system. Good for rapid prototyping and debug UIs. Chinese/English bilingual docs. Low star count but technically mature (34 commits). Recommended for dev tools and debug overlays.

---

## 3. UINEX

- **URL**: https://github.com/djoezeke/uinex
- **PyPI**: `pip install uinex`
- **Latest Update**: April 4, 2026
- **Stars**: 1
- **License**: MIT

### Key Features
- Immediate-mode GUI library for pygame
- Modern-looking UI with theming support
- Pillow integration for image loading
- Extensions system for `[standard]` install
- CI/CD with tests, mkdocs documentation
- UV-based project management

### Widget Set
General immediate-mode widgets (customization examples provided, theming support)

### Assessment
Polished project with proper documentation site, tests, and dependency management. Modern theming approach. 58 commits. Available on PyPI. Good for developers who want a clean, well-structured immediate-mode GUI with docs.

---

## 4. Guipy (guipylib)

- **URL**: https://github.com/jasonzh0/guipy
- **PyPI**: `pip install guipylib`
- **Latest Update**: March 4, 2026
- **Stars**: 5
- **License**: MIT

### Key Features
- Research/simulation-focused UI components
- Live plotting and graphing widgets (unique)
- GUIManager for centralized event handling
- Modern visual style
- Focus on prototyping in corporate/research settings

### Widget Set
Button, Dropdown, Live Plot, Plot (static), Slider, Switch, Textbox

### Assessment
Standout feature: built-in live plotting (unusual for pygame UI libs). Good for scientific visualization, simulations, graphing tools. 40 commits, 5 stars, 1 fork. Active development with CI. Well-documented with GitHub Pages. Recommended for any project needing real-time graphs/charts in pygame.

---

## 5. pygame-widget-kit

- **URL**: https://github.com/sinanorgu/pygame-widget-kit
- **PyPI**: `pip install pygame-widget-kit`
- **Latest Update**: May 5, 2026 (very active)
- **Stars**: 0 (brand new)
- **License**: MIT

### Key Features
- Retained-mode UI with component tree
- Event routing with hover, focus, and active state
- Modal/dropdown support via UIManager
- TextInput with mouse-based text selection and clipboard
- Input filtering modes: text, number, hex, binary, octal
- CodeEditor widget with syntax highlighting + autocomplete provider hook

### Widget Set
Button, Text (label), Select/Dropdown, Radio, TextInput, Slider, TextArea, CodeEditor

### Assessment
Most feature-rich of the new crop. CodeEditor with syntax highlighting is unique. Text input filtering is polished (number-only, hex, binary, etc.). 34 commits, actively developed. On PyPI. Advanced widget set rivals established libs like pygame-gui. Recommended for any project needing text input, code editing, or dropdown menus.

---

## 6. plasticism-widgets

- **URL**: https://github.com/ChenWuwei404/plasticism-widgets
- **PyPI**: Not yet
- **Latest Update**: March 17, 2026
- **Stars**: 2
- **License**: GPL-3.0

### Key Features
- Qt-styled architecture (event stream processing system)
- Three-part widget design: event handler, rendering, extensions
- EventProcessor pipeline (e.g., ButtonStateMachine -> ButtonClicked)
- Resizable window support built-in
- ReadTheDocs documentation

### Widget Set
Label, Button, ToggleButton (composable via event processors), Window container

### Assessment
Unique Qt-inspired design philosophy with event processor pipelines. 108 commits - significant development. GPL-3.0 license (viral, unlike MIT alternatives). Still pre-release (no PyPI package). Interesting for those who like Qt's signal/slot mental model. Less practical for shipping games due to GPL.

---

## 7. SpritePro

- **URL**: https://github.com/NeoXider/SpritePro
- **PyPI**: `pip install spritepro`
- **Latest Update**: May 2, 2026 (v3.9.3, very active, 66 releases)
- **Stars**: 4
- **License**: Open Source

### Key Features
- High-level 2D game framework (not just UI)
- Full UI system: Button, ToggleButton, Slider, TextInput, TextSprite
- Layout system: Flex, Grid, Circle, Line
- ClipMask for viewport/inventory/chat clipping
- ScrollView with mouse wheel and drag-and-drop
- Integrated pymunk physics
- Visual Sprite Editor (scene builder -> JSON)
- Built-in multiplayer (TCP, lobbies, ChatScene)
- Mobile/web support (Kivy backend)
- Animation/Tween system
- Particle system

### Widget Set
Button, ToggleButton, Slider, TextInput, TextSprite (label), Layout (flex/grid/circle/line), ScrollView, ClipMask

### Assessment
Most mature and ambitious project listed. More of a full game framework (like a lighter pygame-ce alternative to Unity) than a pure UI library. 219 commits, 66 releases, version 3.9.3. Russian documentation, some English. Excellent UI system as part of a larger ecosystem. Recommended if you want a full framework rather than just UI widgets.

---

## 8. Guinea

- **URL**: https://github.com/m4reQ/guinea
- **PyPI**: Not confirmed
- **Latest Update**: October 18, 2024
- **Stars**: 2
- **License**: MIT

### Key Features
- Lightweight widget module
- Ready-to-use GUI widgets
- Minimal and simple API

### Widget Set
Basic widgets (specific set not detailed in README)

### Assessment
Small, lightweight project. 25 commits. Minimal documentation. Last updated Oct 2024. Suitable for very simple UI needs but lacks feature depth compared to others. Low activity suggests it may not be actively maintained.

---

## 9. pgwidget

- **URL**: https://github.com/DovaX/pgwidget
- **PyPI**: `pip install pgwidget`
- **Latest Update**: September 6, 2025
- **Stars**: 5
- **License**: MIT

### Key Features
- GUI widgets for pygame + experimental web engine support
- Main program loop wrapper
- Spreadsheet/table widget (unique)

### Widget Set
Checkbox, Radio button, Image Button, Classical Button, Table/Spreadsheet

### Assessment
Mature (212 commits). Unique table/spreadsheet widget not found in other libs. Experimental web support. 5 stars, 1 fork. Good for data-entry UIs and spreadsheet-like interfaces. Less active recently (last update Sep 2025).

---

## Summary Table

| Library | Type | Widgets Count | PyPI | Last Update | Standout Feature |
|---|---|---|---|---|---|
| EasyPygameWidgets | Retained | ~7 | Yes | May 2026 | Screen management |
| ILoveUI.py | Immediate | ~8+ | No | Apr 2026 | Lazy lists, animations, debug tools |
| UINEX | Immediate | ~5+ | Yes | Apr 2026 | Theming, docs, CI/CD |
| Guipy | Retained | ~7 | Yes | Mar 2026 | Live plotting |
| pygame-widget-kit | Retained | ~8 | Yes | May 2026 | CodeEditor, input filtering |
| plasticism-widgets | Retained (Qt-like) | ~4 | No | Mar 2026 | Event processor pipeline |
| SpritePro | Full framework | ~7+ | Yes | May 2026 | Full game framework + UI |
| Guinea | Retained | Minimal | No | Oct 2024 | Lightweight/simple |
| pgwidget | Retained | ~5 | Yes | Sep 2025 | Spreadsheet/table |

## Recommendations

**For in-game debug UIs / rapid prototyping**: ILoveUI.py (immediate-mode, no state management, built-in debug tools)

**For polished applications with text input**: pygame-widget-kit (CodeEditor, input filtering, clipboard)

**For scientific/research visualization**: Guipy (live plotting, sliders, switches)

**For a full game framework with UI**: SpritePro (scenes, physics, multiplayer, editor)

**For simple/small projects**: EasyPygameWidgets or UINEX (easy to learn, on PyPI)
