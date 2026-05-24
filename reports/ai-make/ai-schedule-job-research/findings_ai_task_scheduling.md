# AI Agent Task Scheduling Research

> How AI coding agents (Claude Code, OpenCode, GitHub Copilot, GPT) can read requirement documents and automatically generate task/job schedules, cron jobs, or workflow definitions.

**Date:** 2026-05-01
**Researcher:** OpenCode Agent (research via web)

---

## 1. Overview of the Landscape

AI coding agents are increasingly capable of reading natural-language requirement documents and translating them into executable schedule/workflow definitions. The key patterns fall into three categories:

| Pattern | Example | How It Works |
|---|---|---|
| **File-based job directories + cron-like scheduler** | painting-goblin's `config.ini` + `scheduler.py` | AI writes `.md` job files into a `jobs/` folder; a Python APScheduler daemon copies them into a `todo/` folder on a cron schedule; an executor processes them |
| **Declarative workflow YAML generation** | GitHub Actions, GitLab CI | AI reads requirements, writes `.github/workflows/*.yml` with `schedule:` / `cron:` triggers |
| **Built-in agent scheduling (infra-managed)** | Claude Code Routines | AI defines recurring tasks via `/schedule`; Anthropic-managed infrastructure runs them on cron even when the machine is off |

---

## 2. painting-goblin Project (Your System)

This project is itself a strong reference example of how AI agents can drive job scheduling.

### Architecture

```
config.ini          ← AI-readable cron+param definitions
  [job:print-42]
  schedule = 47 20 12 4 *
  xxx = a, b
  yyy = 12, 34

jobs/               ← AI writes markdown task files here
  print-42.md
  dl-yt-video.md
  research-ai-capability.md
  ...

scheduler.py        ← APScheduler daemon; reads config.ini,
executor.py           copies jobs/ → todo/ on cron, executes via OpenCode CLI
```

**Key insight:** The AI agent (OpenCode) writes human-readable `.md` task definitions into `jobs/`. The `config.ini` [job:] sections define when each job runs (cron) and what parameters to pass. The scheduler copies parameterized variants into `todo/`. The executor spawns OpenCode CLI to run each task autonomously.

Source: `C:\Users\fnaith\Documents\Fork\painting-goblin`

---

## 3. Claude Code / Anthropic — Routines & Scheduled Tasks

Claude Code (from Anthropic) is the closest commercial analog. Key features from docs.anthropic.com:

### Routines (Anthropic-Managed)
> *"Run Claude on a schedule to automate work that repeats: morning PR reviews, overnight CI failure analysis, weekly dependency audits, or syncing docs after PRs merge."*
> *"[Routines] run on Anthropic-managed infrastructure, so they keep running even when your computer is off. They can also trigger on API calls or GitHub events. Create them from the web, the Desktop app, or by running `/schedule` in the CLI."*

### Desktop Scheduled Tasks (Local)
> *"[Desktop scheduled tasks] run on your machine, with direct access to your local files and tools"*

### `/loop` (CLI)
> *"`/loop` repeats a prompt within a CLI session for quick polling"*

This demonstrates three tiers: fully-managed cloud scheduling, local machine scheduling, and in-session looping. An AI agent creates these definitions from natural language prompts.

Sources:
- https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview (section "Schedule recurring tasks")
- https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/routines (404 at time of access but referenced in overview)

---

## 4. GitHub Copilot — Agent Mode & GitHub Actions Integration

GitHub Copilot's Agent mode (announced 2025-2026) can autonomously:

- **Read** specification/requirement documents from issues, PRs, and markdown
- **Generate** GitHub Actions workflow YAML files (`.github/workflows/*.yml`) including `schedule:` events with cron syntax
- **Create, commit, and PR** the workflow definitions

From github.com/features/copilot:
> *"Assign tasks to agents like Copilot, Claude by Anthropic, and OpenAI Codex, and let them plan, explore, and execute work autonomously in the background."*

The Agents feature lets you assign a task from a GitHub Issue, and Copilot will propose a multi-file change including workflow YAML that defines scheduled CI/CD jobs.

Sources:
- https://github.com/features/copilot (Agents section)
- https://github.com/features/actions (CI/CD automation with schedule triggers)

---

## 5. OpenCode — Custom Commands & Agent Skills

OpenCode (opencode.ai) provides mechanisms that enable requirement-to-schedule workflows:

### Custom Commands (`/command`)
Users/AI define markdown files in `.opencode/commands/`:
```yaml
---
description: Run tests with coverage
agent: build
model: anthropic/claude-3-5-sonnet-20241022
---
Run the full test suite with coverage report and show any failures.
```

These are reusable task templates. An AI agent can create such files from a requirements doc.

