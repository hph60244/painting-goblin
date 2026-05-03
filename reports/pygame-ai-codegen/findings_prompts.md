# Prompt Engineering Best Practices for AI Code Agents Generating Pygame Games

**Research Date: 2026-05-03**

---

## Sources Consulted

1. **Anthropic Prompting Best Practices** - https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-prompting-best-practices
2. **Anthropic Prompt Engineering Overview** - https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
3. **Claude Code Overview** - https://code.claude.com/docs/en/overview
4. **GitHub Copilot Features** - https://github.com/features/copilot
5. **Simon Willison: Gemini 2 + Pygame Experiment** - https://simonwillison.net/2024/Dec/19/gemini-2-pygame/

---

## Key Findings

### 1. System Prompt Design for Code Generation Agents

#### Role Assignment (Critical)
- **Best practice**: Give the AI a clear role in the system prompt. A single sentence makes a measurable difference.
- Example: `"You are a senior Python game developer specializing in Pygame. You write complete, runnable games with proper game loops, event handling, and sprite management."`

#### Be Clear and Direct
- Ambiguous prompts produce vague code. The "golden rule": show your prompt to a colleague with minimal context -- if they'd be confused, the AI will be too.
- **For Pygame**: Instead of "Make a game", use: "Create a complete, runnable Pygame game with a player sprite that moves with WASD, enemies that spawn from the right edge, a score counter, and collision detection."

#### Use XML Tags for Structure
- Wrap instructions in `<instructions>`, context in `<context>`, examples in `<examples>`.
- This prevents the model from mixing up specifications vs. instructions.
- Example template for Pygame generation:
```xml
<context>
The user wants a Pygame game with the following requirements.
</context>

<specification>
- Window size: 800x600
- Player: rectangle sprite, arrow key movement
- Enemies: circles falling from top
- Scoring: +10 per enemy dodged, -1 per hit (3 lives)
- Assets: use pygame.draw shapes only (no external assets)
</specification>

<constraints>
- Must be a single .py file
- Must run without errors when executing `python game.py`
- Use pygame.Rect for collision detection
- Game over screen with restart option
</constraints>
```

### 2. Prompt Patterns for Generating Working Pygame Games

#### The "Single Runnable File" Pattern
- **Key insight**: AI models produce more reliable results when constrained to a single file for simple games. Multiple files introduce import/resolution errors.
- **Prompt addition**: "Write the entire game as a single Python file called game.py that can be run with `python game.py`. Include all imports, asset creation, game loop, and entry point."

#### The "Structured Game Loop" Pattern
- Most reliable structure to specify in prompts:
```
1. Constants/configuration (screen size, colors, FPS)
2. Asset initialization (pygame.draw shapes, fonts)
3. Game state classes (Player, Enemy, Projectile, etc.)
4. Game loop:
   a. Event handling (quit, key presses)
   b. Update logic (movement, collisions, spawning)
   c. Draw (background, sprites, UI)
   d. Clock tick
5. Entry point guard (if __name__ == "__main__")
```

#### The "Explicit Dependencies" Pattern
- **Issue**: AI models often assume libraries are installed or use incorrect import paths.
- **Prompt addition**: "Use only pygame and Python standard library (random, math, sys). Do not import any third-party libraries beyond pygame."
- Also specify Pygame version constraints if needed.

#### The "Test-Driven Generation" Pattern (from Claude Code best practices)
- Have the AI write tests first, then implement the game.
- Example: "Before writing the game, write a test file that verifies: (1) the window initializes at the correct resolution, (2) the player moves correctly in all 4 directions, (3) collision detection returns True when sprites overlap."
- Anthropic reports this leads to better long-term iteration quality.

### 3. Effort and Thinking Configuration for Code Generation

#### Claude Opus-Specific Settings
- **Effort level**: Use `xhigh` (extra high) for coding and agentic use cases -- this is Anthropic's recommended default.
- **Max tokens**: Set large output token budget (64k tokens recommended) when running at xhigh/max effort so the model has room to think and act.
- **Adaptive thinking**: Use `thinking: {type: "adaptive"}` for multi-step tool use and complex coding tasks.

#### Mitigating Overthinking
- Adding this to system prompt helps prevent analysis paralysis: "When implementing a game, choose an architecture and commit to it. Avoid revisiting decisions unless you encounter a bug. If weighing two approaches (e.g., sprite groups vs. manual lists), pick one and proceed."

### 4. Claude Code Best Practices for Game Projects

#### CLAUDE.md / Project Memory
- Claude Code reads `CLAUDE.md` from the project root at the start of every session. Use this to persist:
  - Pygame version constraints
  - Preferred game architecture patterns
  - Testing/run commands
  - Coding conventions (type hints, docstrings, etc.)
- Claude also builds auto-memory as it works, saving build commands and debugging insights across sessions.

#### Multi-Context Window Workflows
- For complex games spanning multiple sessions:
  1. First context window: set up framework (project structure, main loop, basic sprites)
  2. Use a `progress.txt` or `tests.json` to persist state between sessions
  3. Have the AI create setup scripts (`init.sh` or `setup.py`) to avoid re-work
  4. Review `progress.txt` and git logs when starting fresh sessions

#### Subagent Orchestration
- Claude Code can spawn subagents for parallel work. For game dev, this is useful for:
  - Reading multiple reference files simultaneously
  - Writing sprite classes in parallel
  - Generating test data while implementing core logic
