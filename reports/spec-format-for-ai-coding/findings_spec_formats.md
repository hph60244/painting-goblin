# Spec Formats for AI Coding Agents — Research Findings

## 1. Gherkin/Cucumber (Given-When-Then) as Spec Format for AI

**Source:** https://cucumber.io/docs/gherkin/reference/

Gherkin is a structured, executable specification language using `Given`-`When`-`Then` keywords. It was designed for Behavior-Driven Development (BDD) and human readability.

### Key Facts:
- Gherkin uses keywords: `Feature`, `Rule`, `Example`/`Scenario`, `Given`, `When`, `Then`, `And`, `But`, `Background`, `Scenario Outline`, `Examples`.
- `Given` steps describe initial context (preconditions).
- `When` steps describe events or actions (the trigger).
- `Then` steps describe expected outcomes (assertions).
- Gherkin scenarios are **executable** — Cucumber matches each step to a step definition (code). The docs state: *"In addition to being a specification and documentation, an example is also a test. As a whole, your examples are an executable specification of the system."*
- Scenario Outlines support parameterized templates with data tables: `Scenario Outline: eating\n Given there are <start> cucumbers\n When I eat <eat> cucumbers\n Then I should have <left> cucumbers\n Examples: | start | eat | left |\n | 12 | 5 | 7 |`
- **Relevance to AI:** Gherkin's structured, unambiguous format maps well to LLM input. Each step is atomic, which helps AI agents plan and execute code. The Given-When-Then pattern gives AI a clear three-stage model of behavior: setup → action → verification.

### AI-Specific Advantages:
- Reduces ambiguity for LLMs — structured keywords constrain output space.
- Natural language within a formal scaffold — combines human readability with machine parseability.
- Parameterized outlines via `Scenario Outline` allow AI to generate test/data tables.
- Step definitions can map directly to function calls an AI agent must implement.
- Tools like SpecFlow and Cucumber already bridge human specs → executable tests, which AI can extend.

---

## 2. Markdown-Based Specs for AI Coding

**Source:** https://specstory.com/

### SpecStory
- **Tagline:** "Ship 10x smarter with perfect context. Every AI chat captured. Every decision remembered. Everyone aligned."
- SpecStory captures AI conversation history as a persistent context layer for agents like Cursor, Copilot, Claude Code, Gemini CLI, and Codex CLI.
- Described as: *"Stop losing valuable context. Start building on every decision and insight."*
- Key features: saves all AI conversations searchably, auto-generates Cursor rules from development history, shares context across teams.
- Philosophy: **"Intent is the new source code."** — meaning the spec/intent behind code matters as much as the code itself.
- Used by 3K+ active developers, 50K+ conversations saved, at companies like NVIDIA, Uber, Alibaba, MIT.

### Markdown as Spec Format (Broader Trend):
- Many AI coding tools use Markdown for `.cursorrules`, `CLAUDE.md`, `AGENTS.md`, and other instructions files.
- Markdown offers: headings for structure, bullet lists for requirements, code blocks for examples, tables for parameters.
- **Conventional commit specs** follow a structured format: `type(scope): description` — e.g. `feat(auth): add login endpoint`. This structured prefix helps AI understand intent.
- PR descriptions, READMEs, and issue templates all serve as lightweight spec documents that AI agents consume.

### AI-Specific Advantages:
- Markdown is the native output format of most LLMs — lowest friction.
- Easy to version control alongside code.
- `*.md` files like `AGENTS.md` serve as "living specs" that AI reads at session start.
- Hybrid format: can embed structured data (tables, code blocks, JSON) within free-form prose.

---

## 3. TDD (Test-Driven Development) with Unit Tests as Specs for AI

TDD's Red-Green-Refactor cycle serves as a natural spec mechanism for AI agents because unit tests define precise, verifiable behavioral contracts.

### Key Facts:
- In TDD, tests are written **before** implementation, making them the *de facto* specification.
- Test frameworks (Jest, pytest, JUnit, RSpec, etc.) provide structured assertion patterns.
- Each test defines: inputs, expected outputs, and edge cases.
- **For AI coding agents:** Tests are the most reliable spec because they are:
  - **Executable** — the AI can run them to verify its own output.
  - **Unambiguous** — a passing or failing test is binary.
  - **Granular** — individual tests map to individual behaviors.
- Cognition AI (makers of Devin) on evaluation: *"One of the best parts about software engineering is that outcomes are often objectively verifiable. In many cases, classical methods like code execution, compilers, linters, type checkers or unit tests are available to check correctness."*
- Devin's evaluation pipeline uses unit tests as ground truth for scoring: *"Generally these methods are preferred because they are deterministic and easy to use."*

### AI-Specific Advantages:
- Tests provide automatic verification — no human judgment needed for pass/fail.
- Test coverage reveals implicit spec gaps (untested = unspecified).
- AI agents like Devin, Copilot, and Cursor use `npm test` / `pytest` as feedback loops.
- SWE-bench, the standard benchmark for coding agents, evaluates based on test pass rates.
- The Cognition team writes: *"Numerical increases in score correlate directly with correctness, speed, and good communication on real-world agent tasks."*

---

## 4. Formal Specification Languages (TLA+, Alloy) Used with AI

### TLA+
**Source:** https://en.wikipedia.org/wiki/TLA%2B

