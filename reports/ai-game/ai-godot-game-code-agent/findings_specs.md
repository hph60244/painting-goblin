# AI Game Generation from Spec/Design Documents: Research Findings

## Overview

This document captures research on approaches, frameworks, and examples where AI agents take a requirement document or design specification and produce a working game. Searches were conducted May 2026.

---

## 1. Direct Approaches: AI Agents Building Games from Specs

### 1.1 Vibe Coding 2D Games with Claude Code & Agent Skills

- **Source**: YouTube tutorial by Chong-U (AI Oriented Dev) — 90K+ views
- **URL**: `https://www.youtube.com/watch?v=84998D65CEEC071F54CC` (referenced in Bing results)
- **Description**: Full tutorial showing how to use Claude Code with agent skills to generate 2D games. Demonstrates the workflow of describing a game concept, having Claude Code create the full project structure, and iterating on it. This is the closest real-world example of an AI code agent building a complete game from a description/prompt.
- **Key takeaway**: Claude Code can generate functional 2D game projects when given a clear game concept prompt, using its agentic mode to plan, write, and iterate.

### 1.2 Gemini Code Assist: Requirements Document to Prototype

- **Source**: Google Cloud Blog
- **URL**: `https://cloud.google.com/blog/topics/developers-practitioners/from-requirements-to-prototype-with-gemini-code-assist`
- **Date**: April 23, 2025 (updated Dec 2025 — now superseded by Gemini CLI + MCP approach)
- **Description**: Google's documented workflow for going from a requirements document (Google Doc) to a working application prototype using Gemini Code Assist. The process:
  1. Place a requirements doc in Google Drive
  2. Use `@GoogleDocs` to find and extract requirements from within VS Code
  3. Prompt Gemini to generate complete project structure + code for all files
  4. Generate bash script to create the project
  5. Install deps and run
- **Example**: Weekend Ideas Application (Python/Flask/SQLite) generated from a functional spec doc
- **Key takeaway**: Iterative process — generate, run, identify gaps, prompt fixes, repeat. AI handles scaffolding + logic from natural-language spec.

### 1.3 Multi-Agent Game Generation (Augment Code / Intent)

- **Source**: Augment Code Blog
- **URL**: `https://www.augmentcode.com/guides/spec-driven-ai-code-generation-with-multi-agent-systems`
- **Date**: Sep 24, 2025
- **Description**: Spec-driven AI code generation using multi-agent architecture (Coordinator-Implementor-Verifier). While not game-specific, the pattern directly applies:
  - **Coordinator**: decomposes spec into tasks
  - **Implementors**: generate code in parallel (isolated git worktrees)
  - **Verifier**: validates output against spec
  - Uses OpenAPI/AsyncAPI as living specs that auto-update
- **Key takeaway**: Multi-agent architecture with spec validation is the most robust approach for ensuring generated code matches the design document.

---

## 2. Frameworks and Tools Enabling Spec-to-Game Generation

### 2.1 Claude Code (Anthropic)

- **Type**: Agentic CLI coding tool
- **Relevance**: Can generate complete game projects from natural language descriptions. Uses `CLAUDE.md` as a project context file that captures project overview, tech stack, and module structure. Supports skill plugins.
- **Source**: Multiple GitHub repos and documentation (claude-code-best, claude-code-guide)
- **Key URL**: `https://github.com/claude-code-best/claude-code`

### 2.2 Gemini Code Assist / Gemini CLI

- **Type**: AI coding assistant with Google Docs integration
- **Relevance**: Can read Google Docs (spec docs) directly, extract requirements, and generate full project code. Superseded by Gemini CLI workspace extension + MCP servers approach (Dec 2025).
- **Source**: `https://cloud.google.com/blog/topics/developers-practitioners/from-requirements-to-prototype-with-gemini-code-assist`

### 2.3 CrewAI

- **Type**: Multi-agent orchestration framework
- **Relevance**: Used for "Agentic PRD" projects — coordinating specialist agents to generate documentation and code from requirements. The pattern extends naturally to game generation.
- **Source**: `https://github.com/nanagajui/agentic_prd`
- **Related**: `https://arxiv.org/html/2409.00038v1` — Academic paper on AI-based multiagent approach for requirements elicitation.

