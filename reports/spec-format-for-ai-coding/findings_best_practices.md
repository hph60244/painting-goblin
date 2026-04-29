# Spec Format for AI Coding: Best Practices Research

## Summary of Sources

1. **Anthropic Prompting Best Practices** — docs.anthropic.com (Claude Opus 4.7, Sonnet 4.6, Haiku 4.5)
2. **Martin Fowler / Thoughtworks: Context Engineering for Coding Agents** (Feb 2026) — martinfowler.com
3. **Martin Fowler / Thoughtworks: Understanding Spec-Driven Development** (Oct 2025) — martinfowler.com
4. **GitHub Blog: Spec-Driven Development with AI / Spec Kit** (Sep 2025) — github.blog
5. **Anthropic: Context Awareness & Multi-Window Workflows** — docs.anthropic.com

---

## 1. Level of Detail That Makes Specs Effective for AI

### Be Clear and Direct (Anthropic)
> "Think of Claude as a brilliant but new employee who lacks context on your norms and workflows. The more precisely you explain what you want, the better the result."
> **Golden rule:** "Show your prompt to a colleague with minimal context on the task and ask them to follow it. If they'd be confused, Claude will be too."

### Provide Sequential Steps
- Use numbered lists or bullet points when order or completeness matters.
- Provide instructions as sequential steps, not paragraphs of prose.

### Be Specific About Output Format
- Specify exact constraints: format, structure, naming conventions.
- Tell the agent **what to do** instead of **what not to do**.
  - Bad: "Do not use markdown"
  - Good: "Your response should be composed of smoothly flowing prose paragraphs."

### Add Context, Not Just Commands
> "Providing context or motivation behind your instructions, such as explaining to Claude *why* such behavior is important, can help Claude better understand your goals."

Example: "Your response will be read aloud by a text-to-speech engine, so never use ellipses since the TTS engine will not know how to pronounce them."

### Use Examples (Few-Shot Prompting)
- 3-5 well-crafted examples dramatically improve accuracy and consistency.
- Make examples: **relevant**, **diverse** (cover edge cases), **structured** (wrap in `<example>` tags).
- Ask Claude to evaluate your examples for relevance/diversity or generate additional ones.

### Right-Size the Detail (Thoughtworks/SDD Article)
> "When I asked Kiro to fix a small bug, it quickly became clear that the workflow was like using a sledgehammer to crack a nut. The requirements document turned this small bug into 4 'user stories' with 16 acceptance criteria."

Key insight: **Match the level of detail to the size/complexity of the task.** Over-specifying small tasks wastes tokens and review time. Under-specifying large tasks leads to hallucinations.

---

## 2. How to Write Unambiguous Specifications

### Structure with XML Tags (Anthropic)
XML tags help Claude parse complex prompts unambiguously:
```xml
<instructions>...</instructions>
<context>...</context>
<input>...</input>
<documents>
  <document index="1">
    <source>filename.txt</source>
    <document_content>{{CONTENT}}</document_content>
  </document>
</documents>
```
- Use consistent, descriptive tag names across all prompts.
- Nest tags when content has a natural hierarchy.

### Long Context Prompting (Anthropic)
- **Put longform data at the top** — documents above the query.
- **Put the query/instructions at the bottom** — can improve response quality by up to 30%.
- **Ground responses in quotes** — ask the agent to quote relevant parts of documents before acting.

### Give the Agent a Role
Even a single sentence makes a difference:
```
You are a senior Python developer specializing in data pipelines.
```

### Separate Spec from Context (Thoughtworks/SDD Article)
- **Memory Bank**: Always-loaded context (rules, architecture, project overview) — `AGENTS.md`, `CLAUDE.md`, `project.md`
- **Specs**: Task-specific artifacts relevant only to the current feature/story
> "These files are relevant across all AI coding sessions, whereas specs are only relevant to the tasks that actually create or change that particular functionality."

### Three Levels of Spec-Driven Development (Thoughtworks)
1. **Spec-first**: Write a spec before coding, use it for the task, discard after.
2. **Spec-anchored**: Keep the spec after completion; evolve it alongside the feature.
3. **Spec-as-source**: The spec is the canonical artifact; humans edit only the spec, code is auto-generated.

### GitHub Spec Kit's Four-Phase Process
1. **Specify** — What and why (user journeys, success criteria, no technical details)
2. **Plan** — Technical details (stack, architecture, constraints)
3. **Tasks** — Break into small, reviewable, independently testable chunks
4. **Implement** — Code generation per task

> "Crucially, your role isn't just to steer. It's to verify. At each phase, you reflect and refine."

---

## 3. Edge Cases and Error Handling in Specs

### Cover Edge Cases in Examples (Anthropic)
- Include diverse examples that explicitly cover edge cases.
- Ask Claude to generate additional edge case examples based on an initial set.

### Defensive Coding Guidance (Anthropic)
To prevent over-engineering while ensuring robustness:
```
- Defensive coding: Don't add error handling, fallbacks, or validation for scenarios that can't happen. Trust internal code and framework guarantees. Only validate at system boundaries (user input, external APIs).
```

### Explicit Error Handling in Specs (Thoughtworks/SDD Article)
The Kiro design document included an explicit "Error Handling" section alongside Data Flow, Data Models, Testing Strategy. **Each spec section should map to specific code concerns** including error paths.

### Research Step for Edge Cases (GitHub Spec Kit)
Spec Kit includes a research step during planning that investigates existing code to understand edge cases before writing implementation tasks. The agent should:
1. Research existing code for similar patterns and their edge cases.
2. Document found edge cases in the spec/plan before implementation.

---

