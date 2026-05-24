# Findings: AI Code Agents for Full Application Generation

## Research Date: 2026-05-01

---

## 1. Overview of the Landscape

Modern AI code agents have matured significantly and can now generate full applications (including CRUD apps, data-fetching tools, and RSS readers) from natural language requirements. The key players fall into two categories: **agentic coding tools** (Claude Code, Cursor Agent) that operate on your codebase autonomously, and **AI software engineers** (Devin) that function as independent developers. Additionally, **rapid prototyping tools** (Claude Artifacts) allow single-shot generation of interactive web apps.

---

## 2. AI Code Agents Ranked by Full-Application Generation Capability

### Tier 1: Most Capable for Full-Stack Apps from Requirements

| Agent | Strengths | Limitations |
|-------|-----------|-------------|
| **Claude Code** | Reads entire codebase; autonomous multi-file editing; runs commands & tests; MCP for external tool integration; sub-agents for parallel work; `CLAUDE.md` for persistent instructions; Plan Mode for requirements-first workflow | Context window fills quickly with large projects; requires clear oversight for complex apps |
| **Devin** | Designed for multi-week, multi-repo projects; can spin up teams of agents; fine-tunable for specific tasks; integrates with Slack, Linear, Datadog; used by Nubank for 6M+ line migrations | Enterprise-focused; less accessible for individual/small-team rapid prototyping |
| **Cursor Agent (Composer)** | Deep IDE integration; rule-based customization (`.cursorrules`); can read your entire project; YOLO mode for autonomous execution; strong TypeScript/React generation | Less proven for large-scale autonomous multi-day tasks than Claude Code or Devin |

### Tier 2: Strong Prototyping & Assisted Development

| Agent | Strengths | Limitations |
|-------|-----------|-------------|
| **GitHub Copilot (Agent Mode)** | Deep GitHub integration; supports multiple models (Claude, GPT, Gemini); cloud agents for background tasks; massive ecosystem | Agent mode is newer; less autonomous than Claude Code for complex multi-file generation |
| **Claude Artifacts** | Single-prompt interactive web app generation (HTML/CSS/JS); Simon Willison built 14 apps in one week; 5-21 minutes per app | Cannot make API calls directly; limited to client-side JavaScript; no backend/database support |

---

## 3. Concrete Examples & Success Stories

### 3.1 Simon Willison's Claude Artifacts (14 Apps in One Week)

**Source:** https://simonwillison.net/2024/Oct/21/claude-artifacts/

Simon Willison documented building 14 interactive web applications using Claude Artifacts in a single week. Notable examples relevant to data-fetching/CRUD:

- **URL to Markdown with Jina Reader** — A web UI that accepts a URL, calls the Jina Reader API to convert page content to Markdown, and provides a copy button. This is a direct analog of an RSS reader's fetch-and-display pattern.
- **OpenAI Audio Recorder** — A microphone-recording web app that base64-encodes audio and sends it to the OpenAI API. Demonstrates data-fetching, encoding, and external API integration.
- **SQLite in WASM Demo** — An in-browser SQLite database that runs entirely in WASM, demonstrating that AI agents can generate CRUD apps with actual database queries.
- **QR Code Decoder** — Paste/drag-and-drop an image, decode QR data, display as hyperlink. Built in seconds.

**Key takeaway:** Most of these took 5-21 minutes from prompt to working app. The prompt pattern was simple: *"Build an artifact (no react) that lets me [verb] [noun] and displays [output]"* followed by iterative refinement.

### 3.2 Claude Code Building Features Across a Codebase

**Source:** https://docs.anthropic.com/en/docs/claude-code/overview

Claude Code is described as capable of: "Describe what you want in plain language. Claude Code plans the approach, writes the code across multiple files, and verifies it works." For bugs: "paste an error message or describe the symptom. Claude Code traces the issue through your codebase, identifies the root cause, and implements a fix."

Example prompts for app building:
- `claude "write tests for the auth module, run them, and fix any failures"`
- `claude "commit my changes with a descriptive message"`

