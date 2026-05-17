# AI Coding Agents Generating Text-Based Adventure / Interactive Fiction Games

## Research Findings

---

## 1. Google Developers Blog: "Build a Text-Based Adventure Game with Gemma 2"

- **URL:** https://developers.googleblog.com/build-a-text-based-adventure-game-with-gemma-2/
- **Date:** August 14, 2024
- **Author:** Ju-yeong Ji (Sr. Technical Consultant Gen AI - AI Studio, Google)

### Key Facts
- Uses instruction-tuned **Gemma 2** (2B/9B/27B) to create a text adventure game
- Game features a "Storyteller" AI companion guiding the player through an escape-the-island narrative
- Full Python game code available on GitHub: https://github.com/bebechien/gemma/tree/main/escape
- Supports local execution via Keras/Kaggle or cloud deployment on Vertex AI
- Implements a stage-based game loop with modular stage classes

### Architecture
- `GemmaBot` wrapper class for interacting with the model
- `IStage` interface for defining game stages (intro, gate, etc.)
- Separate "admin bot" judges end-of-game conditions
- Each stage can have its own system prompt defining the Storyteller's role

### Notable Quote
> "You can apply the same structure to craft diverse games with themes ranging from steampunk to fantasy."

---

## 2. "Building an AI-Powered Text Adventure with Google Gemini" (pratikIT95)

- **URL:** https://pratikit95.github.io/llm-text-adventure/
- **Repos:**
  - Backend API: https://github.com/pratikIT95/text-game-llm-api
  - Frontend UI: https://github.com/pratikIT95/text-game-llm-ui

### Key Facts
- Full-stack text adventure: **Spring Boot** (backend) + **Angular/Angular Material** (frontend) + **Google Gemini API**
- Murder mystery theme set in Colonial India
- Uses Gemini system instructions to define game lore, character roles, and output format (JSON)
- Players are randomly assigned a famous literary detective (Sherlock Holmes, Byomkesh Bakshi, Feluda, Hercule Poirot)
- Three-act structure: introduction, investigation, resolution
- Maximum 20 prompts to prevent infinite loops
- Session tracking via UUID in browser sessionStorage, backend uses `ConcurrentHashMap`

### Notable System Instruction Snippet
> "You are a text adventure game and this is the lore - a murder mystery detective story in early 20th Century, Colonial India. You randomly assign a detective character... Your responses should be in pure JSON format with the following fields - storyText, choices (list of 3), isEnding (whether the story has ended), without any markdown tags."

---

## 3. DSPy Tutorial: "Building a Creative Text-Based AI Game"

- **URL:** https://dspy.ai/tutorials/ai_text_game/
- **Framework:** DSPy (Stanford NLP open-source framework)

### Key Facts
- Uses **DSPy** modular programming with **GPT-4o-mini** for narrative generation
- Dynamic story generation with branching narratives
- AI-powered character interactions and dialogue
- Adaptive gameplay responding to player choices
- Inventory and character progression systems (leveling, skill points)
- Save/load game state functionality (JSON serialization)
- Rich console UI using `rich` and `typer` Python libraries

### Architecture
- `GameAI(dspy.Module)` with three sub-modules:
  - `StoryGenerator` - generates scene descriptions, available actions, NPCs, items
  - `DialogueGenerator` - generates NPC responses, mood changes, quest offers
  - `ActionResolver` - resolves player actions, determines success/failure, stat changes
- Player skills: strength, intelligence, charisma, stealth
- Three-tier boundary system: Always / Ask First / Never

### Engine Components
- `GameEngine` class manages game state, save/load
- `Player` dataclass with health, level, experience, inventory, skills
- `GameContext` tracks visited locations, NPCs met, completed quests, game flags

---

## 4. AddyOsmani.com: "How to Write a Good Spec for AI Agents"

- **URL:** https://addyosmani.com/blog/good-spec/
- **Date:** January 13, 2026
- **Author:** Addy Osmani (Software Engineer at Google)

### Key Facts
- Comprehensive guide on **spec-driven development** for AI coding agents
- References **Claude Code**'s Plan Mode (Shift+Tab), **GitHub Copilot**, and **Gemini CLI**
- Cites analysis of **2,500+ agent configuration files** by GitHub
- Promotes **spec-driven development** where "specs become the shared source of truth... living, executable artifacts that evolve with the project"
- References GitHub Spec Kit: https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
- Cites Simon Willison's "vibe engineering" and "house of cards code" concepts

