# Comparative Analysis of AI Agent Frameworks: Harness Engineering Perspective

> **Research Date:** 2026-04-28
> **Scope:** Claude Code (Anthropic), OpenAI Codex CLI, with reference to Gemini CLI and ecosystem patterns
> **Focus Areas:** Context management, tool governance/safety, state persistence/recovery, feedback mechanisms, production vs. demo readiness

---

## 1. Executive Summary

The AI coding agent landscape is consolidating around two dominant production-grade architectures: **Claude Code (Anthropic)** and **Codex CLI (OpenAI)**. Both have matured beyond demo-stage "chat with code" into full agentic platforms with hierarchical permissions, sandboxed execution, multi-session memory, and enterprise-grade governance. A third category of "demo-grade" frameworks (exemplified by repositories like awesome-llm-apps and single-agent RAG tutorials) provides rapid prototyping but lacks the scaffolding needed for production deployment.

Key finding: **Claude Code leads on context management depth and cross-session memory; Codex CLI leads on OS-level sandboxing breadth and enterprise observability; both are production-grade but take meaningfully different architectural approaches.**

## 2. Claude Code Architecture (Anthropic)

### 2.1 Context Management

Claude Code uses a **hierarchical context injection model**:

- **System prompt + CLAUDE.md (project/user/managed):** Loaded at session start. CLAUDE.md files are delivered as a user message after the system prompt (not part of the system prompt), so compliance is behavioral rather than enforced.
- **Auto memory:** Claude writes its own notes across sessions -- build commands, debugging insights, code style preferences. First 200 lines (or 25KB) are loaded every session. Topic files are loaded on-demand.
- **Hierarchical CLAUDE.md resolution:** Walks up directory tree, loading files from each ancestor directory.
- **Path-scoped rules (.claude/rules/):** YAML frontmatter with paths field scopes instructions to specific file globs. Only loads when Claude reads matching files.
- **Compaction (/compact):** When context window fills, Claude Code compacts -- project-root CLAUDE.md survives (re-read from disk).

**Key limitation:** CLAUDE.md is context, not configuration. Anthropic states: "Settings rules are enforced by the client regardless of what Claude decides to do. CLAUDE.md instructions shape Claude behavior but are not a hard enforcement layer."

### 2.2 Tool Governance and Safety

Claude Code employs a tiered permission system with multiple modes:

- **Hierarchical permission rules:** deny > ask > allow precedence. Rules use Tool(specifier) format with glob/wildcard support.
- **Bash-specific controls:** Read-only command recognition. Compound commands parsed; subcommands independently matched. Process wrapper stripping applied.
- **Sandboxing:** OS-level filesystem and network isolation for Bash commands. Defense-in-depth.
- **Managed settings (enterprise):** 5 delivery mechanisms (server-managed, MDM/OS-level policies, file-based). Managed settings cannot be overridden.
- **CLAUDE.md as managed policy:** Organization-wide file that cannot be excluded by individual settings.
- **Hooks for extended governance:** PreToolUse hooks can deny, force prompts, or skip prompts.

**Key quote:** "Permission deny rules block Claude from even attempting to access restricted resources. Sandbox restrictions prevent Bash commands from reaching resources outside defined boundaries, even if a prompt injection bypasses Claude decision-making."

### 2.3 State Persistence and Recovery

- Session transcripts written to disk automatically. cleanupPeriodDays controls retention (default 30 days).
- Auto memory is machine-local, per-git-repo. Plain markdown, human-editable.
- Customizable git commit/PR attribution strings.
- Sessions move between terminal, desktop app, web, and VS Code. Remote Control for mobile.

### 2.4 Multi-Agent Architecture

- Sub-agents: Lead agent spawns sub-agents for parallel work. Sub-agents maintain their own auto memory.
- Agent SDK: For custom orchestration, tool access, and permission control.
- MCP (Model Context Protocol): Open standard for external tool connections.

---

## 3. OpenAI Codex CLI Architecture

### 3.1 Context Management

Codex CLI uses a configuration-driven context model:

- AGENTS.md (or Rules): Similar to CLAUDE.md. Cross-compatible via @AGENTS.md import.
- Memories system: Persistent memory across sessions. Chronicle subsystem for structured memory.
- Workflows: Reusable, parameterized multi-step procedures.
- Context compaction: API-level conversation state management.

