# Web Game Frameworks for AI Agent Rapid Prototyping

**Date:** 2026-04-27
**Purpose:** Evaluate four web-based game frameworks for suitability with AI coding agents (Claude, GPT, Copilot, etc.) for rapid game prototyping.

---

## 1. Phaser — The Industry Standard

### Stats
- **GitHub Stars:** 39.5k (phaserjs/phaser)
- **Forks:** 7.1k
- **Commits:** 20,892+
- **Latest Release:** v4.0.0 (Apr 10, 2026)
- **License:** MIT
- **CDN:** jsDelivr, cdnjs, unpkg

### AI Readiness
Phaser explicitly markets itself as "AI-ready." The GitHub README states: *"Phaser's API is well understood by every major frontier LLM... Models from Anthropic, OpenAI, Google, and others understand the Phaser API deeply and can generate game code, debug rendering issues, set up physics, and build scene structures out of the box."*

The repository includes a comprehensive `skills/` folder with AI agent skills covering every major subsystem (scenes, physics, input, animations, tilemaps, tweens, particles, cameras).

### Boilerplate & Setup
- **CDN-only (no build):** Yes. Works via `<script>` tag from jsDelivr or cdnjs.
- **Minimal boilerplate:** ~8 lines to start a game:
  ```html
  <script src="//cdn.jsdelivr.net/npm/phaser@4.0.0/dist/phaser.min.js"></script>
  <script>
  const game = new Phaser.Game({ type: Phaser.AUTO, width: 800, height: 600,
    scene: { create() { this.add.text(400, 300, 'Hello') } }
  });
  </script>
  ```
- **npm create template:** `npm create @phaserjs/game@latest` scaffolds with Vite + React/Vue/Svelte/Angular/SolidJS/Next.js.

### Documentation
- Full API docs at https://docs.phaser.io
- Over 2,000 code examples at https://phaser.io/examples
- 700+ tutorials on the Phaser website
- A free 500-page book "Phaser by Example"
- Legacy v3 docs at photonstorm.github.io/phaser3-docs (widely represented in LLM training data)
- **Community size:** Very large — active Discord (244k+ members), Discourse forum, Reddit.

### Best Suited For
2D platformers, RPGs, puzzle games, shoot-em-ups, card games, match-3, arcade games, and virtually any 2D game genre. The most versatile of the four.

### Sharing
Open the HTML file directly in a browser, or deploy to any static host (GitHub Pages, Netlify, Vercel). Also supports Discord Activities, YouTube Playables, and mobile wrappers.

### Verdict for AI Agents
**⭐⭐⭐⭐⭐ (Best Overall)**
- Huge training data presence across all major LLMs
- Official AI skills files in the repo
- Can run with zero build step via CDN
- Extremely well-documented with thousands of examples

---

## 2. Kaboom.js — Fun & Simple (But Unmaintained)

### Stats
- **GitHub Stars:** 2.7k (replit/kaboom)
- **Forks:** 230
- **Commits:** 1,689
- **Status:** **Archived** — repository archived by owner on Nov 12, 2024. Read-only.
- **License:** MIT
- **CDN:** unpkg, jsDelivr

### AI Readiness
The API is extremely simple and intuitive — component-based with a flat namespace. An LLM can easily generate correct Kaboom code because the API surface is small and consistent. However, since the project is no longer maintained, newer LLMs may not have recent training data for it.

### Boilerplate & Setup
- **CDN-only (no build):** Yes.
  ```html
  <script src="https://unpkg.com/kaboom@3000/dist/kaboom.js"></script>
  <script>
  kaboom()
  loadBean()
  const player = add([sprite("bean"), pos(120, 80), area(), body()])
  onKeyPress("space", () => player.jump())
  </script>
  ```
- **npm:** `npm install kaboom` (requires bundler like esbuild or webpack)
- **Scaffold:** `npm init kaboom mygame`

### Documentation
- Inline docs at kaboomjs.com with many examples on the same page
- Playground available at kaboomjs.com/play
- **Warning:** The website (kaboomjs.com) displayed a notice: *"Kaboom.js is no longer maintained."*
- Community fork exists: **KaPlay** (github.com/marklovers/kaplay)

