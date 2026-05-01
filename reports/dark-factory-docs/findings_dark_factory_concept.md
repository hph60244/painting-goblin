# Dark Factory / Lights-Out Manufacturing Applied to AI Coding Agents

## Research Findings — May 2026

---

## 1. Origin of the Term

The "dark factory" (or "lights-out manufacturing") concept originates from industrial manufacturing — specifically Fanuc Robotics in Japan (~2003), where robot-operated factories run without human presence. The factory floor stays dark because robots don't need light to work. The term was appropriated by the AI coding community in late 2025/early 2026 to describe fully autonomous software development pipelines where humans are neither needed nor welcome in the code generation loop.

---

## 2. Key Frameworks & Thinkers

### 2.1 Dan Shapiro's Five Levels of AI Coding Autonomy
**Source:** https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/

Shapiro mapped AI-assisted coding onto the NHTSA's five levels of driving automation:

| Level | Name | Description |
|-------|------|-------------|
| 0 | No Automation | vi/VS Code, every keystroke is yours; AI used only as search engine |
| 1 | Spicy Autocomplete | Offload discrete tasks ("write a unit test", "add a docstring"); Copilot/chat |
| 2 | Pair Programming | AI is a junior colleague; flow state, high productivity. Where 90% of "AI-native" devs live |
| 3 | Safety Driver | AI is the senior dev; you are the manager. Your life becomes diffs. Most people top out here |
| 4 | Robotaxi | You are a PM. Write specs, argue about specs, leave for 12 hours, check if tests pass |
| 5 | Dark Factory | Black box: specs in, software out. No human reads or reviews the code |

Key insight: Level 4 feels like the destination for most, but Level 5 is qualitatively different — "it's not really a car anymore."

### 2.2 StrongDM AI's Software Factory
**Source:** https://factory.strongdm.ai/

Justin McCarthy (StrongDM CTO) founded an AI team in July 2025 with two hard rules:
- **Code must not be written by humans**
- **Code must not be reviewed by humans**

Core concepts developed:
- **Scenarios** (not "tests"): End-to-end user stories stored outside the codebase (like holdout sets in ML), validated flexibly by LLM-as-judge
- **Satisfaction**: Probabilistic, empirical measure of whether observed trajectories satisfy the user
- **Digital Twin Universe (DTU)**: Behavioral clones of third-party APIs (Okta, Jira, Slack, Google Docs, etc.) for high-volume, deterministic validation without hitting real services
- **Compound correctness**: Post-Claude 3.5 (Oct 2024), long-horizon agentic coding began compounding correctness rather than error

StrongDM's philosophy: "If you haven't spent at least $1,000 on tokens today per human engineer, your software factory has room for improvement."

### 2.3 StrongDM Core Principles
**Source:** https://factory.strongdm.ai/principles

1. **Seed**: Start with a spec (PRD, screenshot, existing codebase)
2. **Loop**: Validation harness (end-to-end) → Feedback (sample output fed back in) → repeat until holdout scenarios pass
3. **Fuel**: Apply more tokens. Convert every obstacle into a representation the model can understand

### 2.4 StrongDM Key Techniques
**Source:** https://factory.strongdm.ai/techniques

- **Digital Twin Universe** — Clone external service behaviors for safe testing
- **Gene Transfusion** — Move working patterns between codebases via exemplars
- **The Filesystem** — Models navigate repos, files become practical memory
- **Shift Work** — Separate interactive from fully specified work
- **Semport** — Semantically-aware automated porting between languages
- **Pyramid Summaries** — Reversible multi-level context compression

---

## 3. The Attractor Pattern & Convergent Implementations

**Source:** https://2389.ai/posts/the-dark-factory-is-a-dot-file/

StrongDM open-sourced **attractor** (Feb 2026): ~5,700 lines of natural language specs (not code) describing a unified LLM client, coding agent loop, and DOT-based pipeline engine. Multiple independent teams built implementations that converged on the same 3-layer architecture:

| Layer | Kilroy (Go) | Mammoth (Go) | Smasher (Rust) | Tracker (Go) |
|-------|-------------|--------------|----------------|--------------|
| LLM Client | Provider adapters | Unified OpenAI/Anthropic/Gemini | Streaming, retries, provider quirks | Provider client with trace introspection |
| Agent Loop | Coding agent with tool dispatch | Steering, loop detection, subagents | 6 tools, steering rules, subagents | LLM-powered nodes with context injection |
| Pipeline Engine | DOT parser, CXDB checkpoints | DOT parser, graph engine, node handlers | Winnow parser, tokio broadcast | DAG walker, checkpointing, human gates |

Key insight: "The pipeline files are the durable artifact. The factory code is dorodango — polish it, throw it away, rebuild from spec."

Two pipeline styles emerged:
1. **Tool-heavy**: Deterministic shell commands, no LLM calls, runs in seconds, costs nothing
2. **LLM-heavy**: Every node is an LLM call (planning, scaffolding, implementation, review), takes 20+ minutes, costs $15+

The sweet spot: **hybrid** — deterministic tool nodes for setup/validation/deployment + LLM nodes where reasoning is actually needed.

---

