# Research: Guides, Tutorials & Case Studies for Structuring Requirements Docs for AI Game Generation

> Compiled 2026-05-16. Sources: Anthropic, OpenAI, Cursor Docs, Aider Docs, GitHub Copilot.

---

## 1. Core Philosophy: Simplicity Over Complexity

**Source:** [Anthropic — "Building Effective Agents" (Dec 2024)](https://www.anthropic.com/engineering/building-effective-agents)

> "Over the past year, we've worked with dozens of teams building large language model (LLM) agents across industries. Consistently, the most successful implementations weren't using complex frameworks or specialized libraries. Instead, they were building with simple, composable patterns."

> "Success in the LLM space isn't about building the most sophisticated system. It's about building the *right* system for your needs. Start with simple prompts, optimize them with comprehensive evaluation, and add multi-step agentic systems only when simpler solutions fall short."

### Three core principles for agent design:
1. **Simplicity** in your agent's design.
2. **Transparency** by explicitly showing the agent's planning steps.
3. Carefully craft your **agent-computer interface (ACI)** through thorough tool documentation and testing.

---

## 2. Agent Workflow Patterns (Anthropic Taxonomy)

**Source:** [Anthropic — "Building Effective Agents"](https://www.anthropic.com/engineering/building-effective-agents)

| Pattern | Description | Best For |
|---|---|---|
| **Prompt Chaining** | Decompose task into sequential steps, each LLM call processes previous output | Tasks that decompose into fixed subtasks (e.g., outline → validate → write) |
| **Routing** | Classify input and direct to specialized follow-up | Separate handling for different categories (e.g., simple vs complex game features) |
| **Parallelization** | Run subtasks simultaneously, aggregate results | Independent concerns like guardrails + core response; or voting on code quality |
| **Orchestrator-Workers** | Central LLM dynamically breaks down tasks, delegates, synthesizes | Complex multi-file changes (especially relevant for game code generation across many files) |
| **Evaluator-Optimizer** | One LLM generates, another evaluates in a feedback loop | Iterative refinement when clear criteria exist (e.g., "does this game feel fun?") |
| **Autonomous Agent** | LLM directs its own process, tool use, and planning | Open-ended problems with unpredictable step counts |

**Key insight for game generation:** The evaluator-optimizer pattern is particularly relevant — you can have the agent generate game code, then play-test and iterate based on observed behavior.

---

## 3. Prompt Engineering Best Practices (OpenAI)

**Source:** [OpenAI — Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)

### Message Role Hierarchy:
- `developer` (system) messages = highest priority — "the rules and business logic, like a function definition"
- `user` messages = lower priority — "inputs and configuration, like arguments to a function"
- `assistant` messages = model's own prior responses

### Recommended structure for a developer message:
1. **Identity** — purpose, communication style, high-level goals
2. **Instructions** — rules, what to do, what never to do
3. **Examples** — input/output pairs
4. **Context** — reference data, placed near end of prompt

### Formatting tips:
- Use **Markdown headers** and **lists** to mark distinct sections
- Use **XML tags** (`<game_rules>...</game_rules>`) to delineate content boundaries
- "XML attributes can be used to define metadata about content in the prompt that can be referenced by your instructions"

---

## 4. Cursor Rules: Structuring Project Context for AI Agents

**Source:** [Cursor Docs — Rules for AI](https://docs.cursor.com/context/rules-for-ai)

Cursor supports two types of rules that serve as the "requirements document" for AI agents:

### Project Rules (`.cursor/rules/*.mdc`):
- Markdown-based files with YAML frontmatter
- Can target specific file patterns (e.g., `*.py`, `*.gd`)
- Can be set to "always apply" or auto-attached based on semantic matching

### Key features:
- **Glob-based file targeting** — rules can apply only to specific file types
- **Semantic rule matching** — rules auto-attach based on content similarity
- **Agent mode** — Cursor's agent can read files, run commands, and iterate autonomously

**Relevance for game dev:** You can write rules that define your game architecture, engine conventions, and code style — the agent reads these as its "requirements document."

---

## 5. Aider's Repository Map: Giving Agents Codebase Context

**Source:** [Aider Docs — Repository Map](https://aider.chat/docs/repomap.html)

> "Aider uses a concise map of your whole git repository that includes the most important classes and functions along with their types and call signatures. This helps aider understand the code it's editing and how it relates to the other parts of the codebase."

### How it works:
- Generates a compressed map of key symbols (classes, functions, types) per file
- Uses **graph ranking** to select the most relevant portions within token budget (~1k tokens default)
- Shows how critical lines of code are defined

### Why this matters for game gen:
> "The LLM can see classes, methods and function signatures from everywhere in the repo. This alone may give it enough context to solve many tasks."

**Practical example from Aider:** [Modify an open source 2048 game](https://aider.chat/examples/2048-game.html), [Build pong with aider and pygame](https://aider.chat/examples/pong.html)

---

## 6. GitHub Copilot: Multi-Agent and Custom Instructions

**Source:** [GitHub Copilot Features](https://github.com/features/copilot)

GitHub Copilot now supports:
- **Third-party agents** — assign tasks to Copilot, Claude, or OpenAI Codex agents
- **Custom instructions** — `.github/copilot-instructions.md` for repo-specific guidance
- **MCP server integration** for extending agent capabilities

### Key stat:
> "Developers who use GitHub Copilot report up to 75% higher satisfaction with their jobs than those who don't and are up to 55% more productive at writing code."

---

## 7. Aider's Example: Building Games with Prompting Patterns

**Source:** [Aider Examples — Pong with Pygame](https://aider.chat/examples/pong.html), [2048 Game Modification](https://aider.chat/examples/2048-game.html)

Aider's documented game-building examples demonstrate a key workflow:
1. **Start with a concrete spec** — "Create a pong game using pygame"
2. **Iterate in natural language** — add features, fix bugs conversationally
3. **Use /add to provide context** — point the agent to relevant files
4. **Git integration** — automatic commits for each change, allowing rollback

**Takeaway for requirements docs:** The most effective approach is a layered spec — start with a minimal viable game spec, then iteratively add features through follow-up prompts.

---

## 8. OpenAI Codex: AGENTS.md and Codex Rules

**Source:** [OpenAI Codex — AGENTS.md Guide](https://codex.best/guides/agents-md), [Codex Rules](https://codex.best/rules)

OpenAI Codex supports:
- **`AGENTS.md`** — a file that defines the agent's persona, goals, and operating procedures.
- **Codex Rules** — `.codex/rules/*.md` for scoped project conventions.
- **Subagents** — specialized agents for different tasks (e.g., one for game logic, one for UI).

### Example AGENTS.md structure:
```markdown
# Game Development Agent

You are an expert game developer. You write clean, modular code.
You use pygame. You prefer composition over inheritance.
You always create a requirements doc before coding.
```

---

## 9. Actionable Best Practices for Game Requirements Docs

Synthesized from all sources above:

### Do:
- **Write a layered spec**: MVP first, then expansion features as separate sections
- **Use structured formatting**: Markdown headers + XML tags for game rules, dialogue, and mechanics
- **Include concrete examples**: Show the agent what "fun" looks like via example play sessions
- **Set guardrails**: Define what tech stack, file structure, and patterns to use
- **Provide reference context**: Include snippets of your existing codebase conventions
- **Iterate conversationally**: Start broad, refine specifics through follow-up prompts
- **Use evaluator-optimizer loops**: Generate, test, critique, regenerate

### Avoid:
- **Over-specifying implementation details** — let the agent propose architecture
- **Skipping the MVP** — agents struggle with monolithic specs; build incrementally
- **Vague requirements** — "Make it fun" is useless without concrete criteria
- **Giving contradictory instructions** in different parts of the doc

### Recommended document structure:
```
# Game: [Title]
## Identity & Genre
## Tech Stack & Constraints
## Core MVP Mechanics (ordered by priority)
├── Combat/Fight system
├── Inventory
├── Dialogue
└── Saving/Loading
## Expansion Features (future iterations)
## Code Conventions & Architecture
## Example Play Session (expected input/output)
## Reference Files (links to existing code)
```

---

## Source URLs

| Source | URL |
|---|---|
| Anthropic — Building Effective Agents | https://www.anthropic.com/engineering/building-effective-agents |
| OpenAI — Prompt Engineering Guide | https://platform.openai.com/docs/guides/prompt-engineering |
| Cursor — Rules for AI | https://docs.cursor.com/context/rules-for-ai |
| Aider — Repository Map | https://aider.chat/docs/repomap.html |
| Aider — Pong Example | https://aider.chat/examples/pong.html |
| Aider — 2048 Example | https://aider.chat/examples/2048-game.html |
| GitHub Copilot | https://github.com/features/copilot |
| OpenAI Codex AGENTS.md | https://codex.best/guides/agents-md |
| OpenAI Codex Rules | https://codex.best/rules |
