# Research Findings: Tools, Frameworks, and Workflows for LLM-Powered Text Game Agents

> Compiled: 2026-05-16
> Research method: Web fetch from Wikipedia, GitHub, inklestudios.com, and industry publications

---

## 1. Dedicated Interactive Fiction / Text Game Engines

### Ink (inkle)
- **Type:** Open-source (MIT) narrative scripting language for interactive fiction
- **License:** MIT
- **GitHub:** https://github.com/inkle/ink (~4.8k stars)
- **Website:** https://www.inklestudios.com/ink/
- **Language:** C# (core engine); JavaScript port available as `inkjs`
- **Key features:**
  - Markup-first: "Text comes first, code and logic are inserted within"
  - Compiles to JSON for integration into any game engine
  - Designed as middleware — "a narrative engine designed to slot into a game engine"
  - Unity integration plugin: https://github.com/inkle/ink-unity-integration
  - Unreal integration (Inkpot): https://github.com/The-Chinese-Room/Inkpot
  - Includes `inklecate` command-line compiler
  - Inky editor: WYSIWYG with play-as-you-write
- **Notable games using Ink:** *80 Days* (2014), *Sorcery!* series, *Heaven's Vault*
- **API usage for C#:**
  ```csharp
  using Ink.Runtime;
  _story = new Story(sourceJsonString);
  while(_story.canContinue)
      Debug.Log(story.Continue());
  // Display story.currentChoices list, allow player to choose
  _story.ChooseChoiceIndex(0);
  ```
- **Source:** https://en.wikipedia.org/wiki/Ink_(scripting_language) (404 on fetch, data from GitHub README and inklestudios.com)

### Twine
- **Type:** Free open-source hypertext fiction / interactive fiction tool (GPL v3)
- **Website:** https://twinery.org
- **GitHub:** https://github.com/klembot/twinejs
- **Initial release:** 2009
- **Current version:** 2.9.0 (June 2024)
- **Written in:** TypeScript (v2.x), Python (v1.x)
- **Platforms:** Linux, macOS, Windows, Web application
- **Key features:**
  - Visual node-based editor (hypertext structure)
  - No programming required for basic use
  - Story formats: Harlowe (default), SugarCube, Snowman, Chapbook
  - Supports CSS and JavaScript for customization
  - Emphasizes "visual structure of hypertext"
- **Notable works:** *Depression Quest* (2013), *Queers in Love at the End of the World* (2013), *The Uncle Who Works for Nintendo* (2014), *You Are Jeff Bezos* (2018)
- **Used by:** Charlie Brooker for *Black Mirror: Bandersnatch*
- **Source:** https://en.wikipedia.org/wiki/Twine_(software)

### Inform 7
- **Type:** Programming language and design system for interactive fiction
- **Developer:** Graham Nelson (first released 1993; Inform 7 in 2006)
- **License:** Artistic License 2.0 (open source since 2022)
- **Website:** https://ganelson.github.io/inform-website/
- **Key features:**
  - Natural-language programming — source code reads like English prose
  - "The world is a room." — valid Inform 7 code
  - Compiles to Z-code (Z-machine) or Glulx virtual machines
  - Rule-based, declarative, domain-specific
  - Built-in IDE with interpreter, skein (branching test tree), and transcript
  - The Standard Rules library handles parsing and world model
- **Example:**
  ```inform7
  "Hello World"
  The world is a room.
  When play begins, say "Hello, world!"
  ```
- **Notable games:** *Curses* (1993), *Anchorhead* (1998), *Photopia* (1998), *Galatea* (2000)
- **Source:** https://en.wikipedia.org/wiki/Inform

### Ren'Py
- **Type:** Free open-source (MIT) visual novel engine
- **Website:** https://www.renpy.org/
- **GitHub:** https://github.com/renpy/renpy
- **Initial release:** 2004
- **Written in:** Python, Cython
- **Built on:** Pygame → SDL
- **Key features:**
  - Screenplay-like syntax for dialogue and branching
  - Supports inline Python for advanced logic
  - Animation and Translation Language (ATL) for in-engine animation
  - Screen Language for full UI customization
  - Export targets: Windows, macOS, Linux, Android, iOS, HTML5/WebAssembly
  - Built-in tutorial game
- **Notable games:** *Doki Doki Literature Club!* (2017), *Katawa Shoujo* (2012), *Long Live the Queen* (2012), *Slay the Princess* (2023)
- **Source:** https://en.wikipedia.org/wiki/Ren%27Py

### TADS (Text Adventure Development System)
- **Type:** Prototype-based domain-specific language for interactive fiction
- **Developer:** Michael J. Roberts (first released 1988)
- **Website:** https://www.tads.org/
- **Current version:** TADS 3.1.3 (May 2013)
- **Key features:**
  - Syntax based on C/Pascal (TADS 2), C++/Java-like (TADS 3)
  - Compiles to platform-independent VM story files
  - TADS 3 features: garbage collection, exceptions, UTF-8, strong typing
  - Multimedia TADS (1998): graphics, animation, sound
- **Source:** https://en.wikipedia.org/wiki/Text_Adventure_Development_System

---

