# Workflow Patterns for LLM-Based Game Development

> Research compiled: 2026-05-01
> Sources: Anthropic, Prompt Engineering Guide (DAIR.AI), 12-Factor Agents (HumanLayer)

---

## 1. Foundational Workflow Patterns (Anthropic)

Source: https://www.anthropic.com/research/building-effective-agents

Anthropic identifies 6 core patterns used in production agentic systems. These apply directly to game development with code agents:

### 1.1 Prompt Chaining
Decompose a task into sequential steps where each LLM call processes the output of the previous one. Add programmatic "gates" at intermediate steps.

**Game dev example:**
1. Generate game design doc → 2. Check for completeness (gate) → 3. Generate code structure → 4. Implement mechanics → 5. Generate asset specs

**When to use:** Tasks that cleanly decompose into fixed subtasks. Trades latency for accuracy.

### 1.2 Routing
Classify input and direct to specialized followup tasks. Enables separation of concerns.

**Game dev example:** Route "add enemy AI" to combat subsystem agent, "fix rendering" to graphics agent, "balance stats" to game design agent.

### 1.3 Parallelization (Sectioning & Voting)
- **Sectioning:** Break into independent subtasks run in parallel (e.g., generate player movement code AND enemy AI code simultaneously).
- **Voting:** Run same task multiple times for diverse outputs (e.g., generate 3 art direction proposals and pick best).

### 1.4 Orchestrator-Workers
A central LLM dynamically breaks down tasks, delegates to worker LLMs, and synthesizes results. Key difference from parallelization: subtasks aren't pre-defined.

**Game dev use case:** An orchestrator agent receives "build a platformer game" → dynamically decides: create physics engine, sprite renderer, level loader, input handler → delegates each to a worker → synthesizes into working game.

### 1.5 Evaluator-Optimizer
One LLM generates, another evaluates and provides feedback in a loop.

**Game dev use case:** Code agent writes game feature → review agent checks for bugs, performance, style compliance → loop until passing → human approval gate.

### 1.6 Autonomous Agents
LLMs dynamically direct their own processes and tool usage in a loop. Best for open-ended problems where steps can't be predicted.

**Game dev use case:** "Create a fun RPG battle system" with no further specification — agent iteratively designs, codes, tests, and refines.

### Key Principles from Anthropic
1. **Start simple** — optimize single LLM calls with retrieval/in-context examples first
2. **Add complexity only when it demonstrably improves outcomes**
3. **Prioritize transparency** — explicitly show agent's planning steps
4. **Design ACI (Agent-Computer Interface)** as carefully as HCI
5. **Use frameworks sparingly** — they obscure prompts/responses and make debugging harder

---

## 2. Spec Templates & Prompt Engineering for Code Agents

Source: https://www.promptingguide.ai/applications/coding

### 2.1 System Prompt Structure
A system prompt for a code agent should define:
- **Role** — "You are a game development code assistant..."
- **Language/framework** — "Your language of choice is Python with Pygame."
- **Output format** — "Generate complete, runnable code blocks."
- **Constraints** — "Keep the game under 500 lines. Use only standard library."

### 2.2 Comment-Driven Development
Generate code from structured comments:
```
"""
1. Create a player class with position, velocity, health
2. Create an enemy class that patrols between waypoints
3. Implement collision detection between player and enemies
4. Add a simple HUD showing health and score
"""
```

### 2.3 Spec-First Prompting Pattern
Best practice: write the spec as structured requirements, then ask the agent to implement:

```
## Game Specification
- Genre: Platformer
- Mechanics: Jump, double-jump, collect coins, avoid spikes
- Screen: 800x600, side-scrolling camera
- Assets: Rectangle-based graphics (programmatic, no external files)
- Scoring: 10 points per coin, display at top-left
- Win condition: Collect all 30 coins
- Lose condition: Hit 3 spikes (lives system)
```

### 2.4 Structured Input/Output Delimiters
Use XML or markdown delimiters to separate instructions from data:
```
<system_context>
You are building a web game using HTML5 Canvas + JavaScript.
All code must be self-contained in a single HTML file.
</system_context>

<user_request>
Add a boss enemy that appears after collecting 10 coins.
</user_request>

<existing_code>
[provide relevant existing code context]
</existing_code>
```

---

## 3. Context Engineering for Game Dev Agents

Source: https://www.promptingguide.ai/agents/context-engineering

### 3.1 The Layered Context Architecture
1. **System Layer** — Core agent identity and capabilities
2. **Task Layer** — Specific instructions for the current development task
3. **Tool Layer** — Descriptions and usage guidelines for available tools
4. **Memory Layer** — Relevant historical context (e.g., what was built in previous iterations)

### 3.2 Eliminate Ambiguity
**Bad:** "Make the game look better."
**Good:**
```
Visual requirements:
1. Background color: gradient from #1a1a2e to #16213e
2. Player sprite: 32x32 blue square with 2px white border
3. Enemy sprites: 32x32 red circles
4. Font: 16px monospace, white color for UI text
5. Particle effects on coin collection: 8 yellow sparks, 300ms duration
```

### 3.3 Make Expectations Explicit
- Required vs. optional features
- Quality standards (e.g., "must run at 60fps")
- Output format (e.g., "single HTML file, no external dependencies")
- Decision-making criteria (e.g., "if performance drops below 30fps, reduce particle count")