- **Prompt**: "Spawn multiple subagents in the same turn when fanning out across independent game modules."

### 5. Prompt Engineering Techniques from Anthropic Research

#### Be Explicit About Action vs. Suggestion
- **Less effective**: "Can you suggest a game architecture?"
- **More effective**: "Implement the full game. Write all files needed for a working Pygame application."

#### Provide the "Why" Behind Instructions
- Instead of "Never use sleep() in the game loop", try:
- "The game loop must never use time.sleep() because it blocks the pygame event queue and makes the window unresponsive. Use pygame.time.Clock.tick(FPS) instead."

#### Use 3-5 Examples for Few-Shot Prompting
- When defining output format (e.g., a specific sprite class pattern), provide 3-5 diverse examples wrapped in `<example>` tags.

#### Quote Extraction for Long Documents
- If providing a large game design document, ask the model to quote relevant sections before implementing: "Find quotes from the game design doc relevant to the core mechanics. Place these in <quotes> tags. Then implement based on those quotes."

#### Self-Check Prompt
- "Before finishing, verify your game runs without errors by checking: (1) all imports are valid, (2) all referenced variables are defined, (3) the game loop terminates on window close, (4) there are no infinite loops."

### 6. GitHub Copilot-Specific Notes

- Copilot supports custom instructions for tailoring code generation behavior.
- In agent mode, Copilot can be assigned tasks like "Create a complete Pygame project with the following structure..."
- Copilot Pro+ now supports Claude Opus 4.7 and other models -- allowing choice of model for game generation.
- Multi-model approach: use faster models (GPT-5 mini, Haiku) for boilerplate, premium models (Claude Opus) for complex game logic.

### 7. Structural Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Solution |
|---|---|---|
| "Make me a game like [vague reference]" | Too ambiguous, generates generic/broken code | Specify exact mechanics, controls, win/lose conditions |
| Asking for multiplayer/networking without specifying transport | AI picks arbitrary networking approach that doesn't work | Specify "single-player only" or "local 2-player on same keyboard" |
| No error handling instructions | AI may skip try/except on pygame.init() | Explicitly say "Include error handling for pygame initialization failures" |
| Vague asset requirements | AI may try to load image files that don't exist | Constrain to "Use pygame.draw for all graphics; no external asset files required" |
| Not specifying frame rate | Generated game may run at unbounded FPS | Always include "Use pygame.time.Clock to cap at 60 FPS" |
| Not specifying screen resolution | Window may be tiny or fullscreen unexpectedly | Always specify: "Window size: 800x600 pixels" |

### 8. Specific Prompt Template for Pygame Generation

Based on all findings, here is a composed best-practice prompt template:

````
You are a senior Python game developer specializing in Pygame.

<task>
Create a complete, runnable Pygame game based on the specification below.
</task>

<spec>
- Game title: [NAME]
- Window: [WxH] pixels, title set, 60 FPS cap
- Player: [describe shape, color, controls, speed]
- Enemies/obstacles: [describe spawn pattern, movement, behavior]
- Scoring: [how points are earned/lost]
- Win/lose condition: [game over criteria]
- UI: [score display, lives, menus]
</spec>

<constraints>
- Single .py file: game.py
- Only imports: pygame, sys, random, math
- Use pygame.draw for all graphics (no image files)
- Use pygame.Rect for collision detection
- Game loop structure: events -> update -> draw -> clock.tick(60)
- Entry point guard: if __name__ == "__main__"
- Include game over screen showing final score, with R to restart, Q to quit
- Comment any non-obvious game mechanic decisions
</constraints>

<code_quality>
- Use pygame.sprite.Group for managing multiple sprites
- Keep the game loop clean (one function per phase if helpful)
- Use constants at top of file for all tunable values (speed, spawn rate, colors)
</code_quality>

Before finishing, verify: (1) all imports resolve, (2) no undefined variables, (3) window close button works, (4) no blocking calls in the game loop.
````

### 9. Iteration Workflow (Post-Generation)

Once the AI produces initial code, iterate using these patterns:

1. **Bug-fix prompt**: "The game crashes on startup with error: [paste error]. Read game.py, trace the root cause, and fix it."
2. **Feature-add prompt**: "Add [feature] to the existing game. Do not break existing functionality. Preserve the current game loop structure."
3. **Refactor prompt**: "Refactor game.py to use pygame.sprite.Sprite subclasses for all game objects. Keep the behavior identical."
4. **Performance prompt**: "The game slows down when [N] sprites are on screen. Profile and optimize the update/draw phases."

### 10. Key Takeaways

- **Be extremely specific** about controls, mechanics, and constraints. AI models interpret prompts literally (especially Claude Opus 4.7).
- **Constrain to single-file generation** for first iteration; refactor into modules only after the core game works.
- **Always specify pygame.draw** for graphics unless you provide actual asset files.
- **Always specify FPS capping** (60 FPS) to avoid unbounded loops.
- **Use XML tags** in system prompts to separate instructions from specifications from constraints.
- **Set effort to xhigh** and token budget to 64k for Claude Opus when generating complex games.
- **Persist state between sessions** using CLAUDE.md, progress.txt, and git for multi-session game projects.
- **Verify generated code manually** -- AI games often have subtle bugs in collision detection, event handling, and game-over transitions.

---

*End of report.*
