# Research Findings: Best Tools/Libraries & Prompting Strategies for AI to Create Pixel Games

## 1. Recommended Game Frameworks for AI Code Generation

### Tier 1: Best Fit for AI Generation

| Framework | Language | Stars | Why AI-Friendly | Pixel Suitability |
|-----------|----------|-------|-----------------|-------------------|
| **Pyxel** | Python | 17.4k | Built-in CLAUDE.md with AI coding policies; simple API (16 colors, 256x256 screen, 4 sound channels); web editor (Pyxel Studio) for instant testing | Excellent - retro pixel focus |
| **Pygame** | Python | ~7k (topic) | Simple imperative API; massive ecosystem; well-known by AI training data | Good - flexible but verbose |
| **Godot** | GDScript/C# | ~85k | Node/scene system maps well to AI output; dedicated 2D engine; open source with no licensing fees | Very Good - built-in pixel art tools, tilemaps |
| **Phaser** | JS/TS | ~38k | Browser-based (instant play); simple config; huge community examples | Good - canvas-based rendering |
| **GameMaker** | GML | N/A | Just added **Claude Code CLI integration** for AI-assisted workflows; focused on 2D | Excellent - dedicated 2D engine |

### Tier 2: Viable but with Caveats

| Framework | Notes |
|-----------|-------|
| **Unity** | Too complex for AI; heavy editor dependencies; confusing output; AI tends to fight the ECS/component system |
| **Bevy** (Rust) | Modern ECS but Rust ownership model confuses AI; produces non-compiling code frequently |
| **Raylib** (C/C++) | Simple API but C memory management trips up AI; better for small demos than full games |
| **Love2D** (Lua) | Simple but Lua's lack of OOP conventions leads AI to produce inconsistent code |
| **TIC-80** (Lua) | Fantasy console like PICO-8; limited scope helps AI; but niche community = less training data |

### Key Insight: Pyxel Stands Out

Pyxel is the clear winner for AI-generated pixel games because:
- **CLAUDE.md file** in the repository explicitly provides AI coding policies (naming conventions, structure, performance rules) - this is built for AI collaboration
- **16-color palette** and **256x256 resolution** keep scope small and manageable for AI
- **Python** is the most-trained language across all AI models
- **Built-in editors** for sprites, tilemaps, sounds, and music - no external tools needed
- **Pyxel Studio** provides a web-based IDE for instant iteration

Source: https://github.com/kitao/pyxel (17.4k stars, MIT license)

### GameMaker's New AI Integration

GameMaker (by Opera) recently launched **GM-CLI with Claude Code integration** (April 30, 2026). Users can:
- Query project structures via natural language
- Hunt down bugs
- Manage build configurations
- Use GitHub Actions and MCP Server for automation

Source: https://www.gamedeveloper.com/production/gamemaker-incorporates-claude-code-to-enable-ai-assisted-workflows

---

## 2. Prompting Strategies for AI Game Generation

### Strategy 1: The Game Design Document (GDD) Approach

Start with a structured GDD before writing any code. The GDD should contain:

```markdown
# Game: [Name]
## Core Mechanic
[One sentence describing the main gameplay loop]

## Controls
- Arrow keys / WASD: Movement
- Space: Jump/Action
- E: Interact

## Visual Style
- 16x16 or 8x8 pixel sprites
- [N] colors max palette
- Top-down / Side-scrolling perspective

## Game Objects
- Player: moves, jumps, has HP
- Enemy: follows player, deals damage on contact
- Collectible: grants score boost
- Goal: triggered to win

## Win/Lose Conditions
- Win: Reach the goal
- Lose: HP reaches 0

## Data / State
- Score: integer
- HP: integer (starts at 3)
- Level: string (current map name)
```

### Strategy 2: The "Build One Thing at a Time" Prompt Pattern

Break the game into isolated builds. Each build prompt follows this structure:

```
BUILD N: [Feature Name]
CONTEXT: Previous builds have [X, Y, Z working].
NEW: Add [specific feature].
SPECS: [Technical requirements like file names, function signatures]
TEST: Run game and verify [expected behavior].
```