### Six Core Areas of Effective Specs
1. **Commands** - full commands with flags (`npm test`, `pytest -v`)
2. **Testing** - framework, file locations, coverage expectations
3. **Project structure** - explicit directory layout
4. **Code style** - real code snippets over paragraphs
5. **Git workflow** - branch naming, commit message format
6. **Boundaries** - three-tier: Always / Ask first / Never

### Key Quote
> "I've heard a lot about writing good specs for AI agents, but haven't found a solid framework yet... Simply throwing a massive spec at an AI agent doesn't work - context window limits and the model's 'attention budget' get in the way."

### Four-Phase Gated Workflow (from GitHub Spec Kit)
1. **Specify** - high-level description → detailed spec (user journeys)
2. **Plan** - tech stack + constraints → technical plan
3. **Tasks** - spec + plan → small reviewable chunks
4. **Implement** - one task at a time with focused reviews

---

## 5. Medium: "How to Write PRDs for AI Coding Agents"

- **URL:** https://medium.com/@haberlah/how-to-write-prds-for-ai-coding-agents-d60d72efb797
- **Date:** January 12, 2026

### Key Facts
- Focuses on adapting Product Requirements Documents (PRDs) for AI coding agents
- Emphasizes that **non-goals become even more critical** in AI agent specifications
- AI cannot infer scope boundaries from omission (unlike human readers)
- Advocates explicit "what NOT to do" sections in addition to standard PRD content

### Notable Quote
> "Non-goals become even more critical in AI coding agent specifications. Traditional PRDs often implied scope boundaries through what they omitted. AI cannot infer from omission."

---

## 6. Ganileni/Nomad: AI Agent That Plays Text Adventures

- **URL:** https://github.com/ganileni/Nomad
- **Repo:** github.com/ganileni/Nomad

### Key Facts
- An **AI agent** that autonomously plays text-based adventure games (currently Colossal Cave Adventure)
- Multi-model support: OpenAI, Anthropic, Google
- Tool-based AI interaction using OpenAI function calling
- Maintains conversation summarization for long gameplay sessions
- Session persistence (save/resume)
- YAML-based configuration with environment variable support
- Includes AGENTS.md files at every package level for AI context
- Demonstrates that "smaller models can be observed getting stuck in loops, particularly around challenging areas"

### Architecture
- **Games Layer** - standardized game interface
- **Models Layer** - abstraction over AI providers
- **Agents Layer** - game-playing logic with tool-based interactions
- **Utils Layer** - configuration, logging, error handling

---

## 7. Stanford CS224n: "Learning Strategic Play with Language Agents in Text-Adventure Games"

- **URL:** https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1244/final-projects/MirandaLinLiNicBecker.pdf

### Key Facts
- Academic project using LLMs to power autonomous language agents in text-adventure game environments
- Implements **ReAct** and **Reflexion** baselines
- Interactive fiction environment designed for reinforcement learning
- Explores flexible adaptation of playthrough strategy based on natural language feedback

### Abstract Excerpt
> "We explore the use of LLMs to power autonomous language agents in a text-adventure game environment. Text adventure games require flexible adaptation of playthrough strategy and action vocabulary based solely on natural language feedback."

---

## Summary of Patterns

| Approach | AI Model | Framework | Year | Game Type |
|---|---|---|---|---|
| Google Blog | Gemma 2 | Keras/Python | 2024 | Escape island adventure |
| pratikIT95 | Google Gemini | Spring Boot + Angular | 2025 | Murder mystery (Colonial India) |
| DSPy Tutorial | GPT-4o-mini | DSPy (Stanford) | 2025 | Fantasy RPG (Mystic Realm) |
| AddyOsmani | Claude Code / Copilot | Spec-driven dev | 2026 | General guide (not game-specific) |
| Nomad (ganileni) | OpenAI/Anthropic/Google | Python agent framework | 2025 | Plays Colossal Cave Adventure |
| Stanford CS224n | Various LLMs | ReAct/Reflexion | 2024 | Academic research |

### Common Design Patterns
- **System instructions** to define game lore, tone, and output format
- **JSON output** from AI for structured parsing (choices, scene descriptions, flags)
- **Session tracking** via UUID or conversation history management
- **Modular stage/location architecture** with per-stage system prompts
- **Maximum step/prompt limits** to prevent infinite loops
- **Save/load** game state functionality
- **Boundary systems** (Always/Ask/Never) for agent guardrails
- **Spec-first development** where specs double as AI agent instructions