**Key difference:** Codex relies more on explicit config.toml for persistent behavior. Claude uses in-context CLAUDE.md. Codex is more prescriptive/configuration-heavy; Claude is more fluid/context-adaptive.

### 3.2 Tool Governance and Safety

Codex CLI has sophisticated OS-level sandboxing:

- Three-tier sandbox: macOS (Seatbelt/sandbox-exec), Linux (bubblewrap + seccomp), Windows (native sandbox).
- Approval policies: on-request, untrusted, never, granular, and automatic approval reviews via guardian agent.
- Automatic reviews check for data exfiltration, credential probing, security weakening, destructive actions. Critical-risk actions denied outright. Timeouts/parse errors fail closed.
- Filesystem profiles deny reads for exact paths/globs.
- Protected paths (.git, .agents, .codex) are read-only even in writable modes.
- Network: default no network. Web search defaults to cached mode (OpenAI-maintained index).

**Key quote:** "Codex security controls come from two layers that work together: Sandbox mode (what Codex can do technically) and Approval policy (when Codex must ask before executing an action)."

### 3.3 State Persistence and Recovery

- Session persistence configurable via history.persistence and history.max_bytes.
- OpenTelemetry export: Opt-in structured events for conversations, API requests, tool approvals.
- Compliance API: Detailed audit logs retained up to 30 days.
- Analytics API: Daily time-series metrics, per-user breakdowns.

### 3.4 Multi-Agent Architecture

- Sub-agents for parallel execution.
- Codex SDK: Programmatic orchestration with MCP server integration.
- App Server: Run Codex as a service.

---

## 4. Comparison Matrix

| Dimension | Claude Code | Codex CLI | Demo-Grade Frameworks |
|---|---|---|---|
| Context Management | Hierarchical CLAUDE.md + auto memory + path-scoped rules | AGENTS.md + config.toml + memories/chronicle | Single-prompt, no cross-session memory |
| Tool Governance | Permission rules + hooks + managed settings | OS sandbox + approval policies + guardian auto-review | None or simple allow/deny |
| State Persistence | Auto memory + session transcripts (30d) | History persistence + OTel + Compliance API | None |
| Safety Model | Permission-first, sandbox complementary | Sandbox-first, defense-in-depth, auto-review | None |
| Enterprise Governance | 5 delivery mechanisms, fail-closed, MDM | Managed config, Compliance API, Analytics API | N/A |
| Multi-Agent | Sub-agents + Agent SDK + MCP | Sub-agents + SDK + MCP Server | Single agent loop |
| Observability | Settings-based telemetry | Full OTel + Analytics + Compliance APIs | None |
| Recovery | /compact survives CLAUDE.md | Configurable history; OTel flush on shutdown | None |
| Open Source | No (MCP is open standard) | Yes (Apache-2.0, 78.5k stars, Rust) | Yes (Apache-2.0) |
| Surface Area | Terminal, VS Code, JetBrains, Desktop, Web, Slack, iOS, CI/CD | Terminal, IDE, Desktop, Web, Slack, GitHub, Linear | Single app |
| Cost Model | Claude subscription or API billing | ChatGPT plan or API key | API key only |

## 5. Production-Grade vs. Demo-Grade: Key Differentiators

### 5.1 Production-Grade (Claude Code, Codex CLI)

1. **Defense-in-depth security:** Multiple independent layers (permissions + sandbox + hooks/guardian). A bypass of one layer is caught by another.
2. **Enterprise governance:** Non-overridable managed settings. MDM deployment, SSO, audit trails, compliance APIs.
3. **Stateful persistence:** Multi-session memory surviving crashes, compaction, and context limits. Inspectable and editable format.
4. **Observability:** Structured telemetry, OTel export, analytics dashboards, per-user tracking.
5. **Recovery mechanisms:** Graceful context window limit handling via compaction; critical context re-injection from disk.
6. **Multi-surface continuity:** Sessions moving between terminal, IDE, web, mobile, CI/CD without state loss.
7. **Configuration layering:** Hierarchical (managed > CLI > local > project > user) with clear precedence.

### 5.2 Demo-Grade (typical community frameworks)