### 3.3 Devin at Nubank: Multi-Million Line Migration

**Source:** https://www.devin.ai/

Nubank used Devin to migrate a 6M+ line ETL monolith to sub-modules. Results:
- **8-12x engineering efficiency gain** (comparing engineering hours vs. prompt+review time)
- **20x cost savings**
- ~100,000 data class implementations migrated
- Fine-tuned Devin's completion rate **doubled** and task speed improved **4x** (40 min → 10 min per sub-task)

**Relevance to RSS reader:** If Devin can handle a multi-million line migration with complex business logic, it is more than capable of generating a greenfield RSS reader from requirements. The fine-tuning approach used by Nubank (collecting examples, creating benchmark eval sets) is a pattern that could apply to generating domain-specific apps.

### 3.4 GitHub Copilot Agent Mode

**Source:** https://github.com/features/copilot

GitHub Copilot now supports agent mode where you can "assign tasks to agents like Copilot, Claude by Anthropic, and OpenAI Codex, and let them plan, explore, and execute work autonomously in the background." Cloud agents handle multi-step workflows. The Copilot Spaces feature allows creating a "shared source of truth" with context from docs and repositories — a structured requirements approach.

---

## 4. Prompt Engineering Patterns That Work

### 4.1 The "Explore → Plan → Implement → Commit" Pattern (Claude Code)

**Source:** https://docs.anthropic.com/en/docs/claude-code/best-practices

1. **Explore:** Read relevant files, understand the codebase. Use Plan Mode.
2. **Plan:** Ask Claude to create a detailed implementation plan. Press `Ctrl+G` to edit before proceeding.
3. **Implement:** Switch to normal mode. Let Claude code, verifying against its plan.
4. **Commit:** Ask Claude to commit with a descriptive message and create a PR.

**Prompt template:**
```txt
I want to build [description]. Interview me in detail using the AskUserQuestion tool.
Ask about technical implementation, UI/UX, edge cases, concerns, and tradeoffs.
Keep interviewing until we've covered everything, then write a complete spec to SPEC.md.
```

### 4.2 The "One-Shot Prototype" Pattern (Claude Artifacts)

**Source:** https://simonwillison.net/2024/Oct/21/claude-artifacts/

```txt
Build an artifact (no react) that lets me [paste/upload/input X] and [transforms/decodes/displays Y].
Make it mobile friendly. Include a [copy/download] button.
```

The pattern works because:
- No framework constraints ("no react" avoids unnecessary complexity)
- Single purpose (focuses the model on one clear function)
- UI elements explicitly named ("copy button", "drag and drop")
- Mobile friendliness requested upfront (avoids desktop-only layouts)

### 4.3 The "Specification Interview" Pattern

**Source:** https://docs.anthropic.com/en/docs/claude-code/best-practices

Claude Code has an `AskUserQuestion` tool that it can use to interview you about requirements. The recommended approach for large features:

```txt
I want to build [brief description]. Interview me in detail using the AskUserQuestion tool.
Ask about technical implementation, UI/UX, edge cases, concerns, and tradeoffs.
Don't ask obvious questions, dig into the hard parts I might not have considered.
Keep interviewing until we've covered everything, then write a complete spec to SPEC.md.
```

Once the spec is written, start a **fresh session** to implement it — clean context focused purely on execution.

### 4.4 Provide Verification Criteria

**Source:** https://docs.anthropic.com/en/docs/claude-code/best-practices

This is "the single highest-leverage thing you can do." Include tests, screenshots, or expected outputs so Claude can check itself.

| Before | After |
|--------|-------|
| *"implement a function that validates email addresses"* | *"write a validateEmail function. example test cases: user@example.com is true, invalid is false, user@.com is false. run the tests after implementing"* |

### 4.5 Reference Existing Patterns

```txt
Look at how existing widgets are implemented on the home page to understand the patterns.
HotDogWidget.php is a good example. Follow the pattern to implement a new [component].
Build from scratch without libraries other than the ones already used in the codebase.
```