## 2. General-Purpose Frameworks & Libraries for Python Text Games

### Pygame
- General-purpose Python game library (SDL wrapper)
- Ren'Py is built on top of it; suitable for custom text game engines
- http://www.pygame.org/

### Custom Python + LLM approach
- A common pattern emerging for AI-powered text games:
  - **Python** for game loop, state management, and CLI/web interface
  - **LLM API** (OpenAI, Anthropic Claude, local models via Ollama/LM Studio) for dynamic narrative generation
  - **LangChain / LlamaIndex** for prompt chaining, memory, and tool use
  - **JSON structured output** from LLM for game state transitions (e.g., `{ "action": "move", "direction": "north", "narration": "..." }`)
- Example project pattern: https://github.com/karthick965373/LLM-Text-Adventure-Game (404 on fetch — common community pattern)

---

## 3. Prompt Engineering Patterns for Text Game Generation

### Key Patterns Observed in the Field

**1. Structured Output Parsing**
- Use LLM JSON mode / function calling to emit structured game state
- Example system prompt fragment:
  ```
  You are a text adventure game engine. For each player action, respond with JSON:
  {
    "narration": "<prose description>",
    "state_changes": { "health": -5, "inventory": ["key"] },
    "available_actions": ["go north", "examine room", "talk to guard"]
  }
  ```

**2. World State Injection**
- Maintain a canonical world state outside the LLM context
- Inject relevant state into each prompt (current room, inventory, NPCs)
- Use retrieval-augmented generation (RAG) for lore/quest data

**3. Constraint Enforcement**
- Use system prompts to enforce game rules ("you cannot go east from here")
- Use chain-of-thought for puzzle solving ("think step by step about how to open the door")
- Apply few-shot examples of valid game interactions

**4. Narrative Consistency**
- Maintain a "story so far" buffer in context
- Use summarization when context windows fill
- Employ character cards (common in roleplay LLM applications)

**5. Multi-Agent Architectures**
- Game Master agent: generates narrative and reacts to player
- World Model agent: tracks game state, validates actions
- NPC agent(s): generate dialogue per character
- Evaluator agent: checks output for consistency/rule violations

---

## 4. LLM Agent Architectures for Game Building

### ReAct (Reason + Act) Pattern
- LLM reasons about the game state, then acts (generates text, updates state)
- Used in LangChain agents for text game loops

### Tool-Using Agents
- LLM calls tools: `move(direction)`, `examine(object)`, `inventory()`, `save()`
- Tools enforce game rules and provide structured feedback

### Reflection + Self-Correction
- LLM reflects on its own narrative output for consistency
- Critic agent reviews generated content before committing

### Memory Management
- Short-term: recent conversation/game context in window
- Long-term: vector database (Chroma, Pinecone) for NPC memories, quest states
- Episodic: per-session memory of player actions

---

## 5. Workflow: How an LLM Agent Can Build a Text Game

**Phase 1: Design**
- LLM generates game world, characters, items, quests from a high-level prompt
- Output structured as JSON/YAML game blueprint

**Phase 2: Implementation**
- Agent writes game code (Python + engine calls, Ink script, Inform 7, Twine HTML)
- Uses file operations and iterative refinement
- Can compile/test via shell commands

**Phase 3: Iteration**
- Agent plays the game, identifies bugs/lore gaps
- Feedback loop: "This door should be locked, not open" → regenerate code

**Phase 4: Deployment**
- Export to web (Twine HTML, Ink JSON + JS runtime, Ren'Py distributions)
- Static site or interactive web app

---

## 6. Key Takeaways

| Category | Best Options |
|---|---|
| **Scripted narrative (human-written, deterministic)** | Ink, Inform 7, TADS, Twine |
| **Visual novel / dialogue-heavy** | Ren'Py, Twine, Ink + Unity |
| **LLM-driven dynamic narrative (AI-generated)** | Custom Python + OpenAI/Claude API + LangChain |
| **Rapid prototyping / non-programmers** | Twine, Inky (Ink editor) |
| **Game engine integration** | Ink (Unity/Unreal), Ren'Py (standalone) |
| **Agent-built games** | Python + structured LLM output + iterative code generation |
| **Prompt engineering for games** | System prompts with JSON schemas, world state injection, few-shot constraints, multi-agent critics |

### Notable LLM + Text Game Projects / References
- "Using AI to generate text adventures in Python" — Game Developer (gamedeveloper.com)
- "Unity says its AI tech will soon be able to prompt full casual games into existence" — Game Developer, Feb 2026
- Ubisoft 'Teammates' experiment — generative AI narrative characters (Nov 2025)
- Community pattern: LLM-Text-Adventure-Game on GitHub (Python + GPT)

### Sources
- https://en.wikipedia.org/wiki/Interactive_fiction
- https://en.wikipedia.org/wiki/Twine_(software)
- https://en.wikipedia.org/wiki/Inform
- https://en.wikipedia.org/wiki/Ren%27Py
- https://en.wikipedia.org/wiki/Text_Adventure_Development_System
- https://github.com/inkle/ink
- https://www.inklestudios.com/ink/
- https://www.gamedeveloper.com/programming/using-ai-to-generate-text-adventures-in-python