### Agent Skills (`SKILL.md`)
> *"Agent skills let OpenCode discover reusable instructions from your repo or home directory. Skills are loaded on-demand via the native `skill` tool"*

Skills are discovered dynamically — an AI agent reading a requirements document can generate a `SKILL.md` that encapsulate a scheduling pattern.

### Subagents (`@agent`)
The Task tool lets a primary agent spawn subagents for parallel work. A scheduling system could use this to run multiple job definitions concurrently.

Sources:
- https://opencode.ai/docs/commands
- https://opencode.ai/docs/skills
- https://opencode.ai/docs/agents

---

## 6. Generic Patterns: LLMs Parsing Markdown into Cron/Workflow Defs

Across all tools, the common pipeline is:

```
[Requirements Doc (Markdown)]
        │
        ▼
[AI Agent reads + understands]
        │
        ▼
[Generates structured schedule config]
   ├── config.ini [job:] sections (painting-goblin)
   ├── .github/workflows/*.yml (GitHub Actions)
   ├── .opencode/commands/*.md (OpenCode)
   ├── .claude/skills/*/SKILL.md (Claude/OpenCode)
   ├── Cron/Routines definition (Claude Code)
   └── Any DSL: cron expressions, interval, params
```

### Cron Expression Generation
All major AI coding agents can reliably generate 5-field cron expressions from natural language:
- "Run every weekday at 9am" → `0 9 * * 1-5`
- "Run on the 1st of every month at midnight" → `0 0 1 * *`

This is used by painting-goblin's `scheduler.py` which passes the cron expression to `apscheduler.triggers.cron.CronTrigger`.

---

## 7. Key Takeaways for painting-goblin's Design

**The painting-goblin approach is already state-of-the-art** in several respects:

1. **Decoupled job definition (`.md`) from scheduling (`config.ini`)** — This is more flexible than embedding schedules in code or YAML. An AI agent can update job content without touching the schedule, and vice versa.

2. **AI-native format** — Jobs are plain markdown, which AI agents read/write most naturally. Claude Code, OpenCode, and GPT all natively work with `.md` files.

3. **Parameterization** — The `xxx = a, b` + `yyy = 12, 34` pattern generates combinatorial copies (4 variants). This is more sophisticated than any other tool found in research.

4. **APScheduler + cron** — using standard cron expressions means AI agents can easily generate and validate schedules.

**Gaps vs. other tools:**
- Claude Code Routines offer **cloud-managed** scheduling (runs without the host machine). painting-goblin requires the `scheduler.py` process to be running.
- GitHub Actions workflows can trigger on **GitHub events** (push, issue, PR) in addition to cron. painting-goblin is cron-only.
- OpenCode Skills are **auto-discovered** via the `skill` tool. painting-goblin requires explicit `[job:]` sections in config.ini.

**Potential enhancements:**
- Auto-discovery of `jobs/*.md` files (scan directory instead of listing in config.ini)
- Event-based triggers (file change, webhook) in addition to cron
- Inline schedule metadata in `.md` frontmatter (YAML frontmatter with `schedule:` field)

---

## 8. Repository and Tool References

| Tool / Repo | URL | Relevance |
|---|---|---|
| painting-goblin | `C:\Users\fnaith\Documents\Fork\painting-goblin` | Primary reference — config.ini [job:] + scheduler.py + executor.py |
| Claude Code (Anthropic) | https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview | Routines, scheduled tasks, `/schedule` |
| OpenCode | https://opencode.ai/docs/ | Commands, Skills, Agents, Task tool |
| GitHub Copilot | https://github.com/features/copilot | Agent mode, GitHub Actions YAML generation |
| GitHub Actions | https://github.com/features/actions | `schedule:` cron triggers in workflow YAML |
| APScheduler | https://apscheduler.readthedocs.io/ | Python cron scheduler used by painting-goblin |
| Deno Cron | https://deno.com/blog/cron | In-process cron with backoff, no-overlap guarantee |

---

## 9. Conclusion

The pattern of "AI agent reads a requirements document → generates job definitions + cron schedule → scheduler executes tasks on a timer" is well-established across multiple tools (Claude Code, OpenCode, Copilot, painting-goblin).

painting-goblin's design is uniquely powerful in its **markdown-first approach** and **combinatorial parameterization** — features not found in any other researched tool. The closest commercial equivalents are Claude Code Routines (cloud-managed recurring tasks) and GitHub Actions (event + cron triggered workflows), neither of which supports parameterized job variants from markdown files.

The next evolution would be AI-driven **auto-discovery** of job files and **self-healing** schedules (e.g., AI noticing a job consistently fails at 5-minute intervals and proposing a throttle).