### 3.4 Error Handling in Specs
```
ERROR HANDLING:
- If a file write fails, retry once with a different path
- If code doesn't compile, capture the error and fix the issue
- If the game crashes on load, add console.error logging and retry
- Never delete existing code without confirming first
```

---

## 4. The 12-Factor Agents Framework

Source: https://github.com/humanlayer/12-factor-agents

Key factors most relevant to game development:

### Factor 2: Own Your Prompts
Store prompts in version control (e.g., `CLAUDE.md`, `AGENTS.md`, `.cursorrules`). Treat them as code.

### Factor 3: Own Your Context Window
- Pre-fetch all context the agent might need
- Keep context focused — don't dump entire codebase
- Use a `spec.md` or design doc as the primary context source

### Factor 8: Own Your Control Flow
Don't let the LLM decide everything. Use deterministic code for:
- File I/O operations
- Running tests
- Game loop structure
- Build/deploy pipelines
Use LLMs for creative/design decisions within those guardrails.

### Factor 10: Small, Focused Agents
Instead of one agent that does everything, use specialized agents:
- **Design Agent:** Creates game design docs, mechanics descriptions
- **Code Agent:** Implements features from specs
- **Art Agent:** Generates shader code, CSS, SVG assets
- **Test Agent:** Writes and runs tests, finds bugs

### Factor 12: Stateless Reducer Pattern
Treat each agent interaction as: `state + action -> new state`
- Pass current game state (codebase snapshot + design doc) as input
- Agent produces changes (diff) as output
- Deterministic code applies the changes

---

## 5. Agent-Computer Interface (ACI) Design

Source: https://www.anthropic.com/research/building-effective-agents (Appendix 2)

### 5.1 Tool Design Principles
- Give the model enough tokens to "think" before writing
- Keep format close to what the model saw during training
- Avoid formatting overhead (e.g., exact line counts for diffs)
- Use absolute file paths (agents lose track of relative paths)
- **Poka-yoke** tools — make it hard to make mistakes

### 5.2 ACI for Game Development
Example tool definitions for a game dev code agent:
```
Tool: edit_game_file
  - file_path: str (absolute path)
  - content: str (complete new file content)
  - description: "Replace the entire contents of a game source file"

Tool: run_game
  - description: "Launch the game and capture any runtime errors"

Tool: check_rendering
  - description: "Take a screenshot and verify visual output"
```

---

## 6. Iterative Development Pattern for Games

### 6.1 The Spec → Code → Test → Review Loop
1. **Write/update spec** (human or design agent)
2. **Implement** (code agent reads spec + existing codebase)
3. **Run** (deterministic — launch game, check for errors)
4. **Review** (evaluator agent checks quality, completeness)
5. **Fix** (loop back to step 2 if issues found)
6. **Accept** (human approval gate)

### 6.2 Spec Template for AI Game Development
```
# Game: [Title]

## Core Mechanics
- [movement, combat, scoring, etc.]

## Technical Constraints
- Platform: [web/HTML5/Pygame/etc.]
- Dependencies: [none/allowed/listed]
- Performance target: [60fps/30fps]
- File structure: [single file / modular]

## Visual Style
- Color palette: [hex codes or description]
- Resolution: [width x height]
- Asset approach: [programmatic/shader-based/external]
- UI layout: [HUD elements, menus]

## Game Loop
1. [Initialize state]
2. [Handle input]
3. [Update logic]
4. [Render frame]
5. [Check win/lose conditions]

## Feature Checklist (priority order)
- [ ] P1: Core movement and controls
- [ ] P1: Basic collision detection
- [ ] P2: Enemy AI
- [ ] P2: Scoring system
- [ ] P3: Sound effects
- [ ] P3: Menu screen
- [ ] P4: Particle effects
- [ ] P4: Save/load progress

## State Management
- Global state object structure
- How data flows between systems
- Persistence requirements

## Edge Cases to Handle
- Window resize
- Tab loses focus (pause)
- Very fast/slow frame rates
- Empty/corrupted save data
```

---

## 7. Recommended Prompting Techniques for Game Code

Source: https://www.promptingguide.ai/techniques

| Technique | Application to Game Dev |
|---|---|
| **Chain-of-Thought** | "Think step by step about the game architecture before writing code" |
| **Few-Shot** | Provide 1-2 examples of the desired code style/pattern |
| **Meta-Prompting** | "Generate a plan first, then implement each step" |
| **Self-Consistency** | Generate 3 implementations, vote on best approach |
| **Reflexion** | Agent critiques own code, then fixes issues |
| **Program-Aided (PAL)** | Use code execution as a reasoning step (run the game to verify) |

---

## Summary: Key Takeaways

1. **Start with a written spec** — structured requirements yield dramatically better results than vague requests
2. **Use prompt chaining + evaluator-optimizer** — break game dev into stages with review gates between them
3. **Own your context** — store prompts in `AGENTS.md`/`CLAUDE.md` alongside code
4. **Small focused agents** over one giant agent — separate design, code, and review concerns
5. **ACI matters** — design tool interfaces as carefully as UI
6. **Deterministic guardrails** — LLM does creative work; deterministic code handles file ops, tests, deploys
7. **Iterate via Refine Loop** — spec → implement → run → review → fix → accept
8. **Be extremely specific** — eliminate ambiguity in visual specs, file structure, tech constraints