- Created by Leslie Lamport (2013 Turing Award winner) for designing, modeling, and verifying concurrent and distributed systems.
- TLA+ is described as *"exhaustively-testable pseudocode"* and its use likened to *"drawing blueprints for software systems"*.
- Uses **Temporal Logic of Actions** to specify system behaviors across time.
- **Safety** ("bad things won't happen") defined via set theory and state predicates.
- **Liveness** ("good things eventually happen") defined via temporal logic (always/eventually operators).
- Comes with TLC model checker that performs exhaustive state-space exploration.
- **AWS has used TLA+ since 2011**, finding bugs in DynamoDB, S3, EBS, and an internal distributed lock manager. Quote: *"Some bugs required state traces of 35 steps."*
- **Microsoft Azure** used TLA+ to design Cosmos DB.
- **AI Relevance:** Formal specs like TLA+ are the most rigorous spec format. They eliminate ambiguity entirely but require significant expertise to write. AI agents could theoretically use TLA+ models as test oracles, verifying implementations against formal specs.

### Alloy
**Source:** https://alloytools.org/about.html

- Created at MIT by Daniel Jackson's Software Design Group.
- *"Alloy is a language for describing evolving structures and a tool for exploring them."*
- Based on relational logic — inspired by Z notation, Tarski's relational calculus, and Linear Temporal Logic.
- Alloy Analyzer is a solver that finds structures satisfying constraints, or generates counterexamples.
- Used for: security analysis, network topology design, finding holes in mechanisms.
- **AI Relevance:** Alloy's constraint-based approach is closer to how LLMs reason about code structure. The Alloy Analyzer can automatically find edge cases and counterexamples that an AI agent might otherwise miss.

### Comparison for AI Use:

| Aspect | TLA+ | Alloy | Gherkin | Unit Tests |
|--------|------|-------|---------|------------|
| Rigor | Highest | High | Medium | Medium-High |
| Learning curve | Steep | Moderate | Low | Low |
| Executable | Model-checked | Analyzer-checked | Yes (Cucumber) | Yes |
| Ambiguity | None | Near-none | Low | None |
| AI-friendliness | Low (math syntax) | Medium | High (English) | High |
| Verification | Exhaustive | SAT-based | Step-by-step | Per-test |

---

## 5. How AI Coding Tools Handle Specs

### GitHub Copilot
**Source:** https://github.com/features/copilot

- Uses context from open files, file paths, and repository URLs as implicit specs.
- Chat on GitHub.com creates contextual prompts combining: the user's prompt, open pages, and retrieved codebase/Bing context.
- Copilot Enterprise can index an organization's entire codebase for deeper understanding.
- **Spec mechanism:** Primarily implicit — the code itself and comments serve as the spec. No formal spec format required.
- "Agent mode" can plan and execute tasks autonomously, using files as specs.
- Supports custom MCP servers for extending context.

### Cursor
**Source:** https://www.cursor.com/features

- **Cursor Rules** (`.cursorrules`) are Markdown files that define project-specific instructions for the AI.
- Composer 2 agent mode uses PRD (Product Requirements Document) files — visible in their demo: `feature-prd.md` with sections like "Trigger", "View Behavior".
- Cursor agents read the codebase, plan tasks, and execute end-to-end (including running tests, deploying).
- **Spec mechanism:** A mix of `.cursorrules` for global instructions, `.md` spec documents for features, and existing code as implicit spec.
- The demo shows: *"Plan Mission Control / let's build a mission control interface"* — the AI reads a spec doc and creates implementation tasks from it.

### Devin (by Cognition AI)
**Source:** https://www.devin.ai/, https://cognition.ai/blog/evaluating-coding-agents

- Devin treats **tickets, issues, and PR descriptions** as specs.
- Devin evaluates itself using: unit tests, compilers, linters, type checkers, and **evaluator agents**.
- The Cognition team writes: *"One of the best parts about software engineering is that outcomes are often objectively verifiable."*
- Uses fine-tuning on previous migration examples to learn how to execute spec → code.
- Evaluation methodology: autonomous environments with simulated users, agent-as-evaluator, objective pass/fail criteria.
- **Spec mechanism:** Real-world tickets (Linear, GitHub Issues) + unit tests + evaluator agent instructions.

### General Patterns Across All Tools:

1. **Implicit specs** — the codebase itself (types, interfaces, existing patterns) serves as the primary spec.
2. **Explicit spec files** — Markdown files (`*.md`) with feature descriptions, PRDs, or `AGENTS.md` / `.cursorrules`.
3. **Executable specs** — Unit tests are the gold standard for verification across all tools.
4. **Conversation history** as spec — Tools like SpecStory capture past AI interactions to preserve "intent" and tribal knowledge.
5. **Issue tracker integration** — Linear, GitHub Issues, Jira tickets are treated as spec documents by agents like Devin.

---

## Summary: Which Spec Format Is Best for AI?

| Format | Best For | Limitations |
|--------|----------|-------------|
| **Gherkin** | Behavioral specs, acceptance criteria | Verbose for simple logic; requires step definitions |
| **Markdown** | General-purpose instructions, PRDs | Not executable; ambiguity remains |
| **Unit Tests** | Verifiable behavioral contracts | Doesn't explain *why*, only *what* |
| **TLA+/Alloy** | Distributed/concurrent systems, critical correctness | Steep learning curve; not suitable for UI/CRUD apps |
| **Cursor Rules / AGENTS.md** | Per-project AI configuration | Tool-specific; not standardized across tools |

**Recommendation:** The most effective approach combines Markdown for human-readable intent, unit tests for verifiable contracts, and structured patterns (Gherkin-like or custom) for behavioral specifications. Tools like SpecStory that capture conversation history provide a "context layer" that preserves spec evolution across sessions.

---

### Source URLs
- https://cucumber.io/docs/gherkin/reference/
- https://specstory.com/
- https://en.wikipedia.org/wiki/TLA%2B
- https://alloytools.org/about.html
- https://github.com/features/copilot
- https://www.cursor.com/features
- https://www.devin.ai/
- https://cognition.ai/blog/evaluating-coding-agents