### Strategy 3: Structured Prompt Template for AI Agents

```
## Task
Create a pixel [genre] game using [framework].

## Requirements
1. [Functional requirement]
2. [Visual requirement]
3. [Control requirement]

## Files
- main.py - entry point and game loop
- player.py - player class
- enemies.py - enemy behaviors
- assets/ - sprite/tile data

## Constraints
- Use only [N] colors
- Screen size: 256x256
- Frame rate: 60 FPS

## Testing
- Run the game after each change
- Verify [key behaviors]
```

### Strategy 4: Iterative "Vibe Coding" Workflow

As described by GameMaker's Claude Code integration and the broader "vibe coding" trend:

1. **Describe** what you want to build in natural language
2. **Generate** the initial implementation
3. **Test** immediately (run the game)
4. **Identify** bugs or missing features
5. **Fix** via natural language description of the issue
6. **Enhance** by describing the next feature
7. **Ship** when the game is functional

### Strategy 5: Reference Examples

Include links to working examples in your prompts. Pyxel has excellent built-in examples:
- 02_jump_game.py - Simple jumping mechanic
- 10_platformer.py - Full platformer with scrolling
- Image Editor and Sound Editor built into the engine

For AI agents (Claude, Cursor, Copilot), placing a CLAUDE.md or similar file in the project root dramatically improves output quality. Pyxel's CLAUDE.md is the gold standard example.

---

## 3. Iterative Development with AI Agents (Test, Fix, Enhance Cycle)

### The Correct Workflow

```
┌─────────────────┐
│ 1. SPECIFY      │  Write a clear, focused requirement
└────────┬────────┘
         ▼
┌─────────────────┐
│ 2. GENERATE     │  AI produces initial code
└────────┬────────┘
         ▼
┌─────────────────┐
│ 3. TEST         │  RUN THE GAME. Check for:
│                 │  - Compilation errors
│                 │  - Runtime crashes
│                 │  - Visual correctness
│                 │  - Input response
└────────┬────────┘
         ▼
┌─────────────────┐     YES
│ 4. PASSES?      │ ─────────► Next feature
└────────┬────────┘
         │ NO
         ▼
┌─────────────────┐
│ 5. DESCRIBE BUG │  Tell AI what went wrong
│    → FIX        │  (in natural language)
└────────┬────────┘
         ▼
    (back to TEST)
```

### Best Practices

| Practice | Why |
|----------|-----|
| **Test after every change** | AI often introduces regressions; detect immediately |
| **One feature at a time** | Multi-feature prompts produce confusing, buggy code |
| **Use source control** | Commit working versions; roll back broken AI changes |
| **Keep assets simple** | Use procedural/primitive graphics before integrating art |
| **Pin the framework version** | AI may mix APIs from different versions |
| **Set file size limits** | Large files confuse AI; split into modules early |
| **Include a test harness** | A simple `if __name__ == "__main__"` block for instant testing |

### Common AI Failure Modes in Game Dev

| Failure | Cause | Fix |
|---------|-------|-----|
| Unused imports/variables | AI adds boilerplate it doesn't use | Explicitly state "no unused code" |
| Magic numbers | AI hardcodes values | Request constants at top of file |
| Missing edge cases | AI covers happy path only | Describe edge cases explicitly |
| API hallucination | AI invents framework methods | Reference the actual API docs |
| Scope creep | AI adds features not requested | Be strict in requirements |

---

## 4. Pixel Art Asset Generation Approaches

### AI-Generated Sprites & Tiles

| Tool | Type | Best For | Pixel Art Quality |
|------|------|----------|-------------------|
| **Stable Diffusion** (with pixel art LoRA/checkpoint) | Open-source | Generating sprite sheets, tilesets, backgrounds | High (with right model) |
| **DALL-E 3** | Commercial | Concept art, character designs | Medium (hard to get pixel-level precision) |
| **Midjourney** | Commercial | Mood boards, backgrounds, UI mockups | Medium |
| **Aseprite AI plugins** | Commercial | In-editor AI generation for sprites | High (pixel-perfect editing) |
| **Pixel Art Generator** (various web tools) | Free/Web | Quick sprites, icons, tiles | Medium |
| **Pyxel Editor** (built-in) | Free/Open | Draw sprites directly in code editor | Manual but precise |

