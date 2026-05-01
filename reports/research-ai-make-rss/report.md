# Comparative Analysis: Building an RSS Reader Using AI Code Agents

## Research Question
尋找讓Code Agent根據需求文件製作RSS閱讀器的參考範例
(Find reference examples of making Code Agents build an RSS reader based on requirement documents.)

---

## 1. Executive Summary

There are **three viable approaches** for using AI Code Agents to build an RSS reader from requirement documents, depending on complexity and deployment target:

| Approach | Best For | Time to MVP | AI Tool |
|----------|----------|-------------|---------|
| **Single-page client-side prototype** | Rapid prototyping, demo, personal use | 5-30 min | Claude Artifacts |
| **Full-stack web application** | Production-ready, multi-user, scalable | 2-8 hours | Claude Code |
| **Enterprise-grade with migrations** | Complex requirements, large teams | Days | Devin |

The most practical path for most developers is **Claude Code with the Specification Interview pattern**, using open-source RSS readers (Miniflux, FreshRSS, Folo) as reference architectures.

---

## 2. Agent Comparison

| Criteria | Claude Code | Claude Artifacts | Devin | GitHub Copilot Agent |
|----------|-------------|-----------------|-------|---------------------|
| **Full-stack capability** | ✅ Yes (backend+frontend) | ❌ Client-side only | ✅ Yes | ✅ Yes (agent mode) |
| **Multi-file generation** | ✅ Yes | ❌ Single file | ✅ Yes | ✅ Yes |
| **Codebase awareness** | ✅ Reads whole project | ❌ None | ✅ Yes | ✅ Repo-aware |
| **Autonomous execution** | ✅ Run commands, tests | ❌ Manual copy-paste | ✅ Fully autonomous | ✅ Background tasks |
| **RSS reader analog built** | ✅ Documented (full apps) | ✅ Jina Reader Tool (direct analog) | ✅ Nubank case study | ⚠️ Less documented |
| **Time to working app** | Hours | Minutes | Days | Hours |
| **Best prompt pattern** | Spec Interview → Plan → Implement | "Build an artifact that [fetches/shows X]" | Structured requirements → fine-tune | Assign task + reference docs |

### Key Evidence

**Claude Artifacts** (Simon Willison, 2024): Built 14 interactive web apps in one week, each taking 5-21 minutes. The **Jina Reader Tool** (URL-to-Markdown converter) is a direct architectural analog to an RSS reader: it fetches external content, transforms it, and displays it in a UI. Source: https://simonwillison.net/2024/Oct/21/claude-artifacts/

**Claude Code**: Documented as capable of generating full-stack apps from plain language, with sub-agents for parallel work and Plan Mode for requirements-first workflow. Best practices include the Specification Interview pattern where Claude asks detailed questions and produces a SPEC.md before implementation. Source: https://docs.anthropic.com/en/docs/claude-code/overview

**Devin at Nubank**: 8-12x engineering efficiency gain on 6M+ line migration, 20x cost savings. Demonstrates that even complex enterprise requirements can be converted to working code. Source: https://www.devin.ai/

---

## 3. Reference Open-Source RSS Reader Architectures

The most instructive projects to use as reference when prompting an AI agent:

| Project | Stars | Language | Architecture Highlights |
|---------|-------|----------|------------------------|
| **Miniflux** | 9.1k | Go | Minimalist, single binary, PostgreSQL, internal scheduler, Fever/Google Reader API |
| **FreshRSS** | 14.9k | PHP | Multi-user, SQLite/MySQL/PostgreSQL, extensions system, WebSub support, cron-based |
| **Folo (Follow)** | 38.2k | TypeScript | AI-powered, monorepo, multi-platform, Drizzle ORM, modern stack |
| **Newsboat** | 3.8k | C++/Rust | TUI client, SQLite, macro system, terminal-based |
| **NetNewsWire** | 10k | Swift | Native macOS/iOS, iCloud sync, Feedly sync |

### Common Data Flow
```
[Feed Sources] → [HTTP Fetcher (respects If-Modified-Since/ETag)] → [Feed Parser] → [SQL Storage] → [API/UI]
                                        ↕
                             [Background Scheduler]
```

### Standard Data Models
- **Feed**: id, url, title, site_url, description, icon_url, last_fetched_at, error_count
- **Entry**: id, feed_id (FK), guid, url, title, content, summary, author, published_at, is_read, is_starred
- **Category**: id, user_id, title
- **Subscription**: user_id, feed_id, category_id
- **User**: id, username, password_hash, email, theme

Source: https://github.com/miniflux/v2, https://github.com/FreshRSS/FreshRSS, https://github.com/RSSNext/Folo

---

## 4. Recommended Workflow: Requirements → RSS Reader with Claude Code

