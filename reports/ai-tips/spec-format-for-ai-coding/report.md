# Spec/Test Input Formats for AI Coding Agents — Research Report

## Executive Summary

Based on research across industry practices (GitHub Spec Kit, Anthropic Claude Code, Cursor, Devin), academic literature (Design by Contract, Specification-Driven Development), and practical tools (Gherkin/Cucumber, TLA+, Alloy), the most suitable spec format for AI coding agents is a **layered, hybrid approach** combining:

1. **Persistent project context** (CLAUDE.md / AGENTS.md) — always-loaded rules and conventions
2. **Structured behavioral specs** (Markdown with XML/section conventions) — task-specific requirements
3. **Executable tests** as verifiable ground truth — written before implementation

---

## Recommendation: Layered Spec Architecture

```
┌─────────────────────────────────────────────┐
│  Layer 1: Project Context (persistent)      │
│  ─ CLAUDE.md / AGENTS.md / .cursorrules     │
│  ─ Coding standards, architecture, libs     │
│  ─ Loaded every session                     │
├─────────────────────────────────────────────┤
│  Layer 2: Task Spec (per feature)           │
│  ─ structured Markdown (spec.md)            │
│  ─ User journeys, acceptance criteria       │
│  ─ XML tags: <context>, <instructions>      │
│  ─ Error handling, edge cases               │
├─────────────────────────────────────────────┤
│  Layer 3: Executable Specs (verification)   │
│  ─ Unit tests (Jest, pytest, etc.)          │
│  ─ Gherkin scenarios (Given-When-Then)      │
│  ─ tests.json tracking pass/fail state      │
└─────────────────────────────────────────────┘
```

---

## Why This Works

### Layer 1: Persistent Context
- **Pattern**: `CLAUDE.md` (Anthropic), `AGENTS.md` (OpenCode), `.cursorrules` (Cursor)
- **Purpose**: Ground every AI session in project norms without repeating instructions
- **Content**: Coding standards, preferred libraries, architecture decisions, review checklists
- **Guideline**: Keep as small as possible — too much context degrades agent performance (Thoughtworks)

### Layer 2: Structured Spec
- **Pattern**: GitHub Spec Kit's 4-phase process (Specify → Plan → Tasks → Implement)
- **Content**: Functional requirements, user journeys, data models, error handling
- **Formatting**: Sequential steps, XML tags for sections, examples covering edge cases
- **Placement**: Documents at top, query/instructions at bottom (improves accuracy ~30%, Anthropic)

### Layer 3: Executable Tests
- **Pattern**: Write tests before code, track in `tests.json`
- **Purpose**: Binary pass/fail verification — the most reliable spec because it's deterministic
- **Benefits**: Used by SWE-bench, Devin's evaluation pipeline, Claude Code multi-window workflow
- **Guideline**: Each task should be independently testable (GitHub Spec Kit)

---

## Format Comparison

| Format | Layer | Ambiguity | Executable | Learning Curve | Best For |
|--------|-------|-----------|------------|----------------|----------|
| CLAUDE.md / AGENTS.md | 1 | Low | No | Low | Project conventions |
| Structured Markdown | 2 | Medium | No | Low | Feature specs, PRDs |
| Gherkin (Given-When-Then) | 2+3 | Low | Yes (Cucumber) | Low | Behavioral specs |
| Unit Tests (pytest, Jest) | 3 | None | Yes | Medium | Verification, contracts |
| Design by Contract | 2+3 | Very low | Partial | High | Safety-critical |
| TLA+ / Alloy | 2+3 | None | Yes (model-checked) | Very high | Distributed systems |
| Free-form prompt | None | High | No | None | Exploration only |

---

## Recommended Spec File Structure

```
project/
├── AGENTS.md              # Layer 1: Persistent project context
├── specs/
│   ├── feature-auth/
│   │   ├── spec.md        # Layer 2: Behavioral spec
│   │   ├── plan.md        # Tech design, architecture
│   │   └── tasks.md       # Decomposed, testable tasks
│   └── ...
├── tests/
│   ├── tests.json          # Layer 3: Test state tracking
│   └── test_auth.py        # Executable tests written before code
└── ...
```

---

## Key Practices for Stable Implementation

1. **Write tests first** — Tests are the most reliable spec format; they provide deterministic pass/fail
2. **Use sequential, numbered steps** — Not paragraphs; AI performs better with explicit ordering
3. **Include edge cases in examples** — Cover diverse scenarios; ask AI to generate additional edge cases
4. **Separate memory from specs** — Always-loaded context vs task-specific artifacts
5. **Each task must be independently testable** — Enables TDD-like feedback for AI
6. **Match detail level to complexity** — Over-specifying small tasks wastes tokens; under-specifying large tasks causes hallucinations
7. **Put long documents first, instructions last** — Improves accuracy by ~30%
8. **Use XML/section tags** — `<context>`, `<instructions>`, `<examples>` for unambiguous parsing
9. **Track test state** — `tests.json` structured format preserves state across sessions
10. **Iterate spec before code** — Catching spec errors is cheaper than fixing generated code

---

## Key Industry Quotes

> "We're moving from 'code is the source of truth' to 'intent is the source of truth.' With AI, the specification becomes the source of truth and determines what gets built." — GitHub Spec Kit

> "Think of Claude as a brilliant but new employee who lacks context on your norms and workflows." — Anthropic Prompting Guide

> "Context engineering is curating what the model sees so that you get a better result." — Birgitta Böckeler, Thoughtworks

> "Show your prompt to a colleague with minimal context on the task and ask them to follow it. If they'd be confused, Claude will be too." — Anthropic

---

## Sources
- https://cucumber.io/docs/gherkin/reference/
- https://specstory.com/
- https://github.blog/engineering/devops/spec-driven-development-with-ai/
- https://martinfowler.com/articles/context-engineering.html
- https://martinfowler.com/articles/spec-driven-development.html
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
- https://docs.anthropic.com/en/docs/claude-code/overview
- https://cognition.ai/blog/evaluating-coding-agents
- https://www.cursor.com/features
- https://en.wikipedia.org/wiki/TLA%2B
- https://alloytools.org/about.html
- https://doi.org/10.1007/978-3-540-24853-8_12 (Ostroff et al., 2004)
- https://doi.org/10.1016/j.infsof.2020.106503 (Liu et al., 2021)