### Best Approach: Hybrid AI + Manual

1. **Generate concepts** with Stable Diffusion or Midjourney
2. **Clean up** in Aseprite or Pyxel Editor
3. **Tile** using the game engine's tilemap system
4. **Animate** sprite frames using Aseprite's timeline or Pyxel's animation support

### In-Code Procedural Assets (AI-Friendly)

The most reliable approach for AI-generated pixel games is to **define assets in code**:

```python
# Example: Pyxel tilemap data embedded in code
tilemap = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 1, 1, 0],
    [0, 1, 1, 0, 0, 1, 1, 0],
    [0, 0, 0, 2, 2, 0, 0, 0],
    [3, 3, 3, 3, 3, 3, 3, 3],
]
# 0=air, 1=wall, 2=door, 3=ground
```

```python
# Pyxel: drawing sprites programmatically
pyxel.cls(0)
pyxel.rect(10, 10, 20, 20, 8)    # Draw player as simple rect
pyxel.text(5, 5, "SCORE: 0", 7)   # Simple text HUD
```

### Recommended Asset Pipeline

```
1. AI generates sprite sheet (PNG, 16x16 or 32x32 grid)
2. Load into game as Image Bank (Pyxel) or Sprite Sheet (Phaser/Godot)
3. Define tilemap data in JSON or arrays
4. AI generates code that reads tilemap and renders tiles
5. Test and iterate on tile placement
```

For Pyxel specifically, the built-in **Image Editor** and **Tilemap Editor** allow editing assets directly in the development environment, avoiding the need for external art tools entirely. The Pyxel Studio web version (pyxelstudio.net) offers the same functionality in-browser.

---

## 5. Source URLs

- **Pyxel GitHub**: https://github.com/kitao/pyxel
- **Pyxel Studio (Web IDE)**: https://www.pyxelstudio.net/
- **GameMaker + Claude Code Integration**: https://www.gamedeveloper.com/production/gamemaker-incorporates-claude-code-to-enable-ai-assisted-workflows
- **Godot Engine**: https://docs.godotengine.org/
- **GitHub Topics - Pixel Games**: https://github.com/topics/pixel-game
- **Pyxel CLAUDE.md** (AI coding policy example): https://github.com/kitao/pyxel/blob/main/CLAUDE.md

---

## 6. Key Takeaways

1. **Pyxel is the #1 recommendation** for AI-generated pixel games: Python-based, retro constraints keep scope manageable, has explicit AI coding policies (CLAUDE.md), and includes built-in editors for all asset types.

2. **Structured requirements (GDD-style prompts)** dramatically improve AI output quality. Give the AI a spec document before asking for code.

3. **Iterate in tight loops**: Generate a small piece → test → fix → enhance. Never ask for an entire game at once.

4. **Define assets in code** rather than relying on AI to generate image files. AI is much better at writing arrays/tilemaps than creating correct PNG files. Use the game engine's built-in drawing primitives as a fallback.

5. **GameMaker's Claude Code CLI** (announced April 2026) signals a major trend: game engines are starting to bake AI agent support directly into their toolchains. Expect more engines to follow suit.

6. **Avoid complex engines** (Unity, Unreal) for AI game generation. The AI struggles with their component systems, editor dependencies, and multi-file project structures. Simple frameworks produce more reliable results.

7. **Pin your framework version** in requirements. AI models often hallucinate APIs from future/past versions; specifying the exact version (`pyxel==2.9.3`) improves correctness.

8. **Use CLAUDE.md or AGENTS.md files** in your project root to document coding conventions, project structure, and rules for the AI to follow. Pyxel's own CLAUDE.md is the best reference implementation.
