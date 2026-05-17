# AI-Generated Games: Case Studies & Research Findings

**Date:** 2026-05-01
**Researcher:** AI Code Agent

---

## 1. GitHub Repositories: AI-Generated / LLM-Powered Games

### Notable Repos

| Repo | Stars | Description |
|------|-------|-------------|
| [Glade-tool/glade-mcp-unity](https://github.com/Glade-tool/glade-mcp-unity) | 73 | Connects MCP-compatible AI clients (Claude Code, Cursor) to Unity Editor. 222+ granular tools + full Unity-aware system prompt for AI-assisted game dev. |
| [cosmoart/quiz-game](https://github.com/cosmoart/quiz-game) | 88 | Quiz/trivia game with AI-generated questions, built with Tailwind + Cohere API in NextJS. |
| [ejones/llama-journey](https://github.com/ejones/llama-journey) | 110 | Experimental adventure game with AI-generated content using LLMs. |
| [SpicyMarinara/rpg-companion-sillytavern](https://github.com/SpicyMarinara/rpg-companion-sillytavern) | 240 | RPG Companion extension for SillyTavern - tracks characters, quests, inventory with AI-generated content. |
| [michaelmov/ascii-tetris](https://github.com/michaelmov/ascii-tetris) | 2 | ASCII Tetris built primarily as an exercise in AI-assisted development. |
| [Minoxds/prompt-to-puzzle](https://github.com/Minoxds/prompt-to-puzzle) | 1 | "Spot the Difference" games created from text prompts using AI-driven image generation. |
| [weavejul/GPTMazeGame](https://github.com/weavejul/GPTMazeGame) | 1 | Proof-of-concept 2D maze game using LLMs to generate dynamic dialogue (2020). |

### Key Finding
GitHub search for "AI generated game" returns ~4,100 repos. Most are small hobby projects. The `ai-generated-game` GitHub topic page is empty (no repos have tagged it). Few repos document the full prompt-to-game pipeline end-to-end.

---

## 2. Platforms & Tools for AI Game Generation

### GitHub Spark (Sep 2025)
- **URL:** https://github.com/features/spark
- **What it is:** AI-powered platform for building full-stack intelligent apps from natural language descriptions.
- **Relevance:** Can build simple games/prototypes by describing them in plain language. Supports TypeScript/React, one-click deployment.
- **Quote from site:** "Whether you're a seasoned developer or just getting started, Spark lets you create full-stack applications with built-in AI, using natural language, visual tools, or code."
- **Pricing:** Included in Copilot Pro+ ($39/user/month) and Copilot Enterprise.

### GameMaker + Claude Code (Apr 2026)
- **Source:** Game Developer (gamedeveloper.com)
- **What happened:** GameMaker officially incorporated Claude Code to enable AI-assisted workflows.
- **Significance:** Major game engine (GameMaker) building native AI code generation support into its toolchain.
- **Source URL:** https://www.gamedeveloper.com/production/gamemaker-incorporates-claude-code-to-enable-ai-assisted-workflows

### Glade MCP for Unity
- **What it is:** Open-source MCP (Model Context Protocol) server that connects Claude Code, Cursor, etc. directly to the Unity Editor.
- **Features:** 222+ granular tools, full Unity-aware system prompt, enables AI to manipulate Unity game objects, scenes, scripts.
- **Source:** https://github.com/Glade-tool/glade-mcp-unity

---

## 3. Case Studies: Full Process (Spec to Game)

### No Documented End-to-End Pipeline Found
The research did **not** find well-documented case studies where a requirements/specification document was fed to an AI and a complete, shippable game was produced. The current state appears to be:

- **Iterative prompting** is used, not spec-to-game.
- **Simple browser games** (Tetris, Pong, maze games, quiz games) are the most common AI-generated results.
- **No published mobile games** significantly created with AI code generation were identified.
- Most "AI-generated game" projects use AI for **content generation** (dialogue, quests, art) rather than **full code generation**.

### Limitations Observed
- AI struggles with complex game logic spanning multiple files/systems.
- Security issues are common (unauthenticated endpoints, XSS).
- Debugging AI-generated game code is time-consuming.
- Asset creation (art, sound, UI) remains a bottleneck even if code is AI-generated.

---

## 4. Failures & Challenges

### Hacker News Discussion (Feb 2025)
- **Source:** https://news.ycombinator.com/item?id=42914072 (on "Vibe Coding")
- **User macNchz (experienced AI coding user) reported:**
  > "In my (fairly extensive) experience with the current state of AI coding assistants, prompting for security is nowhere near sufficient for me to be comfortable putting a web app on the internet without reviewing the code carefully."
  > "Several instances where an AI assistant added sensitive API endpoints with no authentication whatsoever, updated API endpoints with methods that didn't follow my guidance on authorization, or created templates with brutal potential for XSS."

### Known Challenges
1. **Security vulnerabilities** - AI often ignores auth/security unless explicitly prompted.
2. **Scope creep** - Without a spec, AI-generated games grow uncontrollably.
3. **Asset pipeline** - Code generation doesn't solve asset creation (sprites, sounds, UI).
4. **Mobile-specific complexity** - Touch input, screen sizes, performance optimization, app store compliance are hard for AI.
5. **Debugging difficulty** - AI-generated code can have subtle bugs that are hard to trace.
6. **No published mobile games** - No examples found of AI-generated code powering a published app store game.

---

## 5. The "Vibe Coding" Phenomenon

- **Term coined by:** Andrej Karpathy (former head of AI at Tesla, OpenAI co-founder)
- **Definition:** Coding by fully giving in to the AI, describing what you want in natural language, and accepting the AI's code output without reading it.
- **Relevance to games:** Many hobbyist game projects are built this way, but results are typically small/simple.
- **Quote from Karpathy context:** "It's not really coding; it's vibe coding." (paraphrased from social media)

---

## 6. AI Tools Commonly Used for Game Generation

| Tool | Use Case | Notes |
|------|----------|-------|
| Claude Code / Claude Sonnet | Full game code generation, iterative development | Most popular for "vibe coding" games |
| GitHub Copilot | Inline code completion, agent mode | Limited ability to generate complete games standalone |
| Cursor | AI-native IDE with agent mode | Often used for iterative game building |
| GPT-4o / GPT-5 | Code generation, game design brainstorming | Used for prototypes, not full games |
| ChatGPT Canvas | Chat-based iterative game building | Simple browser games |
| Replit Agent | Full-stack app generation | Web-based games |
| Bolt.new / v0.dev | UI-first app generation | Simple game UIs |

---

## 7. Success Stories Summary

### What Works Well
- **Simple 2D browser games** (Tetris, Snake, Pong, maze games, quiz games)
- **AI-generated game content** (dialogue, quest text, procedural descriptions)
- **Rapid prototyping** of game mechanics
- **Single-file games** with minimal dependencies
- **HTML5 canvas games** (single HTML file)

### What Fails / Is Hard
- **Multi-scene mobile games** with navigation, save states, touch controls
- **Published app store games** (no known examples)
- **Games needing real-time networking** or multiplayer
- **Games with complex physics** or custom rendering
- **Production-quality asset pipelines**
- **Monetization, analytics, crash reporting** integration

---

## 8. Recommendations for This Project

1. **Start with a detailed spec document** - AI works better with structured requirements.
2. **Target simple 2D HTML5/Canvas games** for the first iteration - this is where AI excels.
3. **Use a single framework consistently** (e.g., Phaser.js with Claude Code) to keep context manageable.
4. **Iterate in small chunks** - prompt for one feature/mechanic at a time.
5. **Review ALL security-sensitive code** manually - especially auth, data storage, network calls.
6. **Plan for asset creation separately** - AI code generation ≠ AI art generation.
7. **Consider game engines with AI support** (Unity + Glade MCP, GameMaker + Claude Code).

---

## Sources

| Source | URL |
|--------|-----|
| GitHub - "ai generated game" search | https://github.com/search?q=ai+generated+game&type=repositories |
| GitHub Spark | https://github.com/features/spark |
| GameMaker + Claude Code | https://www.gamedeveloper.com/production/gamemaker-incorporates-claude-code-to-enable-ai-assisted-workflows |
| Glade MCP Unity | https://github.com/Glade-tool/glade-mcp-unity |
| Hacker News - Vibe Coding security discussion | https://news.ycombinator.com/item?id=42914072 |
| GitHub Copilot | https://github.com/features/copilot |
| Prompt-to-puzzle game | https://github.com/Minoxds/prompt-to-puzzle |
| GPT Maze Game | https://github.com/weavejul/GPTMazeGame |