### Phase 1: Write AI-Friendly Requirements
Structure the requirements document using XML tags (proven technique from Anthropic's docs):

```xml
<requirements>
  <project_overview>
    A self-hosted RSS reader web application with user authentication,
    feed management, and article viewing.
  </project_overview>
  <tech_stack>
    Backend: Python + FastAPI, Database: SQLite, Frontend: Vanilla JS + HTML
  </tech_stack>
  <features>
    <feature priority="high">
      <name>Feed Subscription</name>
      <description>Users can add RSS/Atom feeds by URL</description>
      <acceptance_criteria>
        - User can paste a feed URL and subscribe
        - System fetches and parses the feed
        - Duplicate URLs are rejected
        - OPML import/export supported
      </acceptance_criteria>
    </feature>
    ...
  </features>
  <data_models>
    <model name="Feed">...</model>
    <model name="Entry">...</model>
  </data_models>
</requirements>
```

### Phase 2: Specification Interview
Run Claude Code and use the Spec Interview pattern:
```
I want to build an RSS reader based on the attached requirements document.
Interview me in detail using the AskUserQuestion tool about architecture,
data model, UI, edge cases, and tradeoffs.
After interviewing, produce a complete SPEC.md file.
```
Source: https://docs.anthropic.com/en/docs/claude-code/best-practices

### Phase 3: Implement with Reference Architecture
In a fresh session with SPEC.md, use a prompt that references the Miniflux architecture:
```
Using SPEC.md as the requirements, implement the RSS reader.
Reference the Miniflux architecture pattern:
- Internal scheduler for feed polling
- Respect HTTP caching headers (If-Modified-Since, ETag)
- Three-panel UI (feeds → entries → article)
- SQL database for storage
```

### Phase 4: Iterative Validation
- Generate tests from acceptance criteria **before** implementation code
- After each feature: lint → type check → unit tests → integration tests → build
- Use sub-agents for parallel work (parser + UI simultaneously)

Source: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-prompting-best-practices

---

## 5. Prompt Templates for Each Phase

### Requirements Document Analysis
```
Read the attached requirements document. For each requirement:
1. Identify which files would need to be created/modified
2. Note any ambiguities or missing details
3. Suggest specific implementation approaches
Place your analysis in <analysis> tags.
```

### Architecture Generation
```
Based on the requirements document, design an architecture for an RSS reader.
Follow the standard RSS reader patterns:
- Scheduler-based feed polling
- Feed fetcher with HTTP cache respect
- Feed parser (RSS/Atom/JSON Feed)
- Content extractor (Readability-style)
- SQL database storage
- REST API layer
- Three-panel web UI

Output: directory structure, data models, data flow, API endpoints.
```

### Code Generation with Reference
```
Look at how [Miniflux/FreshRSS/Folo] implements [feed parsing/subscription management/UI].
Follow the same pattern to implement [FEATURE] in our project.
Adapt the approach to our tech stack: [TECH_STACK].
```

### Self-Review
```
Review the code you just generated against the requirements document.
For each requirement, state: ✅ implemented, ⚠️ partial, ❌ missing.
List specific file names and line numbers for any issues.
Then produce a refined version addressing each issue.
```

---

## 6. Key Recommendations

1. **Start with Claude Code** — best balance of autonomy, codebase understanding, and tool integration for this task
2. **Use the Specification Interview** — let the AI produce the spec by asking you questions; it surfaces edge cases you haven't considered
3. **Reference Miniflux architecture** — it's the cleanest, most minimal reference implementation (Go, single binary, PostgreSQL)
4. **Write tests first** — TDD with AI produces more reliable code; generate tests from acceptance criteria before implementation
5. **Develop incrementally** — parser → storage → scheduler → API → UI, validating each layer before moving on
6. **For a quick prototype** — use Claude Artifacts to build a single-page RSS reader in under 30 minutes (see Simon Willison's Jina Reader Tool as a direct analog)

---

## 7. Source URLs

| Resource | URL |
|----------|-----|
| Claude Code Overview | https://docs.anthropic.com/en/docs/claude-code/overview |
| Claude Code Best Practices | https://docs.anthropic.com/en/docs/claude-code/best-practices |
| Simon Willison — Claude Artifacts (14 apps in 1 week) | https://simonwillison.net/2024/Oct/21/claude-artifacts/ |
| Simon Willison — Using LLMs for Code | https://simonwillison.net/2024/Sep/20/using-llms-for-code/ |
| Anthropic Prompt Engineering Best Practices | https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-prompting-best-practices |
| GitHub Copilot Features | https://github.com/features/copilot |
| Devin AI (Cognition Labs) | https://www.devin.ai/ |
| DAIR.AI Prompt Engineering Guide | https://www.promptingguide.ai/techniques |
| Miniflux (Go RSS Reader) | https://github.com/miniflux/v2 |
| FreshRSS (PHP RSS Reader) | https://github.com/FreshRSS/FreshRSS |
| Folo/Follow (TypeScript RSS Reader) | https://github.com/RSSNext/Folo |
| Newsboat (TUI RSS Reader) | https://github.com/newsboat/newsboat |
| NetNewsWire (macOS/iOS RSS Reader) | https://github.com/Ranchero-Software/NetNewsWire |
| Stringer (Ruby RSS Reader) | https://github.com/stringer-rss/stringer |
| GitHub Spark | https://github.com/features/spark |
