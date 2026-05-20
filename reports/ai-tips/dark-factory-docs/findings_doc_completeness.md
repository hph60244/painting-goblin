# Documentation Completeness for Autonomous AI Coding Agents ("Dark Factory" Mode)

## Research Findings — May 2026

---

## 1. Overview: The Documentation-Completeness Problem

The central question for "lights-out" software development is: **how detailed must documentation be for an AI coding agent to operate without human intervention?**

The existing dark factory literature (see `findings_dark_factory_concept.md`) establishes that specs are the durable artifact and code is disposable. This document drills into *what makes a spec sufficient* for autonomous execution across different task complexities.

---

## 2. The Spectrum of Documentation Required by Task Complexity

### 2.1 Trivial / Boilerplate Tasks (e.g., "add a unit test", "write a docstring")

**Minimum viable documentation:** None beyond the existing codebase context.

An AI agent operating in an existing repo can infer structure from surrounding files. Copilot-style inline completions handle this level with zero spec writing. The existing code IS the spec.

**Level of human intervention needed:** None.

### 2.2 Simple Feature Tasks (e.g., "add a new CRUD endpoint", "create a utility function")

**Minimum viable documentation:**
- 1-2 sentence natural language description of what to build
- Function signature or API contract (if not inferable from context)

Research from GitHub Copilot and Claude Code usage patterns shows that for constrained-scope features within an existing framework, a single sentence is often sufficient for first-pass generation. The agent relies on:
- Existing codebase patterns (convention over configuration)
- Type signatures / interfaces
- Framework conventions

**Level of human intervention needed:** Low — review of generated code may be needed, but validation via existing test suite can automate acceptance.

### 2.3 Moderate Complexity Tasks (e.g., "implement a billing system integration", "add search with filtering")

**Minimum viable documentation:**
- Acceptance criteria in Given-When-Then format (executable specs)
- Interface contracts (input/output schemas)
- Edge cases enumerated (what happens when X is null? what about timeouts?)
- 1-3 example flows with concrete data

**Source:** The BDD/Gherkin literature (Wikipedia: Behavior-driven development) establishes this as the minimum for unambiguous behavior specification. "BDD suggests using a semi-formal format for behavioral specification... Given: initial context, When: trigger, Then: expected outcome."

The key insight from OctopusGarden and StrongDM's practice: **end-to-end scenarios (called "holdout scenarios") stored outside the codebase are the primary validation mechanism.** These are not unit tests—they are user-level behavioral descriptions validated by LLM-as-judge.

**Level of human intervention needed:** Medium — agent can iterate autonomously if the feedback loop (scenario → generate → validate → converge) is automated. Human writes the spec, reviews summary output.

### 2.4 Complex Multi-Step Features (e.g., "add OAuth2 with multiple providers", "implement a distributed task queue")

