# Research Findings: Programmatic Job Scheduling Systems

**Date**: 2026-05-01
**Researcher**: AI Agent
**Context**: Research for `painting-goblin` project — a filesystem-based task queue system using Publisher-Subscriber pattern, with AI integration via OpenCode CLI.

---

## 1. File-System-Based Task Queue Systems (Closest to painting-goblin)

### Dagu (dagucloud/dagu)
- **Stars**: 3.3k | **URL**: https://github.com/dagucloud/dagu
- **Description**: Self-hosted workflow engine for scripts, cron jobs, containers, and ops automation.
- **Key relevance**: Uses YAML workflow definitions stored on the filesystem (`~/.config/dagu/dags/`). Stores state in local files by default (no database required). Single binary, no infrastructure dependencies.
- **Direct quote**: "Dagu gives teams one place to run, schedule, review, and debug existing ops automation without standing up a database, message broker, or language-specific SDK stack."
- **AI integration**: Includes built-in agent step, harness step (for Claude Code, Codex, Copilot, OpenCode, Pi), and chat step for LLM calls. The README states: "Run AI coding agents and agent CLIs as workflow steps, or use the built-in agent to write, update, debug, and repair workflows."
- **Architecture**: File-backed storage (logs, state, queue). Optional distributed workers with gRPC. Cron scheduling, overlap policies, catch-up scheduling.
- **Parallel to painting-goblin**: Both use local filesystem as the state medium. Dagu YAML files are similar to painting-goblin's todo/doing/done directory structure.