### Best Suited For
Simple 2D games — platformers, collect-a-thons, arcade games, jam games, educational games. Good for prototyping but limited for complex/large games.

### Sharing
Open HTML file in browser, or deploy to static host. Originally designed for Replit's platform.

### Verdict for AI Agents
**⭐⭐⭐ (Risk: Unmaintained)**
- Simplest API of the bunch — lowest barrier to entry
- **CRITICAL WARNING:** No longer maintained by Replit. The community fork KaPlay is the successor.
- Smallest community and least training data
- Best for throwaway prototypes only

---

## 3. PixiJS — Rendering Powerhouse

### Stats
- **GitHub Stars:** 47k (pixijs/pixijs)
- **Forks:** 5k
- **Commits:** 8,683+
- **Latest Release:** v8.18.1 (Apr 14, 2026)
- **License:** MIT
- **CDN:** jsDelivr, unpkg

### AI Readiness
PixiJS has a dedicated AI page at https://pixijs.com/llms with:
- **llms.txt** — lightweight navigation index
- **llms-medium.txt** — guides and tutorials
- **llms-full.txt** — complete API reference in a single file
- **pixijs-skills** — official skill collection (25 focused skills across Application, Assets, Graphics, Filters, Mesh, Performance, etc.) compatible with 40+ AI agents

The README shows major brands using it: Adobe, Disney, Google, BBC, Lego, Marvel, Spotify, Steam, Ubisoft.

### Boilerplate & Setup
- **CDN-only (no build):** Yes, via ES module imports.
  ```html
  <script type="module">
  import { Application, Sprite, Assets } from 'https://cdn.jsdelivr.net/npm/pixi.js@8/+esm';
  const app = new Application();
  await app.init({ background: '#1099bb', resizeTo: window });
  document.body.appendChild(app.canvas);
  </script>
  ```
- **npm:** `npm install pixi.js`
- **Scaffold:** `npm create pixi.js@latest` (CLI tool)

### Documentation
- https://pixijs.com/8.x/guides — Getting Started, tutorials, examples
- https://pixijs.download/release/docs/index.html — Full API docs
- AI-optimized documentation at /llms
- Showcase page with many real-world examples

### Best Suited For
PixiJS is a **rendering engine**, not a full game engine. It lacks built-in physics, scene management, input handling, audio, etc. Best for:
- Custom rendering-heavy projects
- Data visualizations
- Interactive installations
- Games where you want full control and plan to add your own game logic/physics on top
- Projects using WebGL/WebGPU features

### Sharing
Open HTML in browser, deploy to any static host. Used by major brands in production.

### Verdict for AI Agents
**⭐⭐⭐⭐ (Best for custom rendering)**
- Most GitHub stars of any group (47k)
- Excellent AI support with official skills and llms.txt
- **NOT a game engine** — no physics, no built-in game loop, no scene management
- Requires more code to achieve what Phaser does in fewer lines
- Best when you need maximum rendering control

---

## 4. MelonJS — Lightweight Battery-Included Engine

### Stats
- **GitHub Stars:** 6.3k (melonjs/melonJS)
- **Forks:** 661
- **Commits:** 7,712+
- **Latest Release:** v19.1.0 (Apr 16, 2026)
- **License:** MIT
- **Bundle Size:** Under 100KB gzipped — zero dependencies
- **CDN:** jsDelivr

### AI Readiness
MelonJS has a smaller presence in LLM training data compared to Phaser or PixiJS due to its smaller community. The API follows Canvas2D patterns (`save`, `restore`, `translate`, `rotate`), which is familiar and predictable for LLMs. No official AI skills files exist.

### Boilerplate & Setup
- **CDN-only (no build):** Yes, via ES module.
  ```html
  <script type="module" src="https://cdn.jsdelivr.net/npm/melonjs/+esm"></script>
  <script type="module">
  import { Application, Text } from "https://cdn.jsdelivr.net/npm/melonjs/+esm";
  const app = new Application(800, 600, { parent: "screen", scale: "auto" });
  app.world.addChild(new Text(400, 300, { font: "Arial", size: 40, text: "Hello" }));
  </script>
  ```
