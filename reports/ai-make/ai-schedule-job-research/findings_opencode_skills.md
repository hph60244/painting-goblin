# AI Skills & Agent Tools for Generating Scheduled Task Configurations from Requirements

**Date:** 2026-05-01
**Researcher:** opencode research agent

---

## 1. Overview: The skills.sh Ecosystem

The [skills.sh](https://skills.sh) platform is an open registry of reusable capabilities ("skills") for AI agents. Skills are installed via `npx skills add <owner/repo> --skill <skill-name>` and act as plugins that inject procedural knowledge (SKILL.md files) into agent prompts.

**Supported agents include:** OpenCode, Claude Code, GitHub Copilot, Cline, Cursor, Codex, Windsurf, Gemini, Goose, and 20+ others.

Skills are ranked by weekly installs via anonymous CLI telemetry. All skill definitions live in public GitHub repositories as SKILL.md files.

---

## 2. Key Skills for Implementation Plan Generation

### 2.1 `create-implementation-plan` by github/awesome-copilot

- **URL:** https://skills.sh/github/awesome-copilot/create-implementation-plan
- **Weekly Installs:** 9.7K
- **Repo:** https://github.com/github/awesome-copilot (31.8K stars)
- **Summary:** Creates structured, machine-readable implementation plans for features, refactoring, upgrades, and infrastructure changes.

**Key facts:**
- Generates **deterministic, AI-executable plans** with discrete phases, atomic tasks, and explicit completion criteria
- Enforces strict template compliance with standardized identifier prefixes: `REQ-`, `TASK-`, `GOAL-`, `SEC-`, `CON-`, `GUD-`, `PAT-`, `ALT-`, `DEP-`, `FILE-`, `TEST-`, `RISK-`, `ASSUMPTION-`
- Plans saved in `/plan/` directory using naming convention: `[purpose]-[component]-[version].md` where purpose is one of: `upgrade|refactor|feature|data|infrastructure|process|architecture|design`
- Mandatory template sections: Requirements & Constraints, Implementation Steps (with phases), Alternatives, Dependencies, Files, Testing, Risks & Assumptions, Related Specifications
- Front matter includes: `goal`, `version`, `date_created`, `last_updated`, `owner`, `status` (Completed/In progress/Planned/Deprecated/On Hold with color-coded badges), `tags`
- Each phase has measurable completion criteria; tasks within phases are executable in parallel unless dependencies are specified
- **"All task descriptions must include specific file paths, function names, and exact implementation details"**

### 2.2 `writing-plans` by obra/superpowers

- **URL:** https://skills.sh/obra/superpowers/writing-plans
- **Weekly Installs:** 76.3K
- **Repo:** https://github.com/obra/superpowers (174.5K stars)
- **Summary:** Comprehensive implementation plans for multi-step tasks, breaking down specs into bite-sized, testable steps.

**Key facts:**
- Decomposes requirements into focused tasks (2–5 minutes each) following TDD cycle: write failing test, verify failure, implement, verify pass, commit
- Maps file structure upfront with clear boundaries; each file has one purpose; files that change together stay together
- Includes exact file paths, **complete code samples** (no placeholders), and specific commands with expected outputs for each step
- Requires plan review via subagent before execution
- Two execution modes: subagent-driven (fresh agent per task) or inline batch execution
- Plans saved to `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`
- Task structure: each step is one action — write test, run to confirm failure, implement, run to confirm pass, commit
- **Strict "No Placeholders" policy:** no TBD, TODO, "add appropriate error handling", "similar to Task N", etc.

**Direct quote from SKILL.md:**
> "Every step must contain the actual content an engineer needs. These are plan failures — never write them: 'TBD', 'TODO', 'implement later', 'fill in details'..."

### 2.3 `executing-plans` by obra/superpowers

- **URL:** https://skills.sh/obra/superpowers/executing-plans
- **Weekly Installs:** 61.8K
- **Summary:** Execute a written implementation plan with critical review and task checkpoints.

**Key facts:**
- Loads plan, reviews critically (raises concerns before starting), then executes tasks sequentially
- Marks progress, runs verifications as specified in the plan
- Stops immediately on blockers (missing dependencies, test failures, unclear instructions) — does not guess
- Integrates with git-worktrees for isolated workspaces
- Requires `finishing-a-development-branch` skill to complete work after all tasks verify
- Works best on platforms with subagent support; recommends `subagent-driven-development` as preferred alternative

---

## 3. Related Ecosystem Skills

From the skills.sh leaderboard, these additional skills form the broader planning/execution ecosystem:

| Skill | Installer | Installs | Purpose |
|-------|-----------|----------|---------|
| `brainstorming` | obra/superpowers | 130.6K | Feature/subproject ideation before planning |
| `skill-creator` | anthropics/skills | 177.5K | Create new skills from scratch |
| `subagent-driven-development` | obra/superpowers | 56.3K | Subagent-per-task execution |
| `test-driven-development` | obra/superpowers | 66.4K | TDD workflow skill |
| `verification-before-completion` | obra/superpowers | 54.4K | Verify work before marking done |
| `finishing-a-development-branch` | obra/superpowers | 48.3K | Finalize branch after plan execution |
| `dispatching-parallel-agents` | obra/superpowers | 50.7K | Parallel task dispatch |
| `using-git-worktrees` | obra/superpowers | 50.4K | Isolated workspace management |
| `writing-skills` | obra/superpowers | 52.5K | Create SKILL.md files for the skills registry |
| `azure-enterprise-infra-planner` | microsoft/azure-skills | 189.8K | Enterprise infrastructure planning |

---

## 4. Gaps & Opportunities: Cron/Schedule Config Generation

**No dedicated skill was found on skills.sh for generating cron/schedule/job configurations from natural language or requirements documents.** The existing skills focus on:
1. **Implementation plans** (code changes across files) — what to build and in what order
2. **Task execution** — carrying out the plan

What is **missing** but could be valuable:
- A skill that reads a requirements document / markdown spec and produces executable job configurations (cron expressions, Windows Task Scheduler XML, `at` commands, systemd timers, CI/CD schedule YAML)
- A skill that understands scheduling semantics (timezone handling, frequency translation from natural language like "every weekday at 3am" to cron syntax, dependency chaining between jobs, retry policies, SLA-driven scheduling)
- Integration between implementation plan phases and scheduled job prerequisites

### Natural Language → Schedule Translation Patterns

The existing `create-implementation-plan` skill demonstrates the right approach: structured template with machine-parseable identifiers, deterministic output, specific file paths. A cron/schedule skill would follow the same pattern but output job configs instead of implementation steps.

---

## 5. How OpenCode Fits In

[OpenCode](https://opencode.ai) is explicitly listed as a supported agent on skills.sh. It is:
- An open-source AI coding agent (140K GitHub stars, 850+ contributors)
- Available as terminal, desktop app (Windows/Mac/Linux), and IDE extension
- Supports GitHub Copilot, ChatGPT Plus/Pro, and 75+ LLM providers via Models.dev
- LSP-enabled with multi-session support

OpenCode can load any skills.sh skill via `npx skills add`, meaning all three planning/execution skills above (`create-implementation-plan`, `writing-plans`, `executing-plans`) can be invoked from within OpenCode sessions.

---

## 6. Source URLs

| Resource | URL |
|----------|-----|
| skills.sh Homepage | https://skills.sh |
| skills.sh Docs | https://skills.sh/docs |
| create-implementation-plan | https://skills.sh/github/awesome-copilot/create-implementation-plan |
| awesome-copilot repo | https://github.com/github/awesome-copilot |
| writing-plans | https://skills.sh/obra/superpowers/writing-plans |
| executing-plans | https://skills.sh/obra/superpowers/executing-plans |
| obra/superpowers repo | https://github.com/obra/superpowers |
| OpenCode | https://opencode.ai |
| OpenCode GitHub | https://github.com/anomalyco/opencode |
