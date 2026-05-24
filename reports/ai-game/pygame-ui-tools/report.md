# Pygame UI Tools Research Report

**Date:** 2026-05-11
**Question:** 尋找Pygame的UI工具，近3年還有在更新 (Find Pygame UI tools still updated in the last 3 years)

---

## Executive Summary

There is a healthy ecosystem of actively maintained Pygame UI libraries. The landscape splits into two categories: **established/mature** libraries with large communities, and **newer/emerging** libraries with specialized features.

---

## Tier 1: Established & Recommended

### 1. pygame-gui ★ Top Pick for Full GUI
- **GitHub:** https://github.com/MyreMylar/pygame_gui (806★)
- **PyPI:** `pip install pygame-gui`
- **Latest:** v0.6.14 (May 30, 2025) — very active
- **Requires:** pygame-ce 2.5.3+
- **License:** MIT
- **Widgets:** Buttons, text boxes, sliders, dropdowns, file dialogs, colour pickers, forms, scroll containers, tabs, checkboxes, progress bars, draggable windows, tooltips
- **Theming:** JSON-based theme files (CSS-like), per-widget styling
- **Docs:** Full ReadTheDocs, separate examples repo (162★)
- **Standout:** Most complete widget set, HTML text formatting, i18n (17+ languages), RTL language support
- **Use if:** You need a full desktop-application-like GUI and are using pygame-ce

### 2. pygame-menu ★ Top Pick for Menus
- **GitHub:** https://github.com/ppizarror/pygame-menu (601★)
- **PyPI:** `pip install pygame-menu`
- **Latest:** v4.5.4 (Apr 25, 2025) — very active (104 releases)
- **Requires:** pygame 1.9.3+ (also works with pygame-ce via branch)
- **License:** MIT
- **Widgets:** Menu-focused — buttons, text inputs, colour inputs, selectors, dropdowns, tables, frames, labels
- **Theming:** Theme objects with ~30 customizable parameters, multiple built-in themes
- **Docs:** Full ReadTheDocs with auto-generated API docs
- **Standout:** Most battle-tested (104 releases), works with vanilla pygame, zero runtime deps beyond pygame
- **Use if:** Your primary need is game menus (main menu, pause, settings) or you use vanilla pygame

---

## Tier 2: Emerging & Specialized (All Updated 2025-2026)

| Library | Type | Last Update | Standout Feature |
|---------|------|-------------|------------------|
| **pygame-widget-kit** | Retained | May 2026 | CodeEditor with syntax highlighting, input filtering |
| **SpritePro** | Full framework | May 2026 | Complete game framework + UI, physics, multiplayer |
| **EasyPygameWidgets** | Retained | May 2026 | Beginner-friendly, screen management |
| **ILoveUI.py** | Immediate-mode | Apr 2026 | IMGUI, lazy lists, animations, debug tools |
| **UINEX** | Immediate-mode | Apr 2026 | Modern theming, docs, CI/CD |
| **Guipy** | Retained | Mar 2026 | Live plotting widget (unique) |
| **plasticism-widgets** | Qt-like | Mar 2026 | Event processor pipeline (GPL-3.0) |
| **pgwidget** | Retained | Sep 2025 | Spreadsheet/table widget (unique) |

---

## Tier 3: Not Recommended (Stale/Unmaintained)

- **PGU (pygame-pgu)** — Last release Apr 2019, asks for maintainers
- **pygame-widgets** — No significant updates since ~2021
- **PyGVisuals** — Last release Apr 2020, developer lacks motivation
- **quack-gui** — Last updated May 2024, hobby project
- **Guinea** — Last updated Oct 2024, low activity

---

## Decision Guide

| Your Need | Recommendation |
|-----------|---------------|
| Full GUI system (forms, dialogs, windows) | **pygame-gui** + pygame-ce |
| Game menus (main menu, pause, settings) | **pygame-menu** (works with vanilla pygame) |
| In-game debug overlays / dev tools | **ILoveUI.py** (immediate-mode, lightweight) |
| Text input / code editor | **pygame-widget-kit** |
| Scientific visualization / live plotting | **Guipy** |
| Full 2D game framework with UI | **SpritePro** |
| Simple, beginner-friendly widgets | **EasyPygameWidgets** or **UINEX** |

---

## Key Takeaway

**pygame-gui** is the most complete and actively maintained general-purpose UI toolkit for Pygame, but requires **pygame-ce**. If you need to stay on vanilla pygame, **pygame-menu** is an excellent choice for menu systems. For specialized needs (plotting, code editing, IMGUI), the newer libraries offer compelling alternatives.