- **npm:** `npm install melonjs`
- **Scaffold:** `npm create melonjs@latest my-game`

### Documentation
- https://melonjs.github.io/melonJS/ — API docs
- Beginner's tutorial on the site
- Examples: platformer, isometric RPG, whac-a-mole, 3D mesh, shader effects
- Wiki and FAQ on GitHub

### Best Suited For
2D platformers, isometric games, tilemap-based RPGs, games designed with the Tiled map editor. Particularly strong for:
- **Tiled map editor integration** (orthogonal, isometric, hexagonal maps)
- **Battery-included** — physics, audio, input, camera, UI, particles, tweens all built-in
- Small, dependency-free bundle (under 100KB gzipped)

### Features
- WebGL & Canvas2D renderer with automatic fallback
- Web Audio with 3D spatial sound
- SAT-based 2D physics
- Tiled map editor support up to v1.12
- Camera system with shake/fade/flash effects
- UI toolkit with drag-and-drop
- Custom shader effects (Flash, Outline, Glow, Dissolve, CRT, Hologram)
- 3D mesh rendering (OBJ/MTL)

### Sharing
Open HTML in browser, deploy to any static host.

### Verdict for AI Agents
**⭐⭐⭐⭐ (Best lightweight full engine)**
- Smallest bundle (under 100KB) — fastest page loads
- Full game engine with batteries included (like Phaser)
- Actively maintained (v19.1.0 released Apr 2026)
- Smaller community means less LLM training data — AI agents may produce less accurate code
- Best for small, focused 2D games (especially with Tiled maps)

---

## Comparison Summary

| Criteria | Phaser | Kaboom.js | PixiJS | MelonJS |
|---|---|---|---|---|
| **GitHub Stars** | 39.5k | 2.7k | 47k | 6.3k |
| **Maintained?** | Yes (v4.0.0, Apr 2026) | **No (Archived)** | Yes (v8.18.1, Apr 2026) | Yes (v19.1.0, Apr 2026) |
| **Full Game Engine?** | Yes | Yes | No (rendering only) | Yes |
| **No Build Step (CDN)?** | Yes | Yes | Yes (ESM) | Yes (ESM) |
| **AI Skills / llms.txt?** | Yes (skills/ folder) | No | Yes (skills + llms.txt) | No |
| **LLM Training Data** | Excellent (very high) | Low | Excellent (very high) | Moderate |
| **Bundle Size (gzip)** | 345 KB | ~200 KB | ~250 KB | <100 KB |
| **Boilerplate (lines)** | ~8 | ~5 | ~10 | ~8 |
| **Best For** | Any 2D game | Quick prototypes | Custom rendering | Tiled-based 2D games |

## Final Recommendation

For an **AI coding agent** doing rapid game prototyping:

1. **Phaser** — Best overall. Largest community, most training data, official AI skills, no-build CDN option, full game engine. The agent will produce the most correct code with the least prompting.
2. **PixiJS** — Best for rendering-heavy or non-game interactive projects. Excellent AI documentation support. Requires more game logic code to be written by the agent.
3. **MelonJS** — Best for small/focused games where bundle size matters. Full engine but less LLM training coverage.
4. **Kaboom.js** — Simplest API but **no longer maintained**. Only suitable for throwaway prototypes using the community fork (KaPlay).

### Source URLs
- Phaser GitHub: https://github.com/phaserjs/phaser
- Phaser Website: https://phaser.io
- Phaser Docs: https://docs.phaser.io
- PixiJS GitHub: https://github.com/pixijs/pixijs
- PixiJS Website: https://pixijs.com
- PixiJS AI Docs: https://pixijs.com/llms
- Kaboom.js GitHub: https://github.com/replit/kaboom (archived)
- Kaboom.js Website: https://kaboomjs.com
- KaPlay (community fork): https://github.com/marklovers/kaplay
- MelonJS GitHub: https://github.com/melonjs/melonJS
- MelonJS Website: https://melonjs.org