### 2.4 Intent by Augment Code

- **Type**: Desktop workspace for agent orchestration
- **Relevance**: Coordinator-Implementor-Verifier architecture with Context Engine for cross-file awareness. Processes 400K+ files. Uses living specs as contracts.
- **Source**: `https://www.augmentcode.com/product/intent`

---

## 3. Key Patterns and Approaches

### 3.1 The "Spec-In, Game-Out" Pipeline

The general pattern observed across all approaches:

```
Design Doc / Spec (Google Doc, Markdown, PRD)
  → AI extracts requirements
  → AI generates project structure + all source files
  → AI creates build/run scripts
  → Human tests and identifies gaps
  → AI iteratively fixes issues
  → Working game prototype
```

### 3.2 Single-Agent vs Multi-Agent

| Approach | Pros | Cons |
|---|---|---|
| **Single Agent** (Claude Code, Gemini) | Simpler setup, works for smaller games | Context limits, no parallel work, harder to validate against spec |
| **Multi-Agent** (CrewAI, Intent) | Spec validation, parallel generation, larger scope | More complex setup, higher cost |

### 3.3 Iterative Refinement is Required

Every documented approach emphasizes that AI rarely generates a perfect game in one shot. The reliable pattern is: generate → test → identify gaps → prompt fix → repeat.

### 3.4 Spec Quality Matters

The more structured and detailed the design document:
- Structured specs (with data models, API contracts, acceptance criteria) produce more accurate output
- Plain narrative descriptions require more iterations
- The "living spec" pattern (Intent) where specs auto-update with implementation is the state of the art

---

## 4. Academic Research

- **"AI based Multiagent Approach for Requirements Elicitation and Refinement"** (arXiv 2409.00038v1, Aug 2024)
  - Multi-agent system that deploys AI models as agents to generate user stories from initial requirements
  - Assesses and improves quality, then prioritizes using selected techniques
  - URL: `https://arxiv.org/html/2409.00038v1`

- **Agentic AI Performance Research** (ResearchGate, 2025)
  - 34.2% reduction in task completion time when agentic systems replace traditional AI approaches
  - URL: Referenced by Augment Code guide

---

## 5. Directly Relevant Game Examples

1. **2D Games via Claude Code** — Various YouTubers have demonstrated Claude Code generating complete 2D games (platformers, puzzles) from prompts. The "Vibe Coding 2D Games with Claude Code & Agent Skills" video (90K views) is the most prominent.

2. **Weekend Ideas App via Gemini Code Assist** — While not a game, this demonstrates the complete spec-to-prototype pipeline that would apply to game generation.

3. **No documented examples exist yet for Godot-specific game generation from a full design spec document.** This represents an opportunity.

---

## 6. Gaps and Opportunities

- **No established "Game Design Document → Godot Project" pipeline** exists as an off-the-shelf tool or well-documented workflow
- Most examples are 2D web/mobile games; 3D game generation from spec is largely unexplored
- No framework currently understands GDScript/Godot scene files (.tscn) natively as a spec target
- Multi-agent coordination for game-specific tasks (art generation, level design, balancing) is an open area

---

## 7. Summary of Source URLs

| Source | URL |
|---|---|
| Google Cloud - Gemini Code Assist spec-to-prototype | `https://cloud.google.com/blog/topics/developers-practitioners/from-requirements-to-prototype-with-gemini-code-assist` |
| Augment Code - Spec-Driven AI Code Generation | `https://www.augmentcode.com/guides/spec-driven-ai-code-generation-with-multi-agent-systems` |
| Agentic PRD (crewAI) | `https://github.com/nanagajui/agentic_prd` |
| arXiv Multiagent Requirements Paper | `https://arxiv.org/html/2409.00038v1` |
| Augment Intent Product | `https://www.augmentcode.com/product/intent` |
| Claude Code Guide | `https://github.com/claude-code-best/claude-code` |
| Spec-Driven Dev with Gemini CLI (updated) | `https://medium.com/google-cloud/spec-driven-development-with-gemini-cli-dfb4b88d4880` |
