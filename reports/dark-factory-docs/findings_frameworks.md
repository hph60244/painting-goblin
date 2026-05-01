# Frameworks & Patterns for Autonomous AI Code Agent Execution

## Research Findings — May 2026

---

## 1. The Autonomous Coding Landscape Overview

The ecosystem of fully autonomous AI coding tools (Level 4-5 on Dan Shapiro's autonomy scale) divides into three architectural camps:

| Architecture | Examples | Key Idea | Statefulness |
|---|---|---|---|
| **File-based task queue** (FSMQ) | painting-goblin | Filesystem as the message bus; `todo/doing/done/failed` dirs | Stateless executor, stateful filesystem |
| **DOT pipeline engine** | Fabro, Kilroy, Mammoth, Smasher, Tracker | Graphviz DOT files define DAGs of LLM + tool nodes | Pipeline-defined state machine |
| **Multi-agent orchestration** | Claude Code agent teams, sub-agents | Coordinated parallel sessions with shared task lists | Ephemeral sessions + persistent task list |
| **Cloud-hosted autonomous sessions** | Claude Code routines, Devin | Full sessions run on managed infra, triggered by schedule/events/API | Fully managed state |

---

## 2. painting-goblin: File-System-Based Task Queue (FSMQ)

**Source:** `C:\Users\fnaith\Documents\Fork\painting-goblin\README.md`, `executor.py`, `scheduler.py`

painting-goblin implements a **filesystem-as-message-bus** pattern:

### Architecture
- **Publisher**: Scans `tasks/todo/`, locks the oldest unprocessed `.md` file, moves it to `tasks/doing/` with a UUID suffix to avoid name collisions
- **Subscriber**: Picks up tasks from `tasks/doing/`, spawns `opencode run --file <task.md>` with an `AGENT_PROMPT` that enforces non-interactive autonomous behavior, moves result to `tasks/done/` or `tasks/failed/`
- **Scheduler**: APScheduler-based cron system—reads `config.ini` for `[job:name]` sections, copies job `.md` files to `todo/` on schedule, supports parameterized job variants via filename encoding (`task_param-value.md`)
- **Locking**: `filelock` (Python) per-task, non-blocking acquire, prevents double-processing
- **Heartbeat + Monitor**: Log-file-modification-time monitoring detects stalled tasks; terminates processes that exceed `monitor_timeout_sec`

### AGENT_PROMPT (Autonomy Enforcement)
The system injects a hardcoded system prompt into every task:
```
You are an autonomous, non-interactive agent.
Operational Rules:
1. Do not ask the user any questions or request confirmations.
2. Do not present options or require user selections.
3. Make all decisions automatically based on the provided configuration and policies.
4. Follow a deny-by-default principle for any unauthorized or ambiguous actions.
5. Operate only within explicitly allowed resources.
6. Provide clear, deterministic outcomes for every task.
7. If assumptions are made, document them without requesting clarification.
Your objective is to complete tasks reliably in a fully automated environment.
```

### Communication Pattern
- **Publisher-Subscriber** (not Pub/Sub messaging — it's a task queue with producer-consumer roles)
- No message broker; filesystem = queue
- Task parameters encoded in filenames: `_priority-high_topic-ai.md` → parsed as `[("priority","high"),("topic","ai")]`, injected as env vars
- UUID-based deduplication: base64-urlsafe UUIDv4 (22 chars) appended to filenames

### Unique Characteristics vs. Other Approaches
- **No DOT graphs**: Tasks are flat `.md` files, not DAG nodes
- **No LLM orchestration**: The orchestrator (Python) never calls an LLM—it delegates entirely to OpenCode
- **Stateless executor**: The Python processes can be killed and restarted; task state lives entirely in the filesystem
- **Single-agent-per-task**: Unlike Claude Code agent teams or DOT pipelines, each task is handled by exactly one agent instance

---

## 3. Claude Code: Sub-Agents, Agent Teams, and Routines

**Source:** https://docs.anthropic.com/en/docs/claude-code/sub-agents
**Source:** https://docs.anthropic.com/en/docs/claude-code/agent-teams
**Source:** https://docs.anthropic.com/en/docs/claude-code/routines

### 3.1 Sub-Agents
Single-session delegation model. A main agent spawns child agents that run in their own context windows:

| Agent | Model | Tools | Purpose |
|---|---|---|---|
| **Explore** | Haiku | Read-only | Codebase search, file discovery |
| **Plan** | Inherited | Read-only | Codebase research for planning |
| **General-purpose** | Inherited | All tools | Complex multi-step tasks |

- Sub-agents defined as Markdown files with YAML frontmatter
- Placed in `.claude/agents/` (project), `~/.claude/agents/` (user), or via `--agents` CLI flag
- Support: tool allowlists/denylists, permission modes (`auto`, `dontAsk`, `bypassPermissions`, `plan`), model selection, persistent memory, hooks, MCP server scoping, git worktree isolation
- **Fork mode** (experimental): inherits full conversation history, runs sub-agents in background with shared prompt cache
- Sub-agents **cannot** spawn other sub-agents

### 3.2 Agent Teams
Multi-session orchestration. A team lead coordinates independent Claude Code instances:

- **Architecture**: Lead + teammates (each a full Claude Code session) + shared task list (file-based, on local filesystem) + mailbox (inter-agent messaging)
- **Task list**: Tasks have states (pending → in progress → completed), dependencies, locking to prevent race conditions
- **Display modes**: In-process (Shift+Down to cycle) or split panes (tmux/iTerm2)
- **Teammate spawning**: Natural language descriptions, optional subagent-type references, optional plan-approval gates
- **Communication**: Direct `SendMessage` between teammates, auto-idle notifications, task auto-claiming
- **Limitations**: No nested teams, one team per session, no session resumption for in-process teammates, task status lag

### 3.3 Routines
Fully autonomous cloud-hosted sessions:

- **Triggers**: Cron schedule, HTTP API endpoint, GitHub webhook events (PR opened/released/etc.)
- **Runs on**: Anthropic-managed cloud infrastructure (laptop can be off)
- **Permissions**: No approval prompts; all decisions autonomous
- **Branch policy**: `claude/`-prefixed branches by default; unrestricted pushes optional per repo
- **Usage**: Daily run caps + per-account subscription limits
- **Connectors**: MCP servers for Slack, Linear, GitHub, etc.
- **One-off scheduling**: Natural language time descriptors (`/schedule in 2 weeks`)

### 3.4 Comparison with painting-goblin
| Dimension | Claude Code Routines | painting-goblin |
|---|---|---|
| Queue mechanism | Proprietary cloud backend | Filesystem (`todo/doing/done/failed`) |
| Scheduler | Cron/API/GitHub webhook | APScheduler (cron in config.ini) |
| Agent model | Claude (hosted) | OpenCode (any model) |
| Autonomy enforcement | Built-in cloud mode | Hardcoded AGENT_PROMPT |
| Execution env | Anthropic cloud | Local machine |
| Parallelism | Per-task new session | Per-task new OpenCode process |
| Task format | Any Claude-compatible prompt | `.md` files in queue dirs |

---

## 4. Devin by Cognition AI

**Source:** https://www.cognition.ai/blog/introducing-devin (March 12, 2024)

The first commercially marketed "AI software engineer":

- **SWE-bench**: 13.86% resolved (vs. previous SOTA 1.96%)
- **Capabilities**: Long-term reasoning and planning, shell/code-editor/browser in sandboxed compute environment
- **Interaction**: Real-time progress reporting, accepts feedback, collaborates on design choices
- **Work modes**: Both interactive (collaborative) and autonomous (GitHub issue → PR)
- **Pricing model**: Subscription-based, cloud-hosted
- **Key differentiator**: End-to-end from issue to pull request with no human code writing

Quote: *"Devin can plan and execute complex engineering tasks requiring thousands of decisions. Devin can recall relevant context at every step, learn over time, and fix mistakes."*

**SWE-bench results context:**
- Unassisted: 13.86%
- Previous best assisted (told exact files): 4.80%
- Previous best unassisted: 1.96%

---

## 5. DOT (Dependency-Ordered Tasks) Pipeline Engines

**Source:** https://2389.ai/posts/the-dark-factory-is-a-dot-file/

The "attractor pattern"—multiple independent implementations converging on identical 3-layer architecture:

### Convergent 3-Layer Architecture

| Layer | Kilroy (Go) | Mammoth (Go) | Smasher (Rust) | Tracker (Go) |
|---|---|---|---|---|
| **LLM Client** | Provider adapters | Unified OpenAI/Anthropic/Gemini | Streaming, retries, provider quirks | Provider client with trace introspection |
| **Agent Loop** | Coding agent with tool dispatch | Steering, loop detection, subagents | 6 tools, steering rules, subagents | LLM-powered nodes with context injection |
| **Pipeline Engine** | DOT parser, CXDB checkpoints | DOT parser, graph engine, node handlers | Winnow parser, tokio broadcast | DAG walker, checkpointing, human gates |

Key quote: *"The pipeline files are the durable artifact. The factory code is dorodango — polish it, throw it away, rebuild from spec."*

### Two Pipeline Styles
1. **Tool-heavy**: Deterministic shell commands, no LLM calls, runs in seconds, costs nothing
2. **LLM-heavy**: Every node is an LLM call (planning, scaffolding, implementation, review), takes 20+ minutes, costs $15+

**Sweet spot**: Hybrid — deterministic tool nodes for setup/validation/deployment + LLM nodes where reasoning is needed.

---

## 6. Fabro

**Source:** https://github.com/fabro-sh/fabro

"The open source dark software factory for expert engineers":
- **Language**: Rust
- **License**: MIT
- **Stars**: 734+
- **Pipeline definition**: Graphviz DOT graphs
- **Features**: Multi-model routing with CSS-like stylesheets, human-in-the-loop gates, cloud sandboxes, git checkpointing, automatic retrospectives
- **Deployment**: Single binary, no runtime dependencies

---

## 7. Kilroy

**Source:** https://github.com/danshapiro/kilroy (inferred from 2389.ai article)

Dan Shapiro's implementation of the dark factory pattern:
- **Language**: Go
- **Architecture**: Local-first CLI
- **Pipeline engine**: DOT parser, CXDB checkpointing
- **Isolation**: Git worktrees
- **Relation to attractor**: One of the four convergent implementations

---

## 8. OctopusGarden

**Source:** https://github.com/foundatron/octopusgarden

Open-source implementation of StrongDM's pattern:
- **Key features**: Holdout scenarios, probabilistic satisfaction scoring via LLM-as-judge, convergence loop with no human code review
- **Notable concerns** from author:
  1. "Phenotype correct, genotype wild" — code works but is messy
  2. Compliance (ISO 27001, SOC 2) is a nightmare
  3. LLM outages block the entire pipeline
  4. Security hardening needs better story
  5. Unit of responsibility keeps growing
  6. **"I was surprised this works"**

---

## 9. StrongDM's Attractor Pattern & Dark Factory Principles

**Sources:**
- https://factory.strongdm.ai/
- https://factory.strongdm.ai/principles
- https://factory.strongdm.ai/techniques

Justin McCarthy (StrongDM CTO) founded an AI team in July 2025 with two hard rules:
- **Code must not be written by humans**
- **Code must not be reviewed by humans**

### Core Concepts
- **Scenarios** (not "tests"): End-to-end user stories stored outside the codebase (holdout sets), validated flexibly by LLM-as-judge
- **Satisfaction**: Probabilistic, empirical measure of whether observed trajectories satisfy the user
- **Digital Twin Universe (DTU)**: Behavioral clones of third-party APIs for high-volume deterministic validation
- **Compound correctness**: Post-Claude 3.5 (Oct 2024), long-horizon agentic coding began compounding correctness rather than error

### Core Loop
1. **Seed**: Start with a spec (PRD, screenshot, existing codebase)
2. **Loop**: Validation harness → Feedback → repeat until holdout scenarios pass
3. **Fuel**: Apply more tokens. Convert every obstacle into a representation the model can understand

### Key Techniques
- **Gene Transfusion** — Move working patterns between codebases via exemplars
- **The Filesystem** — Models navigate repos; files become practical memory
- **Shift Work** — Separate interactive from fully specified work
- **Semport** — Semantically-aware automated porting between languages
- **Pyramid Summaries** — Reversible multi-level context compression

Quote: *"If you haven't spent at least $1,000 on tokens today per human engineer, your software factory has room for improvement."*

---

## 10. Comparison: painting-goblin vs. Other Approaches

| Dimension | painting-goblin (FSMQ) | DOT Pipeline (Fabro/Kilroy) | Claude Code Routines | Devin |
|---|---|---|---|---|
| **Queue** | Filesystem dirs | DOT graph nodes | Cloud backend | Proprietary |
| **Task format** | `.md` files | `*.dot` graph files | Prompt + repo | Natural language |
| **Orchestrator** | Python (no LLM) | LLM + tool nodes | Cloud service | Proprietary |
| **Parallelism** | Per-subscriber | DAG node scheduling | Per-trigger session | Single session |
| **Scheduling** | APScheduler (local cron) | N/A (triggered) | Cloud cron/API/GitHub | N/A (on-demand) |
| **Failure handling** | Move to `failed/` dir | Checkpoint + retry | Session replay | Unknown |
| **Monitoring** | Log-file heartbeat + timeout | CXDB checkpointing | Cloud dashboard | Unknown |
| **Context isolation** | Per-process OpenCode | Per-node | Per-session | Unknown |
| **Human role** | Write `.md` task files | Write DOT spec | Write prompt/schedule | Issue author |
| **Cost model** | Local compute only | Token costs only | Subscription + token | Subscription |
| **Open source** | Yes (custom) | Yes (MIT/varies) | No (proprietary) | No (proprietary) |

### Key Architectural Differences

**1. Orchestrator intelligence**: painting-goblin's orchestrator (Python) has zero LLM calls—it's pure filesystem operations. DOT pipelines use LLMs to decide routing and node execution. Claude Code Routines use cloud-based Claude.

**2. Task granularity**: painting-goblin tasks are monolithic `.md` files given to a single agent. DOT pipelines decompose work into a DAG of small, composable steps (e.g., "plan → scaffold → implement → test → review").

**3. State management**: painting-goblin uses the filesystem as both queue and state store. DOT pipelines use CXDB/checkpoint files. Claude Code uses cloud state. Devin uses proprietary state management.

**4. Scaling model**: painting-goblin scales by adding subscriber processes (threads). DOT pipelines scale by adding nodes to the DAG. Claude Code scales by creating more cloud sessions.

**5. Autonomy enforcement**: painting-goblin injects a hardcoded AGENT_PROMPT into every task. Claude Code has built-in permission modes. Devin has implicit autonomous behavior. DOT pipelines have no explicit autonomy prompt—autonomy is embedded in the pipeline structure.

---

## 11. GitHub Spec Kit

Multiple search attempts for `github.com/spec-spec/kit` returned 404. This suggests the repository either:
- Does not exist publicly
- Was renamed or moved
- Refers to a different tool/pattern not yet public

The "spec spec" concept appears in the dark factory literature as a shorthand for **specifications about specifications**—i.e., meta-specs that define how specs should be written for AI consumption. This ties into the broader finding that **specs are the expensive part; code is disposable.**

---

## 12. Key Quotes

> *"The pipeline files are the durable artifact. The factory code is dorodango — polish it, throw it away, rebuild from spec."* — 2389 Research

> *"If you haven't spent at least $1,000 on tokens today per human engineer, your software factory has room for improvement."* — Justin McCarthy, StrongDM

> *"I was surprised this works."* — OctopusGarden author

> *"Level 4 feels like the destination for most, but Level 5 is qualitatively different — it's not really a car anymore."* — Dan Shapiro, on the 5 Levels of AI Coding Autonomy

> *"Code must not be written by humans. Code must not be reviewed by humans."* — StrongDM founding rules

> *"Phenotype correct, genotype wild."* — OctopusGarden author, on AI-generated code quality

---

## 13. Synthesis & Implications for painting-goblin

painting-goblin's filesystem-based task queue (FSMQ) pattern is a **minimalist, pragmatic implementation** of the dark factory concept. It maps to Level 4 on Dan Shapiro's scale (Robotaxi — "write specs, leave for 12 hours, check if tests pass") or Level 5 (Dark Factory — "specs in, software out, no human reads code") depending on how the task `.md` files are authored.

### Where painting-goblin fits uniquely:
1. **Lowest infrastructure overhead**: No cloud, no database, no message broker—just a filesystem
2. **Maximum portability**: Works on any OS with Python + any AI CLI tool (currently OpenCode, but swappable)
3. **Simple failure model**: `done/failed` directories are an elegant, inspectable state store
4. **No LLM vendor lock-in**: The orchestrator never calls an LLM directly; it only delegates to an external agent

### Where painting-goblin could grow:
1. **DOT pipeline integration**: Instead of monolithic `.md` task files, support `.dot` files that define multi-step pipelines (plan → implement → test → review)
2. **Task dependencies**: DAG-based task scheduling (currently tasks are independent)
3. **Self-verification**: Like StrongDM's "scenarios" or OctopusGarden's LLM-as-judge
4. **Checkpointing**: Currently no intermediate state preservation
5. **Parallel tasks within one agent**: Spawn sub-tasks for large projects

---

## Source URLs

1. https://docs.anthropic.com/en/docs/claude-code/sub-agents
2. https://docs.anthropic.com/en/docs/claude-code/agent-teams
3. https://docs.anthropic.com/en/docs/claude-code/routines
4. https://www.cognition.ai/blog/introducing-devin
5. https://2389.ai/posts/the-dark-factory-is-a-dot-file/
6. https://github.com/fabro-sh/fabro
7. https://github.com/danshapiro/kilroy
8. https://github.com/foundatron/octopusgarden
9. https://factory.strongdm.ai/
10. https://factory.strongdm.ai/principles
11. https://factory.strongdm.ai/techniques
12. https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/
13. https://sotaverified.org/blog/improving-autoresearch-dark-factory-harness
14. https://github.com/2389-research/
