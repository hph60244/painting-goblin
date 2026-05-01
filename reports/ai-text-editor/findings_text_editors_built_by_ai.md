# Findings: Text Editor Projects Built by AI

## 1. Anthropic Claude - Text Editor Tool (Agent Tool)

Anthropic provides a built-in **Text Editor tool** as part of the Claude API for building agentic coding applications. This tool gives AI agents the ability to read, write, and edit files programmatically — effectively acting as a text editor within an agent loop.

- **Source:** Anthropic Claude API Documentation (text-editor tool for agents)
- **Key detail:** The tool enables agents to perform file read/write operations, view file contents, and make targeted edits — a foundational building block for AI-built text editors and coding agents.

---

## 2. Anthropic Autonomous Coding Agent Quickstart

Repository: `anthropics/claude-quickstarts` (16.4k stars)

This is a **two-agent pattern** (initializer + coding agent) that builds complete applications autonomously over multiple sessions. Key features:

- **Initializer Agent:** Reads an `app_spec.txt`, generates a `feature_list.json` with test cases, sets up project structure, and initializes git.
- **Coding Agent:** Implements features one by one, marking them as passing in the feature list.
- Progress is persisted via `feature_list.json` and git commits between sessions.
- Includes a **defense-in-depth security model** with OS-level sandboxing, filesystem restrictions, and a bash command allowlist.

> The agent can build full applications including web-based editors, with each coding iteration taking 5-15 minutes.

- **Source:** https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding

---

## 3. Anthropic "Building Effective Agents" Cookbook

Repository: `anthropics/claude-cookbooks` (41.9k stars)

Reference implementation for the "Building Effective Agents" research blog post. Includes patterns applicable to building text editors with AI:

- **Prompt Chaining** - Sequential tool calls for incremental editing
- **Routing** - Classify input and route to specialized handlers
- **Orchestrator-Subagents** - Delegate subtasks (e.g., syntax highlighting, auto-complete) to sub-agents
- **Evaluator-Optimizer** - Iterative improvement loop for generated editor code

- **Source:** https://github.com/anthropics/claude-cookbooks/tree/main/patterns/agents

---

## 4. GitHub Copilot (AI in VS Code / Editor)

GitHub Copilot is the most widely adopted AI developer tool, with millions of users and tens of thousands of business customers. It provides:

- **Inline code suggestions** - AI-generated completions as you type
- **Agent mode** in VS Code - autonomous task execution including file editing
- **Copilot Edits** - multi-file editing across projects
- Support for leading editors: VS Code, JetBrains, Neovim, Visual Studio, Xcode, Eclipse, and Zed

> "Developers who use GitHub Copilot report up to 75% higher satisfaction with their jobs... and are up to 55% more productive at writing code." — GitHub Copilot product page

- **Source:** https://github.com/features/copilot

---

## 5. Cursor - AI-First Code Editor

Cursor (by Anysphere, Inc.) is an AI-native code editor built from the ground up for AI-assisted development. Key capabilities:

- **Agent Composer 2** - Autonomous agents that can plan, search, and build features end-to-end
- **Cloud Agents** - AI agents that run in parallel, building, testing, and demoing features autonomously
- **Tab** - Specialized autocomplete model ("Magically accurate autocomplete")
- **Codebase indexing** - Full understanding of project context at any scale
- Supports multiple LLMs: GPT-5, Claude Opus 4.6, Gemini 3 Pro, Grok Code

> "The best LLM applications have an autonomy slider: you control how much independence to give the AI. In Cursor, you can do Tab completion, Cmd+K for targeted edits, or you can let it rip with the full autonomy agentic version." — Andrej Karpathy

> "Cursor quickly grew from hundreds to thousands of extremely enthusiastic Stripe employees." — Patrick Collison, Stripe CEO

- **Source:** https://www.cursor.com/

---

## 6. Lovable (formerly GPT Engineer) - AI App Builder

Lovable (raised $330M Series B) is an AI platform that builds full-stack applications from natural language prompts. Relevant for text editor building:

- **Agent Mode** - autonomously plans and builds features
- **Visual Edits** - Figma-like visual editing of generated apps
- **Supabase Integration** - backend generation for data-persistent apps
- Built with React, TypeScript, Tailwind CSS component libraries

> "Lovable has reached $100M ARR and enables non-technical users to build production-ready applications including rich text interfaces." — Lovable blog

- **Source:** https://www.lovable.dev/blog

---

## Summary Table

| Project | Type | AI Role | Key Framework | Stars/Users |
|---------|------|---------|---------------|-------------|
| Anthropic Text Editor Tool | Agent API tool | Read/write/edit files | Claude API | N/A (built-in) |
| Anthropic Autonomous Coding Agent | Reference app | Builds full apps from spec | Claude Agent SDK | 16.4k stars |
| Anthropic Agent Cookbook | Patterns/recipes | Agent orchestration patterns | Claude API | 41.9k stars |
| GitHub Copilot | IDE extension | AI pair programmer | VS Code API | Millions of users |
| Cursor | Standalone editor | AI-native IDE | VS Code fork | Millions of users |
| Lovable | Web platform | Full-stack AI app generation | React/TypeScript | $100M ARR |

## Key Takeaways

1. **AI agents can build text editors autonomously** — Anthropic's autonomous coding agent demonstrates AI building complete applications including rich UIs.
2. **The dominant architecture** is an agent loop with file read/write tools, orchestration patterns, and iterative refinement (evaluator-optimizer).
3. **AI-first editors (Cursor) and AI-augmented editors (VS Code + Copilot)** represent different points on the spectrum — Cursor bakes AI into every interaction, while Copilot augments a traditional editor.
4. **Security sandboxing** is a critical concern — Anthropic's autonomous agent uses an OS-level sandbox, filesystem restrictions, and command allowlists.
5. **Multiple LLMs** are being used for editor-building tasks — Claude, GPT-4/5, Gemini, and specialized fine-tuned models (Cursor's Tab model).