## 4. Relationship Between Spec and Test Cases for AI

### Write Tests Before Code (Anthropic)
> "Ask Claude to create tests before starting work and keep track of them in a structured format (e.g., `tests.json`). This leads to better long-term ability to iterate."

### Tests as a Constraint on Generated Code
> "Remind Claude of the importance of tests: 'It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality.'"

### Multi-Context Window Workflow (Anthropic)
1. Use the first context window to set up a framework (write tests, create setup scripts).
2. Future windows iterate against a todo-list derived from failing tests.
3. Track test state in structured JSON:
```json
{
  "tests": [
    { "id": 1, "name": "authentication_flow", "status": "passing" },
    { "id": 2, "name": "user_management", "status": "failing" }
  ],
  "total": 200, "passing": 150, "failing": 25, "not_started": 25
}
```

### Spec as Source of Truth for Tests (GitHub Spec Kit)
> "Each task should be something you can implement and test in isolation — this is crucial because it gives the coding agent a way to validate its work and stay on track, almost like a test-driven development process for your AI agent."

### Tessl's @test Annotation
Tessl specs include `@test` annotations that tell the framework what tests to generate alongside the implementation code, creating a direct 1:1 mapping between spec clauses and test cases.

---

## 5. Examples of Successful AI Coding Workflows Using Specs

### GitHub Spec Kit Workflow
```
1. /specify "Build a user authentication system with email verification"
2. Review generated spec → refine → /plan "Use Express.js, PostgreSQL, JWT tokens"
3. Review generated plan → refine → /tasks
4. Agent implements tasks one-by-one, developer reviews per task
```

### Claude Code Multi-Window Workflow (Anthropic)
- **Session 1**: Set up test framework and initial tests in `tests.json`.
- **Session 2+**: Start fresh context, read `tests.json` and `progress.txt`, run integration test, implement features.
- **State files**: `tests.json` (structured), `progress.txt` (freeform notes), git log (history).

### Claude Code Context Engineering (Thoughtworks)
- **CLAUDE.md**: Always-loaded project rules ("we use yarn, not npm")
- **Rules**: Path-scoped guidance (`*.sh` → "use ${var} not $var")
- **Skills**: Lazy-loaded instructions for specific domains (React conventions, API integration)
- **Subagents**: Separate contexts for parallel tasks (E2E tests, code review)

### Avoiding Over-Engineering (Anthropic)
```
Avoid over-engineering. Only make changes that are directly requested or clearly necessary:
- Scope: Don't add features beyond what was asked
- Documentation: Don't add docstrings to code you didn't change
- Abstractions: Don't create helpers for one-time operations
```

---

## 6. Anthropic, GitHub, and OpenAI Recommendations for Structuring Specs

### Anthropic's Recommended Spec Structure
1. **System prompt**: Role + context + rules (loaded every session via `CLAUDE.md`)
2. **Documents at top**: Long content first
3. **Query/instructions at bottom**: Task-specific instructions last (improves accuracy by ~30%)
4. **XML tags**: `<instructions>`, `<context>`, `<examples>`, `<input>`
5. **Use `effort` parameter**: `xhigh` for coding/agentic, `high` for intelligence-sensitive
6. **Set `max_tokens` large enough**: Start at 64k tokens for agentic coding

### GitHub Spec Kit's Spec Structure
1. **Constitution** (`constitution.md`): Immutable principles that apply to every change
2. **Spec** (`spec.md`): Functional requirements, user journeys, checklists for completeness
3. **Plan** (`plan.md`): Technical stack, architecture, constraints
4. **Tasks** (`tasks.md`): Actionable, testable chunks with traceability to spec requirements
5. **Templates**: Reusable structures for each artifact type

### Common Pitfalls to Avoid
- **Over-specification** (Thoughtworks): "Are we making something worse in the attempt of making it better?" — the German concept of *Verschlimmbesserung*
- **Reviewing markdown > reviewing code**: Specs generate many files to review; keep scope tight.
- **False sense of control**: "Just because the windows are larger, doesn't mean that AI will properly pick up on everything."
- **Ignoring non-determinism**: "As long as LLMs are involved, we can never be *certain* of anything."
- **CCD vs SDD**: Spec-as-source may repeat the failures of Model-Driven Development (MDD) — inflexibility *and* non-determinism.

### Context Engineering Best Practices (Thoughtworks)
> "Context engineering is curating what the model sees so that you get a better result."

- **Build context files (rules) gradually** — don't pump everything in upfront.
- **Keep context as small as possible** — "An agent's effectiveness goes down when it gets too much context."
- **Use transparency tools** — `Claude Code's /context` command to see what's taking up space.
- **Use Skills for lazy-loading** — only load domain-specific guidance when relevant.
- **Beware of the "illusion of control"** — no amount of context engineering guarantees behavior.

---

## Key Quotes

> "We're moving from 'code is the source of truth' to 'intent is the source of truth.' With AI, the specification becomes the source of truth and determines what gets built." — GitHub Spec Kit announcement

> "This isn't because documentation became more important. It's because AI makes specifications executable." — GitHub Spec Kit announcement

> "We treat coding agents like search engines when we should be treating them more like literal-minded pair programmers." — GitHub Spec Kit announcement

> "Think of Claude as a brilliant but new employee who lacks context on your norms and workflows." — Anthropic Prompting Guide

> "The past has shown that the best way for us to stay in control of what we're building are small, iterative steps." — Birgitta Böckeler, Thoughtworks

> "A spec is a structured, behavior-oriented artifact — or a set of related artifacts — written in natural language that expresses software functionality and serves as guidance to AI coding agents." — Birgitta Böckeler, Thoughtworks
