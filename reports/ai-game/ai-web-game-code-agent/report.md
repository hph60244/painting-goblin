# AI Code Agent Web Game Development — Research Report

## Summary

This report consolidates findings on using AI code agents to create web games from requirement documents. Research covered three subtopics: existing tools/examples, workflow patterns, and best practices.

---

## 1. Key Tools & Platforms

| Tool | Type | Game Dev Strength |
|------|------|-------------------|
| **Claude 3.5 Sonnet + Artifacts** | Chat + live preview | Instant single-file HTML games; live rendering in-chat |
| **Claude Code** | Terminal agent | Multi-file editing, autonomous planning, codebase understanding |
| **Cursor** | AI-first IDE | Agent mode builds full apps from PRDs; multi-model support |
| **GitHub Copilot Agent mode** | IDE + cloud agents | Autonomous code generation, PR creation, code review |
| **bolt.new** | Browser-based agent | No-install, full-stack in-browser game dev |
| **v0 (Vercel)** | Prompt-to-app | Template category for games; one-click deploy |
| **Replit Agent** | Browser IDE agent | Zero-setup full-stack game building |
| **Rosebud AI** | Specialized game AI | Vibe-coding 2D/3D WebGL games from descriptions |
| **Aider** | Terminal agent | Best-in-class auto-lint/auto-test, conventions files, git safety |

## 2. Documented Case Studies

1. **Ben's Bites — Side-Scrolling Game w/ Claude** ([source](https://catalog.bensbites.com/tutorial/create-an-html5-web-game-with-claude)): Generated SVG character + background, then prompted Claude to inline everything into a single HTML5 side-scrolling game. Iterative refinement.

2. **AccessAgent.ai — Space Shooter & Memory Card Game** ([source](https://accessagent.ai/learn/build-game-with-ai)): Agent reads a guide, generates self-contained HTML game, zips and deploys — all in one conversation.

3. **NVIDIA Research — "Plunderwater" Game Jam** ([source](https://research.nvidia.com/publication/2025-06_generative-ai-game-jam-case-study-october-2024)): Academic case study (CVPR 2025) of building a complete game in days using commercial GenAI tools.

4. **Claude Pinball Game** ([source](https://www.howtouselinux.com/post/how-to-use-claude-to-write-an-h5-game-a-step-by-step-guide)): Step-by-step guide — brainstorm → HTML5 Canvas → physics → input → scoring → polish.

5. **Rosebud AI — Desert Dunes Explorer** ([source](https://lab.rosebud.ai/blog/webgl-game-example-created-with-ai)): Full WebGL 3D game with procedural terrain, dynamic lighting, particles — vibe-coded from description.

6. **OpenGame — Academic Framework** ([source](https://arxiv.org/abs/2604.18394)): First open-source agentic framework for end-to-end web game creation; 150 diverse game prompts benchmarked.

## 3. Workflow Patterns That Work

### The Iterative Spec → Code → Test → Review Loop
1. Write/update structured spec (requirement document)
2. Code agent implements from spec
3. Run game and check for errors
4. Review agent evaluates quality
5. Fix and loop
6. Human approves

### Key Patterns (from Anthropic's "Building Effective Agents"):
- **Prompt Chaining**: Break game dev into sequential stages with gates
- **Orchestrator-Workers**: One LLM delegates subtasks (physics, rendering, input) to workers
- **Evaluator-Optimizer**: Generate → evaluate → refine loop for polish
- **Small Focused Agents**: Separate design, code, art, and test agents

## 4. Best Practices

1. **Start with a structured spec** — structured requirements yield dramatically better results than vague prompts. Use a spec template (see findings_workflows.md for full template).

2. **One mechanic per iteration** — break game features into bite-sized steps; complete one mechanic before moving to the next.

3. **Use auto-lint + auto-test** — catch AI-generated bugs immediately (Aider's `--auto-test`, ESLint).

4. **Single-file prototyping → refactor** — start with one `.html` file for rapid iteration, then split into structured project.

5. **Keep files small and focused** — single-responsibility modules work best with AI agents.

6. **AGENTS.md / conventions file** — document coding conventions the agent should follow.

7. **Frequent git commits** — safety net for experimentation; enables rollback of bad AI generations.

8. **Be extremely specific** — eliminate ambiguity in visual specs, file structure, tech constraints.

## 5. Recommended Approach

```
Phase 1: Prototype
  Write 1-2 sentence game concept → Agent generates single-file HTML game → Review → Iterate

Phase 2: Structure
  Refactor into modules → Write AGENTS.md → Set up linting/testing → Configure auto-lint

Phase 3: Polish
  Evaluator-optimizer loops for visuals/feel → AI-generated test suites → Playthrough tests

Phase 4: Production
  Code review → TypeScript → Bundle (Vite) → Deploy
```

## 6. Source URLs

- https://www.anthropic.com/news/claude-3-5-sonnet
- https://catalog.bensbites.com/tutorial/create-an-html5-web-game-with-claude
- https://accessagent.ai/learn/build-game-with-ai
- https://research.nvidia.com/publication/2025-06_generative-ai-game-jam-case-study-october-2024
- https://www.howtouselinux.com/post/how-to-use-claude-to-write-an-h5-game-a-step-by-step-guide
- https://lab.rosebud.ai/blog/webgl-game-example-created-with-ai
- https://arxiv.org/abs/2604.18394
- https://www.anthropic.com/research/building-effective-agents
- https://www.promptingguide.ai/applications/coding
- https://github.com/humanlayer/12-factor-agents
- https://aider.chat/docs/usage/tips.html
- https://aider.chat/docs/usage/lint-test.html
- https://cursor.com
- https://bolt.new
- https://v0.dev
