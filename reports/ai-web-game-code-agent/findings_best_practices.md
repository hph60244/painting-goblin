# Best Practices and Frameworks for AI Web Game Development

**Research Date:** 2026-05-01
**Subtopic:** Best practices, workflows, project structure, and testing strategies for using AI coding agents to create browser-based games.

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Iterative Prompting Workflows](#iterative-prompting-workflows)
3. [Testing Strategies for AI-Generated Games](#testing-strategies-for-ai-generated-games)
4. [Project Structure for AI-Generated Code](#project-structure-for-ai-generated-code)
5. [AI Coding Agent Tools & Frameworks](#ai-coding-agent-tools--frameworks)
6. [Agentic System Design Patterns](#agentic-system-design-patterns)
7. [Community Best Practices](#community-best-practices)
8. [Recommended Workflow for Web Game Development](#recommended-workflow-for-web-game-development)
9. [Source References](#source-references)

---

## Executive Summary

AI coding agents are transforming browser-based game development. The most successful implementations combine **simple, composable patterns** rather than complex frameworks (Anthropic, Dec 2024). Key findings:

- **Start simple** - optimize single LLM calls with retrieval and in-context examples before adding agentic complexity
- **Break game features into bite-sized steps** - one mechanic per prompt cycle
- **Use linting and auto-testing** to catch AI-generated code issues immediately
- **Maintain a clean project structure** so the AI agent understands context
- **Leverage git** as a safety net for experimentation

---

## Iterative Prompting Workflows

### The Bite-Sized Step Approach (Aider)

The Aider project (aider.chat) recommends breaking goals into small, independent steps:

1. **Plan first** - Use `/ask` mode to discuss architecture before editing code
2. **Add only relevant files** to the chat context - too much irrelevant code distracts LLMs
3. **Work one feature at a time** - complete one mechanic before moving to the next
4. **Drop completed files** from context with `/drop` as you go
5. **Use `/clear` to reset** when the agent gets stuck on a problem

### Prompt Chaining for Game Logic (Anthropic)

Complex game features should be decomposed into sequential steps:

- **Step 1:** Generate game design outline
- **Step 2:** Check outline against requirements (programmatic gate)
- **Step 3:** Generate core game loop logic
- **Step 4:** Generate rendering/assets
- **Step 5:** Generate input handling

Each LLM call processes the output of the previous one, with programmatic checks at each stage.

### Routing for Mixed Complexity

For games with varied features (e.g., simple UI vs. complex physics), use routing:
- Route simple rendering tasks to smaller, cost-efficient models
- Route complex game logic to more capable models
- Route bug fixes to models with strong debugging capabilities

### Evaluator-Optimizer Loop

Use an evaluation loop for game polish:
1. Generate game feature (e.g., collision detection)
2. Run an evaluator LLM to assess correctness
3. Feed evaluation back for refinement
4. Loop until quality threshold is met

---

## Testing Strategies for AI-Generated Games

### Automated Linting (Aider)

Aider provides built-in linters for most popular languages and will auto-lint every edit:

- **JavaScript/TypeScript:** ESLint
- **HTML/CSS:** stylelint, HTML validators
- **Auto-lint on edit** catches syntax errors immediately
- **Per-language linters** can be configured via `--lint "language: cmd"`
- **Auto-fix mode** runs code formatters as linters

### Automated Testing (Aider)

- Use `/test <test-command>` to run tests and share output with the AI
- Configure `--test-cmd` for auto-testing after every AI edit
- Use `--auto-test` to run the full test suite after each change
- For compiled languages, use test commands that also compile: `--test-cmd "npm run build && npm test"`

### Manual Run-Share Loop

- Use `/run` command to execute the game and share output with the AI agent
- Share error messages directly so the AI can fix them
- Share visual output for the AI to diagnose rendering issues

### Recommended Test Types for Web Games

| Test Type | Purpose | Tool |
|-----------|---------|------|
| Unit tests | Individual game mechanics (score, spawn, collision) | Vitest, Jest |
| Integration | Game loop, state management | Vitest |
| Visual/rendering | Canvas output, DOM state | Playwright, Puppeteer |
| Playthrough | Full game flow from start to end | Manual + Playwright |

---

## Project Structure for AI-Generated Code

### Recommended Structure

Based on community best practices for AI-assisted game development:

```
game-project/
├── src/
│   ├── core/           # Game loop, state machine, main entry
│   │   ├── Game.js
│   │   ├── Loop.js
│   │   └── State.js
│   ├── entities/       # Players, enemies, items
│   │   ├── Player.js
│   │   └── Enemy.js
│   ├── systems/        # Physics, collision, input, audio
│   │   ├── Physics.js
│   │   ├── Input.js
│   │   └── Audio.js
│   ├── rendering/      # Canvas/WebGL, sprites, UI
│   │   ├── Renderer.js
│   │   └── UI.js
│   └── utils/          # Math helpers, constants
│       ├── math.js
│       └── constants.js
├── tests/
│   ├── unit/
│   └── integration/
├── public/
│   └── assets/
├── index.html
├── package.json
├── .eslintrc.js
└── AGENTS.md           # Project conventions for AI agent
```

### Why This Structure Works with AI Agents

- **Separation of concerns** lets the AI focus on one file at a time
- **Single-responsibility files** reduce context needed per prompt
- **`AGENTS.md` or `CONVENTIONS.md`** file documents coding conventions the agent should follow (Aider conventions file feature)
- **Small, focused modules** prevent the AI from producing monolithic, tangled code

### Aider's Guidance on Files

- **Only add files that need changing** - too much irrelevant code confuses the LLM
- **Aider uses a repo map** to understand relationships between files without loading them all
- **For new files**: use `/add <file>` to create them explicitly
- **For bug fixes**: use `/run` to share the error output rather than describing it

---

## AI Coding Agent Tools & Frameworks

### Recommended Tools for Browser Game Development

| Tool | Type | Key Features | Best For |
|------|------|--------------|----------|
| **Claude Code (Anthropic)** | Terminal agent | Multi-file editing, tool use, codebase understanding | Complex game logic, architecture |
| **Cursor** | IDE agent | Composer, Tab autocomplete, codebase indexing, multi-model | Full-stack game development |
| **GitHub Copilot** | IDE + cloud agent | Agent mode, Copilot CLI, code review, third-party agent support | Iterative development, PR reviews |
| **Aider** | Terminal agent | Git integration, auto-lint, auto-test, repo map, model switching | Structured workflows, safety |
| **Gemini Code Assist** | IDE agent | Deep Google Cloud integration | Full-stack + cloud games |

### Key Differentiators

- **Cursor** offers an "autonomy slider" - from Tab completion to full agentic mode
- **Aider** provides best-in-class automated linting/testing integration
- **Claude Code** excels at understanding large codebases and multi-file edits
- **GitHub Copilot cloud agents** can work autonomously in the background

---

## Agentic System Design Patterns

Based on Anthropic's research (Dec 2024) on building effective agents:

### 1. Orchestrator-Workers Pattern

Best for complex game features spanning multiple files:
- **Orchestrator LLM** dynamically breaks down the task (e.g., "add jump mechanic")
- **Worker LLMs** implement individual pieces (physics, input, animation)
- Orchestrator synthesizes results

### 2. Parallelization Pattern

- **Sectioning:** Split game tasks into independent subtasks (e.g., renderer + input handler + audio system developed in parallel)
- **Voting:** Run the same prompt multiple times for diverse implementations, then pick the best

### 3. Agent Loop Pattern

1. Receive task from human
2. Plan approach
3. Execute tool calls (edit files, run tests)
4. Observe results
5. Iterate or ask for human feedback

### Core Principles (Anthropic)

1. **Maintain simplicity** in agent design
2. **Prioritize transparency** - show the agent's planning steps
3. **Carefully craft tool interfaces** - treat agent-computer interfaces (ACI) with as much care as human-computer interfaces (HCI)
4. **Use absolute file paths** - reduces agent errors
5. **Test tools thoroughly** - run example inputs in workbench to see what mistakes the model makes

---

## Community Best Practices

### From Aider Community

- **Switching models can unstick problems** - switch between GPT-4o and Sonnet when stuck
- **Use `/clear` to reset context** instead of fighting with confused context windows
- **Pair program with the AI** - code the next step yourself if the AI is stuck, then have it continue
- **Provide documentation URLs** - the AI can scrape and read docs you link
- **Use conventions files** to document standing instructions for the AI

### From Cursor Community

- **Use .cursorrules** to define project-specific behaviors for the agent
- **Leverage codebase indexing** so the AI understands your full project
- **Start with Tab for small edits** → **Cmd+K for targeted changes** → **Agent for full features**
- **Cloud agents can build and demo features autonomously** for you to review

### General Game Development Wisdom

- **Start with a playable prototype** before adding polish - AI excels at rapid prototyping
- **Keep the game loop simple**: `update()` → `render()` → `handleInput()`
- **Use vanilla HTML5 Canvas + JavaScript** for fastest AI iteration (no framework overhead)
- **Add TypeScript for type safety** - reduces AI-generated bugs
- **Commit frequently** so you can roll back bad AI generations

---

## Recommended Workflow for Web Game Development

### Phase 1: Prototype (Rapid)

1. Define the game concept in a prompt (1-2 sentences)
2. Use agent to generate `index.html` with inline JS canvas game
3. Open in browser and review
4. Iterate: "add WASD movement" → "add enemy spawning" → "add score counter"
5. Each iteration: 1 mechanic, review, commit

### Phase 2: Structure

1. Refactor into project structure (split files)
2. Add AGENTS.md with coding conventions
3. Set up linting (ESLint) and testing (Vitest)
4. Configure auto-lint in your AI coding agent

### Phase 3: Polish

1. Use evaluator-optimizer loops for:
   - Visual polish (particles, animations)
   - Game feel (tweaking physics values)
   - Performance optimization
2. Test edge cases with AI-generated test suites
3. Run playthrough tests

### Phase 4: Production

1. Code review AI-generated code
2. Add TypeScript types
3. Bundle and optimize (Vite, esbuild)
4. Deploy

---

## Source References

| Source | URL | Key Contribution |
|--------|-----|------------------|
| Anthropic - Building Effective Agents | https://www.anthropic.com/research/building-effective-agents | Agentic design patterns (orchestrator-workers, evaluator-optimizer, routing, prompt chaining) |
| Aider - Tips & Usage | https://aider.chat/docs/usage/tips.html | Iterative prompting, file management, unsticking strategies |
| Aider - Linting and Testing | https://aider.chat/docs/usage/lint-test.html | Auto-lint, auto-test, `/run` command for error sharing |
| Cursor - Product Features | https://www.cursor.com/features | Agent mode, codebase indexing, multi-model support |
| GitHub Copilot - Features | https://github.com/features/copilot | Cloud agents, code review, multi-LLM support |
| Cursor - AI Workflows | https://docs.cursor.com/context/ai-workflows | Agentic workflows, context management |
| Aider - Conventions Files | https://aider.chat/docs/usage/conventions.html | AGENTS.md / conventions for coding standards |

---

*Research compiled using web searches across AI coding agent documentation, Anthropic research publications, and community best practices resources.*