## 4. The Dark Factory Harness for Research

**Source:** https://sotaverified.org/blog/improving-autoresearch-dark-factory-harness

David Colmenares extended the dark factory concept to ML research automation:

### Problems After 20 Autonomous Experiments
1. Random walk — no research context, no throughline
2. No memory of why things failed — can't distinguish OOM from shape mismatch
3. Only the final number — no loss curves, gradient norms, or diagnostic depth
4. Context fog — accumulated diffs and logs drown reasoning

### The 5 Principles of a Research Dark Factory
1. **Plan before you perturb** — Force hypothesis writing before code changes
2. **Give the agent eyes** — Rich structured JSON diagnostics per experiment
3. **Periodic distillation** — Every N experiments, synthesize meta-patterns into strategy docs
4. **Fail fast, fail cheap** — Crash advisor that maps tracebacks to fixes; disposable code
5. **The morning read** — Human reviews research decisions (not code) via hypothesis logs

---

## 5. Open-Source Dark Factory Tools

### Fabro
**Source:** https://github.com/fabro-sh/fabro

"The open source dark software factory for expert engineers." Rust-based, 734 stars, MIT license.
- Define processes as Graphviz DOT graphs
- Multi-model routing with CSS-like stylesheets
- Human-in-the-loop gates, cloud sandboxes, git checkpointing
- Automatic retrospectives after every run
- Single binary, no runtime dependencies

### OctopusGarden
**Source:** https://github.com/foundatron/octopusgarden

Open-source implementation of StrongDM's pattern: holdout scenarios, probabilistic satisfaction scoring via LLM-as-judge, convergence loop with no human code review.
- Notable concerns raised by author:
  1. Generated code works but is messy ("phenotype correct, genotype wild")
  2. Compliance (ISO 27001, SOC 2) is a nightmare
  3. Debugging is hard — Claude outages block smoke tests
  4. Security hardening needs better story
  5. Unit of responsibility keeps growing — how many services per SRE team?
  6. "I was surprised this works"

### Kilroy
**Source:** https://github.com/danshapiro/kilroy

Dan Shapiro's implementation. Local-first Go CLI, runs attractor pipelines in isolated git worktrees with CXDB checkpointing.

### Mammoth / Smasher / Tracker
**Source:** https://github.com/2389-research/

Three independent implementations from 2389 Research (Harper Reed):
- **Mammoth** (Go): Scope-crept into full spec engine with DOT linter, fan-in nodes, verification nodes
- **Smasher** (Rust): Lean, 5 crates, HTMX frontend with SSE streaming, used day-to-day
- **Tracker** (Go): Simple, bubbletea TUI, checkpointing, retry with backoff

---

## 6. Key Distinctions: Truly Autonomous vs. Interactive/Assisted

| Dimension | Interactive / Assisted | Truly Autonomous (Dark Factory) |
|-----------|----------------------|-------------------------------|
| Human role | Driver / pair programmer | Spec author / output consumer |
| Code reading | Human reviews diffs | No human reads code |
| Feedback loop | Real-time back-and-forth | Spec → generate → validate → converge |
| Validation | Human judgment + CI | LLM-as-judge + scenarios + holdout sets |
| Disengagement | Seconds to minutes | Hours to days |
| Error handling | Human debug | Crash advisor + revert + retry |
| Code quality | Maintained by humans | Dorodango — disposable, rebuild from spec |

---

## 7. Critical Concerns / Open Challenges

1. **Code maintainability** — Dark-factory-generated code works but humans often don't want to maintain it
2. **Compliance** — ISO 27001, SOC 2 with fully AI-generated codebases is an unsolved problem
3. **Debugging** — LLM outages block the entire pipeline; generated code is opaque
4. **Security** — AI-generated services need hardening beyond what current pipelines provide
5. **Scale of responsibility** — One engineer managing an AI-generated service mesh raises questions of accountability
6. **Token economics** — The "apply more tokens" principle has real dollar costs
7. **Reward hacking** — Agents cheat tests; holdout scenarios partially mitigate this
8. **The attractor problem** — Independent implementations converge on same architecture, suggesting a natural optimal form for this problem space

---

## 8. Summary

The dark factory concept for AI coding is real, actively evolving, and already producing working software. The key paradigm shift is: **specs are the expensive part; code is disposable.** Multiple independent teams have converged on the same 3-layer architecture (LLM client → agent loop → DOT pipeline engine). The primary open questions are around maintainability, compliance, and the changing role of human engineers from code writers to spec authors and system supervisors.

---

## Source URLs

1. https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/
2. https://factory.strongdm.ai/
3. https://factory.strongdm.ai/principles
4. https://factory.strongdm.ai/techniques
5. https://2389.ai/posts/the-dark-factory-is-a-dot-file/
6. https://sotaverified.org/blog/improving-autoresearch-dark-factory-harness
7. https://github.com/fabro-sh/fabro
8. https://github.com/foundatron/octopusgarden
9. https://news.ycombinator.com/item?id=47920020 (Ask HN: What does your agentic software dark factory look like?)
10. https://www.danshapiro.com/blog/2026/02/you-dont-write-the-code/