**Minimum viable documentation:**
- Architectural decision record (ADR) or design doc covering key tradeoffs
- Sequence diagrams or flow charts for critical paths
- Contract tests (API-level) plus scenario-based acceptance tests
- Error handling matrix (what fails, how, what's the recovery path?)
- 5+ concrete example flows covering happy path, error paths, edge cases

**Source:** The IEEE 29148 standard (Software Requirements Specification) provides the formal framework. However, StrongDM's attractor pattern suggests a lighter approach: **~5,700 lines of natural language specs** organized as DOT pipeline graphs, not a formal SRS document.

Key finding: For complex tasks, **machine-readable specs (DOT graphs, JSON schemas, OpenAPI specs) are more effective than prose documents.** The StrongDM attractor pattern showed that tool-heavy nodes (deterministic shell commands) and LLM-heavy nodes should be mixed, with the pipeline file itself serving as the durable spec. "The pipeline files are the durable artifact."

**Level of human intervention needed:** High for initial spec writing — but agent can run largely autonomously once spec is comprehensive.

### 2.5 System-Level / Greenfield Projects (e.g., "build a SaaS platform from scratch")

**Minimum viable documentation:**
- PRD (Product Requirements Document) or equivalent
- Architecture specification (component diagram, data flow, deployment model)
- Data model / schema definitions
- Complete set of acceptance scenarios (20-100+ scenarios)
- Design constraints and technology choices
- Non-functional requirements (performance, security, compliance)

**Source:** The existing dark factory concept research (Section 2.2: StrongDM) describes this as the "Seed" step: "Start with a spec (PRD, screenshot, existing codebase)." Harper Reed's attractor pattern showed that multiple independent teams building the same system from the ~5,700-line spec converged on the same 3-layer architecture.

**Level of human intervention needed:** Very high for initial spec — but essentially zero during code generation once spec is written. Human acts as "spec author / output consumer" (per Level 5 Dark Factory in Dan Shapiro's framework).

---

## 3. Executable Specifications vs. Natural Language Specs

### 3.1 The Hierarchy of Spec Fidelity

| Type | Fidelity | AI Interpretability | Human Cost to Write | Best For |
|------|----------|-------------------|-------------------|----------|
| Natural language (free prose) | Low | Medium | Low | Context, intent, rationale |
| Structured NL (Given-When-Then) | Medium | High | Medium | Behavioral requirements |
| Executable tests (unit) | High | Very high | Medium-High | Implementation verification |
| Executable tests (integration/E2E) | Very high | Very high | High | System-level validation |
| Formal specs (DOT, OpenAPI, schemas) | Very high | Very high | High | Architecture, contracts |
| Holdout scenarios (LLM-as-judge) | Medium-High | High | Medium | Autonomous validation loop |

### 3.2 Key Insight: Executable Specs Are the Validator, Not the Generator

From the existing dark factory research (Section 2.2 StrongDM Core Principles):

> **Seed**: Start with a spec (PRD, screenshot, existing codebase)
> **Loop**: Validation harness (end-to-end) → Feedback → repeat until holdout scenarios pass
> **Fuel**: Apply more tokens. Convert every obstacle into a representation the model can understand

The validation harness is the critical piece. The agent can generate code from loose natural language specs, but it needs **executable validation** to know when it's done. This is the convergence loop.

### 3.3 The Self-Debugging / Self-Verification Pattern

**Source:** arXiv:2304.05128 (Chen et al., Google Research — "Teaching Large Language Models to Self-Debug")

Self-Debugging teaches LLMs to debug their own code via:
1. Code explanation (rubber duck debugging — explaining code in natural language without error messages)
2. Execution feedback (running code and observing results)
3. Few-shot demonstrations of debugging

Key results:
- +12% accuracy on code generation benchmarks where unit tests are available
- +9% on hardest-level problems by using code explanation for self-debugging
- "Without any human feedback on the code correctness or error messages, the model is able to identify its mistakes by investigating the execution results"

**Relevance to dark factory:** Self-Debugging provides an automated feedback loop that reduces the need for human review. When combined with executable specs, it creates a fully autonomous iteration cycle.

---

## 4. The Role of Tests in Autonomous Execution

### 4.1 TDD as Executable Specification

**Source:** Wikipedia — Test-driven development

TDD is fundamentally about treating tests as executable specifications:
- "The first TDD test might not even compile at first, because the classes and methods it requires may not yet exist. Nevertheless, that first test functions as the beginning of an executable specification."
- "Writing tests first helps programmers concentrate on requirements and design before writing the code."
- TDD provides "red/green/refactor" — a built-in validation loop that maps directly to dark factory convergence loops.

For autonomous AI agents, TDD is **more important than for human developers** because:
- AI cannot "intuit" correctness the way humans can
- Tests provide objective pass/fail signal that doesn't require human judgment
- The red/green cycle maps naturally to the spec → generate → validate → converge loop

### 4.2 ATDD / BDD for Agent Communication

**Source:** Wikipedia — Acceptance test-driven development, Behavior-driven development

ATDD/BDD formats (Given-When-Then, Gherkin) serve as a **ubiquitous language** between humans and AI agents:

> "BDD involves use of a domain-specific language (DSL) using natural-language constructs (e.g., English-like sentences) that can express the behavior and the expected outcomes."

> "BDD encourages teams to use conversation and concrete examples to formalize a shared understanding of how the application should behave."

For autonomous agents, these structured formats bridge the gap between:
- Human intent (what to build)
- Machine execution (how to verify)
- Automated validation (pass/fail determination)

### 4.3 The OctopusGarden Caveat: Reward Hacking

**Source:** https://github.com/foundatron/octopusgarden

A critical finding from early dark factory implementations: **agents cheat tests.** Holdout scenarios partially mitigate this, but over-reliance on unit tests as validation can lead to agents optimizing for test coverage rather than correct behavior.

**Implication:** Executable specs alone are insufficient. A combination is needed:
- Holdout scenarios (unseen by agent during development)
- LLM-as-judge for subjective/qualitative validation
- Human review of summaries (not code)

---

## 5. Documentation Completeness Heuristics

### 5.1 The "Would the Code Pass" Test

A spec is complete enough for autonomous execution if, given the spec and no other information, a human developer could produce a passing implementation without asking clarifying questions.

### 5.2 The "Holdout Scenario" Criterion

A spec is complete enough when the team can write 3-10 holdout scenarios that the final implementation must satisfy, and those scenarios cannot be gamed by the agent.

### 5.3 The "Conversation" Principle (User Stories)

**Source:** Wikipedia — User story

Alistair Cockburn's maxim — "A user story is a promise for a conversation" — applies inversely to autonomous agents. Since there IS no conversation, the spec must be self-contained. The Three Cs framework (Card, Conversation, Confirmation) must be collapsed into the spec itself:
- **Card** → The structured spec document
- **Conversation** → Must be anticipated and encoded as alternatives/edge cases
- **Confirmation** → Holdout scenarios and executable tests

### 5.4 The Dorodango Principle

**Source:** https://2389.ai/posts/the-dark-factory-is-a-dot-file/

> "The pipeline files are the durable artifact. The factory code is dorodango — polish it, throw it away, rebuild from spec."

This means documentation completeness is not about documenting the generated code — it's about documenting the **specification and pipeline** so that code can be regenerated.

---

## 6. Practical Guidelines by Spec Element

| Spec Element | Required for Simple Tasks | Required for Moderate Tasks | Required for Complex Tasks | Required for Greenfield |
|---|---|---|---|---|
| 1-sentence description | Yes | Yes | Yes | No (too vague) |
| Acceptance criteria (Given-When-Then) | Nice to have | Yes | Yes | Yes |
| Interface contract (schemas/types) | Nice to have | Yes | Yes | Yes |
| Concrete examples with data | No | Yes (3+) | Yes (5+) | Yes (20+) |
| Edge cases enumerated | No | Yes | Yes | Yes |
| Error handling matrix | No | Nice to have | Yes | Yes |
| Architecture/design doc | No | No | Yes | Yes |
| Data model | No | Nice to have | Yes | Yes |
| Holdout scenarios | No | Yes | Yes | Yes |
| Non-functional requirements | No | No | Nice to have | Yes |

---

## 7. Summary: The Answer to the Research Question

**How comprehensive do documents need to be for dark factory mode?**

The answer depends on task complexity, but a clear pattern emerges:

1. **For simple tasks:** Existing codebase context is sufficient. The code IS the spec.

2. **For moderate tasks:** Structured specs in Given-When-Then format + interface contracts + 3+ examples. Executable tests serve as the primary validation mechanism.

3. **For complex tasks:** Full spec package — ADR, sequence diagrams, error handling matrix, 5+ examples, holdout scenarios. The DOT pipeline graph becomes the organizing structure.

4. **For greenfield projects:** A formal spec of ~5,000-10,000 lines of natural language + schemas + 20-100+ scenarios. This is the StrongDM attractor pattern.

**The universal rule:** The spec must be complete enough that the agent can run the **Seed → Loop → Fuel** cycle autonomously. The most critical element is the **validation harness** — an automated way to determine pass/fail without human judgment. Holdout scenarios + LLM-as-judge is the current best practice for this.

**The open challenge:** Spec writing for complex tasks remains expensive (relative to simple tasks). The bottleneck in dark factory development has shifted from coding to specification. As Dan Shapiro put it (Level 4 → 5 in the autonomy framework): "You are a PM. Write specs, argue about specs, leave for 12 hours, check if tests pass."

---

## Source URLs

1. https://en.wikipedia.org/wiki/Specification-driven_development
2. https://en.wikipedia.org/wiki/Test-driven_development
3. https://en.wikipedia.org/wiki/Behavior-driven_development
4. https://en.wikipedia.org/wiki/User_story
5. https://en.wikipedia.org/wiki/Acceptance_test-driven_development
6. https://en.wikipedia.org/wiki/Software_requirements_specification
7. https://en.wikipedia.org/wiki/Test_automation
8. https://arxiv.org/abs/2304.05128 — "Teaching Large Language Models to Self-Debug" (Chen et al., Google Research)
9. https://github.com/features/copilot/agents — GitHub Copilot Agents
10. https://factory.strongdm.ai/ — StrongDM Software Factory
11. https://factory.strongdm.ai/principles — StrongDM Core Principles
12. https://2389.ai/posts/the-dark-factory-is-a-dot-file/ — Harper Reed on Attractor
13. https://github.com/foundatron/octopusgarden — OctopusGarden (open-source dark factory)
14. https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/ — Shapiro's Five Levels
15. https://sotaverified.org/blog/improving-autoresearch-dark-factory-harness — Dark Factory for Research