### 4.6 Simon Willison's "Weird Intern" Mental Model

**Source:** https://simonwillison.net/2024/Sep/20/using-llms-for-code/

Treat the AI as an intern who is "screamingly fast, has read all documentation, is massively overconfident, makes mistakes, doesn't realize them, never gets tired, and never gets upset." The workflow:
1. Ask for options first
2. Request a quick prototype of the best option
3. Iterate aggressively: "No, do it again. Do it differently. Change that."
4. Never accept the first output as final

---

## 5. Limitations & Challenges

### 5.1 Context Window Constraints

**Source:** https://docs.anthropic.com/en/docs/claude-code/best-practices

"The context window is the most important resource to manage." Performance degrades as context fills. Symptoms include "forgetting" earlier instructions and making more mistakes. Mitigations:
- Run `/clear` between unrelated tasks
- Use sub-agents for investigation (they run in separate context windows)
- Keep CLAUDE.md concise
- Use `/compact` to summarize when approaching limits

### 5.2 Kitchen Sink Sessions

A common failure pattern: starting with one task, asking something unrelated, then returning to the first task. Context gets polluted with irrelevant information. Fix: `/clear` between unrelated tasks.

### 5.3 The Trust-Then-Verify Gap

AI agents "produce a plausible-looking implementation that doesn't handle edge cases." Always provide verification (tests, scripts, screenshots). If you can't verify it, don't ship it.

### 5.4 Artifact API Restrictions

Claude Artifacts cannot make API calls to external hosts, submit forms, or link out to other pages. This limits their use for truly full-stack apps. They are best for client-side prototypes that can later be hosted independently.

### 5.5 Claude Code Still Requires Oversight

Claude Code is a "copilot, not autopilot." It requires periodic human review, especially for:
- Architecture decisions that have long-term implications
- Security-sensitive code
- Complex business logic
- Integration with existing systems

### 5.6 Noisy / Distracting Output

Cursor and other tools can sometimes produce overly verbose output or get distracted. The Cursor team notes that the agent can sometimes be "too helpful" by editing things it shouldn't, requiring careful use of rules and `.cursorrules` files.

---

## 6. Recommendations for Building an RSS Reader with AI Code Agents

Based on the research, the most effective approach would be:

1. **Use Claude Code** as the primary agent (strongest balance of autonomy, codebase understanding, and tool integration).
2. **Start with the "Specification Interview" pattern** — let Claude Interview you and produce a SPEC.md.
3. **Create a CLAUDE.md** before starting with build commands, preferred tech stack, and coding conventions.
4. **Use Plan Mode** for architecture exploration (feed data model, API routes, component tree).
5. **Implement iteratively**: backend (RSS fetching/parsing/storage) → API layer → frontend.
6. **Provide verification criteria**: sample RSS feeds, expected output formats, test cases.
7. **Use sub-agents** for parallel work (e.g., one agent for the XML parser, another for the UI).
8. **Commit frequently** so you can rewind if the agent goes off track.

For a single-page RSS reader prototype, **Claude Artifacts** can generate a working HTML/CSS/JS version in under 30 minutes (see the Jina Reader Tool as a direct analog at https://tools.simonwillison.net/jina-reader).

---

## 7. Source URLs

| Source | URL |
|--------|-----|
| Claude Code Overview | https://docs.anthropic.com/en/docs/claude-code/overview |
| Claude Code Best Practices | https://docs.anthropic.com/en/docs/claude-code/best-practices |
| Simon Willison — Claude Artifacts (14 apps in 1 week) | https://simonwillison.net/2024/Oct/21/claude-artifacts/ |
| Simon Willison — Using LLMs for Code | https://simonwillison.net/2024/Sep/20/using-llms-for-code/ |
| GitHub Copilot Features | https://github.com/features/copilot |
| Devin AI (Cognition Labs) | https://www.devin.ai/ |