### Cronicle (jhuckaby/Cronicle)
- **Stars**: 5.6k | **URL**: https://github.com/jhuckaby/Cronicle
- **Description**: Multi-server task scheduler and runner with web UI. A "fancy Cron replacement" in Node.js.
- **Key relevance**: Has both scheduled and on-demand jobs. Real-time stats and live log viewer. JSON messaging system for plugins. REST API for scheduling.
- **Quote**: "A multi-server task scheduler and runner, with a web based front-end UI. It handles both scheduled, repeating and on-demand jobs."
- **Note**: Has been superseded by xyOps (https://github.com/pixlcore/xyops).

### BunQueue (egeominotti/bunqueue)
- **Stars**: 436 | **URL**: https://github.com/egeominotti/bunqueue (from topic search)
- **Description**: High-performance job queue for Bun. SQLite persistence, DLQ, cron jobs, S3 backups.
- **Key relevance**: "Built for AI agents and automation." SQLite-backed queue (filesystem-adjacent). Bun runtime.

---

## 2. Dynamic Cron Job Generators / Config-Driven Scheduling

### Kubernetes CronJob
- **URL**: https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/
- **Description**: Native Kubernetes resource for running scheduled tasks. Defined declaratively in YAML.
- **Key relevance**: The defining example of "scheduled tasks defined in config files and auto-deployed." CronJob specs are YAML manifests applied via `kubectl apply`.
- **Pattern**: `apiVersion: batch/v1` + `kind: CronJob` + `spec.schedule: "*/5 * * * *"` — the schedule is embedded in the resource definition.

### robfig/cron (Go library)
- **Stars**: 14.1k | **URL**: https://github.com/robfig/cron
- **Description**: Cron library for Go. De facto standard Go cron implementation.
- **Key relevance**: Enables programmatic creation of cron schedules. V3 added functional options, chain/jobwrapper interceptors, logging interface. Foundation for many higher-level schedulers.

### Apache Airflow
- **Stars**: 45.3k | **URL**: https://github.com/apache/airflow
- **Description**: Platform to programmatically author, schedule, and monitor workflows.
- **Quote**: "When workflows are defined as code, they become more maintainable, versionable, testable, and collaborative."
- **Pattern**: DAGs defined in Python. The scheduler reads DAG definitions from a `dags_folder` on the filesystem and auto-discovers changes. Schedules specified via `@daily`, `@hourly`, cron expressions, or `timedelta`. Closest mainstream parallel to painting-goblin's "drop files in a directory" pattern.

### Prefect
- **Stars**: 22.3k | **URL**: https://github.com/PrefectHQ/prefect
- **Description**: Workflow orchestration framework for Python. Scheduling with cron, intervals, and events.
- **Quote**: "The simplest way to elevate a script into a production workflow."
- **Pattern**: Decorators decorate Python functions as flows/tasks. `flow.serve(name="...", cron="* * * * *")` for scheduling. Supports event-driven triggers.

### Temporal
- **Stars**: 20k | **URL**: https://github.com/temporalio/temporal
- **Description**: Durable execution platform. Workflows that handle intermittent failures and retries automatically.
- **Key relevance**: Distributed cron as a feature topic. Workflows can be scheduled with cron-like expressions. Uses SDKs (Go, Java, Python, TypeScript) for defining workflows programmatically.

---

## 3. Markdown-to-Schedule Converters / Doc-Driven Scheduling

**No dedicated open-source tools found** that convert markdown to cron schedules directly. However, several closely related patterns were identified:

- **Dagu's document feature**: Workflow YAML files can reference Markdown "documents" attached to runs as artifacts (screenshots, reports, markdown files). Not markdown-to-schedule, but markdown-as-schedule-output.
- **Airflow's DAG-as-code**: DAGs are Python code (not markdown), but the Python syntax serves as a human-readable "document" describing the schedule. Airflow also renders DAG code in the UI for human review.
- **AI-Agent-Assisted Scheduling**: Dagu's `harness` step type runs coding agent CLIs (Claude Code, OpenCode, etc.) which can read requirements docs (including markdown) and output YAML workflow definitions. This is the closest existing pattern to "markdown-to-schedule".

**Research gap**: No tool specifically converts natural language markdown schedules (e.g., "run every weekday at 9am and send a report") into cron expressions. This is a potential niche for painting-goblin if it implements LLM-based task parsing from markdown specs.

---

## 4. GitHub Actions (Workflow-as-Code Scheduling)

- **URL**: https://github.com/features/actions
- **Description**: Automate workflows from GitHub events. YAML-defined workflows with cron (`schedule` event).
- **Pattern**: `.github/workflows/*.yml` files auto-discovered by GitHub. Scheduled via `on: schedule: - cron: '0 0 * * *'`.
- **Key relevance**: The most widely used example of "schedule defined in config file, auto-deployed." Filesystem (git repo) as the source of truth for schedules.
- **Related projects**: `tiennm99/claude-code-routine-trigger` (0 stars) — "Scheduled GitHub Actions workflow that fires a Claude Code routine on a customizable cron" — AI agent triggered by cron config.

---

## 5. Config-Driven Webhook Scheduling (adnanh/webhook)

- **Stars**: 11.8k | **URL**: https://github.com/adnanh/webhook
- **Description**: Lightweight incoming webhook server to run shell commands.
- **Pattern**: Hooks defined in `hooks.json` or `hooks.yaml`. HTTP endpoints trigger command execution. Config files support JSON, YAML, and Go templates.
- **Key relevance**: Demonstrates the "config file drives execution" pattern. Templates enable dynamic config generation. Hot-reload of config files.

---

## 6. AI Agent + Scheduling Patterns

### Dagu Harness Step
- Dagu's `harness` step type directly runs AI coding agent CLIs. It treats the AI agent as a workflow step whose output (YAML, scripts, configs) feeds into subsequent steps.
- **Workflow**: Agent reads requirements doc → Agent outputs workflow YAML → Dagu schedules and executes it.
- **Relevance to painting-goblin**: Validates the pattern of "AI agent reads a requirements document and outputs scheduling configs."

### Claude Code Routine Trigger
- **URL**: https://github.com/topics/cron-scheduler (from topic search)
- **Pattern**: GitHub Actions scheduled workflow fires Claude Code at cron intervals. AI agent runs on a schedule defined by a cron config.

### General Pattern
The dominant pattern across all researched tools is:
1. **Config-as-code**: Schedule defined in YAML/Python/JSON on the filesystem
2. **Auto-discovery**: Scheduler watches a directory or git repo for changes
3. **Declarative scheduling**: The *what* and *when* are co-located in the same file
4. **AI integration tier**: Newer tools (Dagu, BunQueue) explicitly build AI agent steps into the workflow engine

---

## Comparison to painting-goblin

| Feature | painting-goblin | Dagu | Airflow | CronJob (K8s) |
|---|---|---|---|---|
| Filesystem-driven | Yes (todo/doing/done dirs) | Yes (~/.dagu/dags/) | Yes (dags_folder/) | No (kubectl apply) |
| No DB required | Yes | Yes (default) | No (needs PostgreSQL) | Yes (etcd optional) |
| Cron scheduling | Via subscriber | Built-in cron | Built-in scheduler | Native CronJob |
| AI agent integration | Via OpenCode CLI | Harness/agent steps | External only | No |
| Language | Python | Go/Go embedded | Python | YAML/any |
| Task queue | File-based | File-based + optional distributed | Celery/RDBMS | Pod-based |
| Document artifacts | Not yet | Yes (Markdown reports) | Yes (XCom/logs) | Logs only |

## Key Takeaways for painting-goblin

1. **Dagu is the closest existing system**: Same filesystem-first philosophy, same AI agent integration goals. painting-goblin's niche advantage is its extreme simplicity (no binary, just Python + directory watching).

2. **Markdown-to-schedule is unfilled**: No tool cleanly converts natural language markdown scheduling specs into cron jobs. This is a greenfield opportunity.

3. **Filesystem-as-queue is validated**: Both Dagu and painting-goblin prove that file-backed queues are viable for lightweight task scheduling, especially when combined with AI agents.

4. **AI agent as workflow step**: Dagu's harness/agent steps validate that treating AI coding agents as composable workflow steps (read doc → generate config → deploy schedule) is an emerging pattern with growing adoption.

5. **Config auto-discovery**: The most ergonomic schedulers (Airflow, Dagu, GitHub Actions) all auto-discover config files from a watched directory. painting-goblin's todo/doing/done directory structure is a variant of this pattern.
