# Game Engine Options for AI Coding Agent — Research Findings

**Date:** 2026-04-27
**Goal:** Evaluate Godot Engine (GDScript) and Raylib (Python bindings) for rapid game prototyping by an AI coding agent (Claude, GPT, etc.)

---

## 1. Godot Engine (with GDScript)

### 1.1 GitHub Stats
- **Stars:** ~110k — godotengine/godot (https://github.com/godotengine/godot)
- **Forks:** ~25.1k
- **Releases:** 68 stable releases; latest v4.6.2 (Apr 2026)
- **Contributors:** Large, active community; 83k+ commits
- **License:** MIT (completely free, no royalties)

### 1.2 API & AI Agent Suitability
- GDScript is Python-like syntax, making it relatively easy for LLMs to generate. However, GDScript is Godot-specific — most LLMs have seen GDScript in training data but not to the same depth as Python/JavaScript.
- Godot uses a **scene tree + node-based architecture** with signal/slot patterns. LLMs generally understand this, but the generated code may require the visual editor for scene setup (creating `.tscn` files with correct node hierarchies).
- **Key API concepts an AI must get right:** `extends Node2D`/`extends Sprite2D`, `_ready()`, `_process(delta)`, `Input.is_action_just_pressed()`, `preload()`, signals, and `@onready` syntax.

### 1.3 Editor Required vs. Code-Only
- **Can be used code-only:** Yes. Godot supports command-line execution including `--script`, `--headless`, `--check-only`, and `--export-release`.
- Documentation explicitly states: *"Some developers like using the command line extensively. Godot is designed to be friendly to them… Given the engine relies on almost no external libraries, initialization times are pretty fast, making it suitable for this workflow."* (https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)
- Export pipeline is fully CLI-able: `godot --headless --export-release "Linux/X11" /var/builds/project`
- **However:** Most Godot workflows assume the editor for scene creation, resource management, and visual layout. Going code-only means manually creating `.tscn` files as structured text or doing everything procedurally in GDScript — which is possible but not the primary workflow.
- **Verdict:** Code-only is supported but secondary. An AI agent can generate a complete project structure with `project.godot`, `.gd` scripts, and `.tscn` scenes, then execute it headlessly.

### 1.4 Boilerplate for a Simple Game
- **Minimal Godot project:** Create `project.godot` (4 lines), a main scene `.tscn` file, and a script. For a simple "Hello World" window:
  - `project.godot` (~5 lines of config)
  - A root node scene (can be created via script alone or a minimal `.tscn`)
  - A `.gd` script with `_ready()` and `_process()` (~10-15 lines)
- **Total for minimal window:** ~20-30 lines across 2-3 files.
- **For a simple game (Pong, Breakout):** ~100-200 lines of GDScript across multiple files.

### 1.5 Documentation Quality & LLM Training Data Coverage
- **Official documentation:** Comprehensive, hosted at docs.godotengine.org, includes class reference, step-by-step tutorials, and contributed guides. Maintained on GitHub (godotengine/godot-docs).
- The full class reference is accessible from within the editor.
- **LLM training data coverage:** Godot is a prominent open-source project. GDScript code and documentation are widely represented in CommonCrawl and GitHub-based training datasets. However:
  - GDScript is less represented than Python or JavaScript in LLM training.
  - Godot 4.x broke compatibility with Godot 3.x. LLMs may generate outdated Godot 3 syntax.
  - Godot 4.0+ API changes (e.g., `KinematicBody2D` → `CharacterBody2D`) may trip up LLMs trained on older data.
- **Verdict:** Moderate coverage. An AI agent will generate plausible GDScript ~70-80% of the time for common patterns, but will need careful prompting about Godot 4.x specifics.

### 1.6 Export/Package Workflow
- Export to Windows, macOS, Linux, Android, iOS, Web (HTML5).
- Export templates must be downloaded separately (~200 MB).
- CLI export: `godot --headless --export-release "Windows Desktop" builds/game.exe`
- **CI/CD friendly:** Yes. The `--headless` flag enables export on servers without GPUs.
- Self-contained `.pck` files or single executable per platform.

### 1.7 Community Size
- **Massive.** ~110k GitHub stars, 1.5k watchers, 25k forks.
- Active Discord, Reddit (r/godot), Godot Contributors Chat.
- Extensive ecosystem of addons, tutorials, and assets.

---

## 2. Raylib (with Python bindings — raylib-python-cffi)

### 2.1 GitHub Stats
- **Raylib core (C):** 32.6k stars, 3.1k forks (https://github.com/raysan5/raylib)
- **Raylib Python bindings:** 236 stars, 42 forks (https://github.com/electronstudio/raylib-python-cffi)
- **Latest bindings version:** 5.5.0.4 (Dec 2025); raylib C core at v6.0 (Apr 2026)
- **License:** zlib/libpng (C core), EPL-2.0 (Python bindings)

### 2.2 API Simplicity
- "A simple and easy-to-use library to enjoy videogames programming" — README
- **Extremely flat API:** ~600 functions organized into modules (rcore, rshapes, rtextures, rtext, rmodels, raudio).
- No complex inheritance hierarchies or component systems. Just functions around a game loop.
- **Cheatsheet available:** https://www.raylib.com/cheatsheet/cheatsheet.html — single-page reference for all functions.

### 2.3 Python Bindings Quality
- Uses CFFI (not ctypes) — *"Faster, fewer bugs and easier to maintain than ctypes"* (README).
- Supports type checking with MyPy.
- Docstrings and auto-completion work in IDEs.
- **Two modules:** `raylib` (exact C API mirror) and `pyray` (more Pythonic API).
- **Multiple backends:** Desktop (GLFW), SDL, DRM, Web, Software rendering.
- **Performance:** ~5.8% of native C performance on CPython; ~53% on PyPy (per Bunnymark benchmark). See README for exact numbers.

### 2.4 Boilerplate for a Simple Game
```python
from pyray import *

init_window(800, 450, "Hello")
while not window_should_close():
    begin_drawing()
    clear_background(WHITE)
    draw_text("Hello world", 190, 200, 20, VIOLET)
    end_drawing()
close_window()
```
- **Minimal window:** 8 lines of Python (including imports).
- **Simple game (Pong, Snake):** ~80-150 lines. Extremely concise.
- **No project files, no scene files, no config.** Just a single `.py` file.
- **Verdict:** Minimal boilerplate. The lowest barrier to entry of all evaluated options.

### 2.5 Documentation & Examples
- No standard API docs per se — relies on the cheatsheet and ~140 C code examples (also ported to Python).
- Python bindings have auto-generated docs at https://electronstudio.github.io/raylib-python-cffi
- **The raylib philosophy:** *"raylib is designed to be learned using the examples as the main reference."* (README)
- **LLM coverage:** Raylib's C API is well-represented in training data, but the Python bindings are less prominent. An AI agent is more likely to generate correct raylib C code than correct `pyray` code.
- The bindings repo includes a `CLAUDE.md` and `AGENTS.md` file — indicating explicit AI agent support (https://github.com/electronstudio/raylib-python-cffi/blob/master/CLAUDE.md).

### 2.6 Community Size
- **Raylib core:** 32.6k stars — strong but niche compared to Godot.
- **Python bindings:** 236 stars — very small community.
- Discord servers: raylib general (~20k members), raylib Python (much smaller).
- **Binding to 70+ languages** — raylib has impressive polyglot reach.

---

## 3. Comparison with Alternatives

### 3.1 Pygame (Python)
- **Stars:** 8.7k (https://github.com/pygame/pygame)
- **License:** LGPL
- **Boilerplate:** ~10 lines for minimal window. Comparable to raylib.
- **LLM coverage:** Very high. Pygame is the most common Python game library in LLM training data. LLMs generate correct Pygame code with high reliability.
- **Pros:** Massive ecosystem, most LLM training data of any option, mature, widely taught.
- **Cons:** Slower than raylib, older API, LGPL license may concern some projects, no built-in 3D.

### 3.2 Arcade (Python)
- **Stars:** 2k (https://github.com/pythonarcade/arcade)
- **License:** MIT
- **Description:** "Easy-to-learn Python library for creating 2D video games. Ideal for beginning programmers." Built on pyglet and OpenGL.
- **Boilerplate:** ~15 lines for minimal window.
- **LLM coverage:** Moderate. Less training data than Pygame but more than raylib Python.
- **Pros:** Clean modern API, good documentation, built-in physics, MIT licensed.
- **Cons:** Smaller community, 2D only, relatively slow development.

### 3.3 Phaser (JavaScript/TypeScript)
- **Stars:** 39.5k (https://github.com/phaserjs/phaser)
- **License:** MIT
- **Platform:** Web (HTML5 + Canvas/WebGL)
- **LLM coverage:** Very high. Phaser README explicitly states: *"Phaser's API is well understood by every major frontier LLM. This repository includes a comprehensive set of AI agent skills that give coding agents deep knowledge of every Phaser subsystem, making it the ideal framework for AI-assisted game development."*
- **Boilerplate:** ~20 lines HTML + JS for minimal game.
- **Pros:** Instant sharing (just a URL), huge community, official AI skill files, TypeScript support, Phaser 4 just released with massive improvements.
- **Cons:** Browser-only by default (can wrap with Electron/Capacitor), JavaScript toolchain complexity (npm, bundlers), no native desktop/mobile builds.

### 3.4 Kaboom.js (JavaScript)
- **Stars:** 2.7k (https://github.com/replit/kaboom) — **now archived.**
- **Status:** Replit no longer maintains Kaboom. Community fork is KaPlay.
- **License:** MIT
- **Pros:** Extremely concise API, great for prototyping.
- **Cons:** **Archived/unmaintained.** Not recommended for new projects.

---

## 4. Summary & Recommendations for AI Agent Rapid Prototyping

| Criterion | Godot (GDScript) | Raylib (Python) | Pygame | Arcade | Phaser |
|---|---|---|---|---|---|
| **GitHub Stars** | 110k | 32.6k (C) / 236 (Python) | 8.7k | 2k | 39.5k |
| **Boilerplate** | Medium (3 files) | Very Low (1 file) | Low (1 file) | Low (1 file) | Medium (npm + HTML) |
| **LLM Coverage** | Moderate | Low-Moderate | **Very High** | Moderate | **Very High** |
| **Code-Only Workflow** | Supported but secondary | **Primary** | **Primary** | **Primary** | **Primary** |
| **Export Targets** | Desktop/Mobile/Web | Desktop/Web | Desktop | Desktop | Web (native via wrapper) |
| **Learning Curve** | Steepest | Lowest | Low | Low | Moderate |
| **3D Support** | Yes | Yes | No | No | No (2D only) |
| **Performance** | Native (C++) | ~5-53% of native C | Good (SDL) | Good (OpenGL) | Good (WebGL) |

### Key Findings

1. **For an AI agent prototyping quickly with Python:** **Raylib (pyray)** or **Pygame** are the best choices. They require a single `.py` file, no project scaffolding, and `pip install` is the only setup needed. Pygame has better LLM training data coverage. Raylib has a cleaner API.

2. **For web-first prototypes with maximum LLM support:** **Phaser 4** is the strongest option. It ships with official AI agent skill files, is widely represented in LLM training data, and enables instant sharing via URL. Its README aggressively positions it as "AI-ready."

3. **Godot is overkill for rapid prototyping** — it's a full editor-based engine. While it can be used code-only, the workflow fights the tool's design philosophy. Use Godot when you need a complete game with polished export to multiple platforms, not for quick idea testing.

4. **Kaboom.js is effectively dead** — archived by Replit. Avoid.

5. **For pure simplicity:** The order is Raylib ≈ Pygame < Arcade < Phaser < Godot (from simplest to most complex).

6. **The Python-FFI overhead matters:** Raylib Python reaches only ~5.8% of native C performance on CPython (53% on PyPy). For simple games this is fine; for sprite-heavy games, Pygame or pure Python may keep up better.

7. **Godot's export pipeline is superior** for actually shipping a game, but the friction of generating correct `.tscn` files and GDScript from an LLM is higher.