1. **Single-turn or limited context:** No systematic context management. Every session is fresh.
2. **No sandbox or permission system:** Agent runs with user full privileges.
3. **No cross-session memory:** All state is ephemeral.
4. **No observability:** No telemetry, audit trails, or usage analytics.
5. **No recovery:** Context overflow = lost state. No compaction or re-injection.
6. **Single surface:** Streamlit app or basic CLI. No multi-surface continuity.
7. **No configuration layering:** One config file (if any), no hierarchy.

**The dividing line is not features-per-minute but reliability, safety, and operational maturity.** A demo agent can write impressive code in a single session; a production agent does it safely, repeatably, and accountably across hundreds of sessions with dozens of team members.

---

## 6. Harness Engineering Implications

### 6.1 Platform Choice

- **If safety/isolation is paramount** (multi-tenant CI/CD, untrusted code): Codex CLI sandbox-first architecture provides stronger guarantees. OS-level enforcement (Seatbelt, bwrap+seccomp, Windows sandbox) is harder to bypass than permission rules.
- **If context quality and developer ergonomics is paramount** (internal dev tools, pair programming): Claude Code auto memory and hierarchical CLAUDE.md provides richer contextual awareness with less config overhead.
- **Both are production-grade.** The choice depends on which axis (sandbox enforcement vs. context fluidity) aligns with your deployment environment.

### 6.2 Custom Agent Development

- **Claude Agent SDK:** Best for teams that want Claude Code tool ecosystem (MCP, sub-agents) with custom orchestration.
- **OpenAI Codex SDK + Open Source:** Best for teams needing full control (Apache-2.0 license, Rust codebase, modifiable sandbox) willing to invest in integration.
- **Do NOT use demo-grade frameworks** for anything touching production data or with compliance requirements.

### 6.3 Key Architectural Decisions to Steal

1. **Hierarchical configuration layering** (managed > local > project > user) with immutable managed settings for compliance.
2. **Dual-layer safety:** Behavioral (permissions/instructions) + OS-enforced (sandbox). Neither alone is sufficient.
3. **Auto-gathered cross-session memory** that is inspectable, editable, and bounded (first N lines/KB at session start; on-demand for deeper context).
4. **Path-scoped rules** reducing context bloat by loading instructions on demand based on file access patterns.
5. **Fail-closed startup** for enterprise: if managed settings cannot be fetched, agent refuses to start.

---

## 7. Source URLs

| Source | URL |
|---|---|
| Claude Code Overview | https://docs.anthropic.com/en/docs/claude-code/overview |
| Claude Code Settings & Configuration | https://docs.anthropic.com/en/docs/claude-code/settings |
| Claude Code Memory (CLAUDE.md + Auto Memory) | https://docs.anthropic.com/en/docs/claude-code/memory |
| Claude Code Permissions & Governance | https://docs.anthropic.com/en/docs/claude-code/permissions |
| OpenAI Codex CLI (GitHub) | https://github.com/openai/codex |
| OpenAI Codex Developer Docs | https://developers.openai.com/codex |
| Codex Agent Approvals & Security | https://developers.openai.com/codex/agent-approvals-security |
| Codex Enterprise Governance | https://developers.openai.com/codex/enterprise/governance |
| Awesome LLM Apps (demo-grade reference) | https://github.com/Shubhamsaboo/awesome-llm-apps |

---

## 8. Key Quotes

> "Settings rules are enforced by the client regardless of what Claude decides to do. CLAUDE.md instructions shape Claude behavior but are not a hard enforcement layer." -- Anthropic Docs

> "Codex security controls come from two layers that work together: Sandbox mode (what Codex can do technically) and Approval policy (when Codex must ask you before it executes an action)." -- OpenAI Codex Docs

> "Permission deny rules block Claude from even attempting to access restricted resources. Sandbox restrictions prevent Bash commands from reaching resources outside defined boundaries, even if a prompt injection bypasses Claude decision-making." -- Anthropic Docs

> "The first 200 lines of MEMORY.md, or the first 25KB, whichever comes first, are loaded at the start of every conversation. Content beyond that threshold is not loaded at session start." -- Anthropic Docs

> "The reviewer policy checks for data exfiltration, credential probing, persistent security weakening, and destructive actions. Low-risk and medium-risk actions can proceed when policy allows them. The policy denies critical-risk actions." -- OpenAI Codex Docs

> "Auto memory files are plain markdown you can edit or delete at any time." -- Anthropic Docs

---

*End of findings. Prepared for use in the effective-unsupervised-ai research project.*
