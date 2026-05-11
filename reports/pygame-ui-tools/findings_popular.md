# Popular Pygame UI Libraries - Research Findings

**Date:** 2026-05-11
**Researched by:** opencode

---

## 1. pygame-gui

| Field | Value |
|---|---|
| **Name** | pygame-gui |
| **GitHub URL** | https://github.com/MyreMylar/pygame_gui |
| **PyPI URL** | https://pypi.org/project/pygame-gui/ |
| **Latest Version** | v0.6.14 |
| **Latest Release Date** | May 30, 2025 |
| **Last Commit** | May 30, 2025 (v0.6.14 tag) |
| **Total Commits** | 1,729 |
| **Stars** | 806 |
| **Forks** | 92 |
| **License** | MIT |
| **Python Support** | 3.10+ |
| **Dependency** | Pygame Community Edition 2.5.3+ |
| **Downloads** | Consistent, tracked on pepy.tech |

### Recent Release History (last 2 years)

| Version | Date |
|---|---|
| 0.6.14 | May 30, 2025 |
| 0.6.13 | Dec 29, 2024 |
| 0.6.12 | Jun 16, 2024 |
| 0.6.11 | Jun 9, 2024 |
| 0.6.10 | Apr 14, 2024 |
| 0.6.9 | Apr 23, 2023 |
| 0.6.8 | Jan 8, 2023 |

### Key Features

- Full widget set: buttons, labels, text boxes, sliders, dropdown menus, progress bars, images, panels, windows, scrolling containers, tab containers, forms, colour pickers, 2D sliders, checkboxes
- HTML-style text formatting with hyperlinks
- i18n/localization support (17+ languages including Arabic, Hebrew, Korean, Georgian, Ukrainian)
- Theme files (JSON-based CSS-like theming with full control over colours, borders, fonts, images)
- Text shaping and right-to-left language support (via pygame-ce/SDL_ttf/Harfbuzz)
- Text selection and clipboard copy/paste
- Anchoring system for responsive/resizable layouts
- Tooltip support on most elements
- Active community with multiple contributors per release

### Maintenance Assessment

**ACTIVELY MAINTAINED.** This is the go-to GUI library for Pygame CE. The author (MyreMylar/Dan Lawrence) is highly responsive, with 6 releases in ~2 years, extensive changelogs, active issue triage (60 open issues), ongoing PR review, and support for Python 3.13. The library switched from old Pygame to Pygame CE in v0.6.9 and has been continuously improved with major feature additions (tabs, forms, checkboxes, 2D sliders, text shaping).

---

## 2. PGU (Pygame Utilities / pygame-pgu)

| Field | Value |
|---|---|
| **Name** | PGU - PyGame Utilities |
| **GitHub URL** | https://github.com/parogers/pgu |
| **PyPI URL** | https://pypi.org/project/pygame-pgu/ |
| **Latest Version** | 0.21 |
| **Latest Release Date** | Apr 19, 2019 |
| **Last Commit** | Unknown (repo auto-exported from Google Code, 67 total commits) |
| **Stars** | 97 |
| **Forks** | 36 |
| **License** | LGPL-2.1 |
| **Python Support** | Python 3 (per PyPI classifiers) |

### Key Features

- GUI widgets with standard widget set, dialogs, HTML rendering, CSS-box-model themes
- Tile/level editors (tileedit, leveledit) with isometric and hexagonal format support
- Sprite engines: tilevid, isovid (isometric), hexvid (hexagonal)
- Layout utilities, text rendering, HTML rendering
- Pathfinding algorithms, high score tracking, animation helpers
- Timer module for fixed-rate FPS
- Bitmapped font support

### Maintenance Assessment

**NOT ACTIVELY MAINTAINED.** The last PyPI release was in April 2019 (over 7 years ago). The GitHub README explicitly states: *"PGU is in need of more contributors."* The repo is an automated export from the now-defunct Google Code platform. While the codebase is functional and has historical significance, there is no active development, no recent releases, and no maintainer responsiveness. The project mentions someone (jsbueno) was "likely making a Python-3 only release soon" but no release has materialized since 2019.

---

## 3. Other Notable Pygame UI Toolkits

### Pygame Community Edition (pygame-ce)

- **URL:** https://pyga.me / https://github.com/pygame-community/pygame-ce
- While not a UI library itself, pygame-ce (the community fork of Pygame) is the modern, actively maintained Pygame distribution that pygame-gui depends on. It includes built-in `pygame._sdl2` UI features (window, texture, renderer) and improved text/font rendering via SDL_ttf + Harfbuzz.

### pygame-widgets

- A lightweight widget library found on PyPI and GitHub, but the primary repository appears to have low activity. No significant releases since ~2021. Offers basic widget set (buttons, sliders, text boxes) with minimal dependencies.

### Custom/In-House Solutions

- Most Pygame game developers either use **pygame-gui** or build custom UIs directly with pygame's drawing primitives (rect, blit, font rendering). There are no other actively maintained, feature-complete GUI libraries for Pygame that match pygame-gui's scope and activity level.

---

## Summary & Recommendation

| Library | Active? | Verdict |
|---|---|---|
| **pygame-gui** | Yes | **Recommended.** The only actively maintained, full-featured GUI toolkit for Pygame CE. |
| **PGU** | No | Not recommended for new projects. Legacy codebase with no updates since 2019. |
| **pygame-widgets** | No | Minimal activity, limited features. Not recommended. |
| **DIY / pygame-ce builtins** | N/A | Viable for simple UIs but requires significant custom work for complex interfaces. |

**Bottom line:** For any new Pygame project requiring a GUI, **pygame-gui** is the clear choice. It is actively maintained, well-documented, feature-rich, and has a growing community. If you only need very simple UI (a few buttons and text labels), consider using pygame-ce's built-in drawing primitives to avoid external dependencies.
