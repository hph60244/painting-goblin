# Research: AI Code Agents Creating Domain-Specific Languages (DSLs) from Requirements

## Overview

This report surveys how modern AI frameworks and research systems enable Code Agents to generate or leverage Domain-Specific Languages (DSLs) from requirement documents. The landscape spans two paradigms: (1) agents that *generate a DSL* as an intermediate representation from natural-language requirements, and (2) agents that *operate within a pre-defined DSL* to produce correct-by-construction outputs.

---

## Key Frameworks, Tools, and Research Systems

### 1. ARC — Agentic Requirement Compilation (arXiv:2602.13723)

**How it works:** ARC ingests multi-modal requirement documents (50–200 scenarios) and compiles them into runnable web systems. The core insight is to use a **multi-modal DSL document** as the bridge between requirements and code. A bidirectional test-driven agentic loop decomposes requirements top-down into verifiable interfaces, then agents generate code bottom-up to satisfy those tests.

**DSL role:** The DSL document captures UI layouts, API contracts, and database schemas. ARC generates not just source code but also modular designs, enriched test suites, and full traceability across requirements-design-code.

**Key result:** 50.6% more GUI tests passed vs. SOTA baselines. Novice users authored DSL documents for a 10K-line ticket-booking system in ~5.6 hours.

**URL:** https://arxiv.org/abs/2602.13723

---

### 2. HAVEN — Hybrid Automated Verification Engine (arXiv:2604.27643)

**How it works:** HAVEN uses LLM agents to analyze hardware design specifications and produce structured architectural plans. Instead of generating HDL code directly, it introduces a **Protocol-Aware Sequence DSL** that decomposes testbench sequences into fine-grained step types. Predefined DSL patterns establish high-coverage sequences without LLM involvement; agents then iteratively improve coverage by composing additional DSL sequences from coverage-gap reports.

**DSL role:** The DSL acts as a safe intermediate representation that prevents LLMs from writing incorrect low-level HDL. A rule-based code generator transforms DSL sequences into correct UVM testbench components via Jinja2 templates.

**Key result:** 100% compilation success, 90.6% code coverage, 87.9% functional coverage across 19 open-source IP designs.

**URL:** https://arxiv.org/abs/2604.27643

---

### 3. ARGUS — Agentic GPU Optimization via Data-Flow Invariants (arXiv:2604.18616)

**How it works:** ARGUS introduces a **tile-based, Pythonic DSL** that exposes hardware instructions and compiler policies while hiding low-level GPU representations. The DSL provides tag functions for symbolic annotations and tag assertions for relational constraints. When violations occur, the compiler returns concrete counterexamples (thread, data element, program point) enabling dense structured feedback.

**DSL role:** The DSL encodes data-flow invariants verified at compile time (abstract interpretation + SMT solving, zero runtime overhead). An in-context RL planner learns to select optimizations and synthesize effective invariants.

**Key result:** Generated kernels achieve 99–104% of hand-optimized assembly throughput; 2–1543× faster than other agentic systems.

**URL:** https://arxiv.org/abs/2604.18616

---

### 4. μCUTLASS — DSL for GPU Kernel Optimization Agents (arXiv:2603.29010)

**How it works:** μCUTLASS provides a **compact DSL** (learnable in-context) that lets LLM agents reason at a higher abstraction level while preserving important optimization levers (kernel configuration, epilogue fusion, multi-stage pipelines). Combined with Speed-of-Light (SOL) guidance using first-principles performance bounds.

**DSL role:** Raising the abstraction level from raw CUDA to a DSL turns a 0.40× regression into a 1.27× speedup (GPT-5-mini). SOL-guided steering raises this to 1.56×. Saves 19–43% of tokens while retaining ≥95% speedup.

**Key result:** Weaker models + DSL outperform stronger baseline agents at lower token cost.

**URL:** https://arxiv.org/abs/2603.29010

---

### 5. AKG Kernel Agent — Multi-Agent Kernel Synthesis (arXiv:2512.23424)

**How it works:** A multi-agent system that automates kernel generation, migration, and performance tuning. Designed to support **multiple DSLs** (Triton, TileLang, CPP, CUDA-C) to target different hardware backends. Modular design allows rapid integration of new DSLs.

**DSL role:** Acts as a hardware abstraction layer — agents generate DSL code, then platform-specific compilers lower it to target hardware. This decouples agent reasoning from hardware details.

**Key result:** 1.46× avg speedup over PyTorch Eager baselines across GPU and NPU backends.

**URL:** https://arxiv.org/abs/2512.23424

---

### 6. GEAK — Generating Efficient AI-centric GPU Kernels (arXiv:2507.23194)

**How it works:** GEAK uses inference-time compute scaling and a Reflexion-style feedback loop to generate performant **Triton DSL** code for AMD GPUs. The DSL (Triton) is a Python-based language for GPU programming that balances performance and ease of coding.

**DSL role:** Triton DSL serves as the target language, providing a structured intermediate representation that agents can reliably generate and compilers can optimize.

**Key result:** Up to 63% correctness and 2.59× execution speedup over baseline prompting approaches.

**URL:** https://arxiv.org/abs/2507.23194

---

### 7. Delta Prover — Custom DSL for Formal Math Proofs (arXiv:2507.15225)

**How it works:** An agent-based framework that orchestrates LLM interaction with the Lean 4 proof environment. The agent uses a **custom DSL built upon Lean 4** for streamlined subproblem management. Combines reflective decomposition and iterative proof repair.

**DSL role:** The DSL bridges general-purpose LLM reasoning and the formal proof environment, handling subproblem decomposition and management that would otherwise be error-prone for raw LLM output.

**Key result:** 95.9% success rate on miniF2F-test benchmark, surpassing all existing approaches including those requiring model specialization.

**URL:** https://arxiv.org/abs/2507.15225

---

### 8. LLM-DSL-Gen (GitHub: SaturnTsen/LLM-DSL-Gen)

**How it works:** An LLM-driven DSL generator for the Lokad domain-specific language. The system uses LLMs to produce DSL code from natural language descriptions, targeting a pre-existing DSL ecosystem (Lokad).

**DSL role:** The LLM generates DSL constructs directly, which are then compiled/executed by the Lokad runtime. This is the most direct example of "DSL from requirements."

**URL:** https://github.com/SaturnTsen/LLM-DSL-Gen

---

### 9. LangGraph (LangChain)

**How it works:** LangGraph is a low-level orchestration framework for building stateful, long-running agents. While not DSL-focused itself, it provides the orchestration substrate that many DSL-using agent systems (like ARC) build upon. Features include durable execution, human-in-the-loop, comprehensive memory, and debugging via LangSmith.

**DSL role:** Enabling infrastructure — agents built on LangGraph can maintain state across multi-step DSL compilation, track requirement-to-DSL traceability, and support human review of generated DSL artifacts.

**URL:** https://docs.langchain.com/oss/python/langgraph/overview

---

## Patterns and Approaches

### Pattern A: DSL as Safe Intermediate Representation
**Example:** HAVEN, ARGUS
The DSL constrains what the LLM can express, preventing incorrect low-level code generation. A rule-based compiler then transforms DSL constructs into correct executable code. This "DSL firewall" pattern is the most reliable approach for correctness-critical domains.

### Pattern B: DSL as Abstraction Layer
**Example:** μCUTLASS, AKG, GEAK
The DSL raises the reasoning level so agents don't waste tokens on low-level details while preserving important optimization levers. Multiple DSL backends allow targeting different hardware without retraining agents.

### Pattern C: DSL as Requirement Document Format
**Example:** ARC
The DSL itself becomes the requirements artifact — authored by humans (potentially non-experts) or generated from natural language. A compilation pipeline transforms DSL documents into full-stack applications with tests and traceability.

### Pattern D: DSL as Subproblem Manager
**Example:** Delta Prover
The DSL structures complex reasoning tasks (e.g., formal proofs) into manageable subproblems. The agent uses the DSL to decompose, track, and reassemble sub-results.

### Pattern E: LLM-Generated DSL Constructs
**Example:** LLM-DSL-Gen, HAVEN (iterative coverage improvement)
The LLM directly generates DSL statements from natural language descriptions. This is the most natural "DSL from requirements" pattern — the DSL provides structure, the LLM provides fluency.

---

## Common Design Principles

1. **Bidirectional feedback loops** — Test results or compiler errors flow back to the agent to refine DSL output (ARC, HAVEN, ARGUS, GEAK).
2. **Compile-time verification** — DSL constructs are verified at compile time (ARGUS's SMT solving, ARC's test generation) rather than relying solely on runtime checks.
3. **Human-in-the-loop** — DSL artifacts are human-readable and human-authorable, enabling domain experts to review, correct, or even write DSL documents (ARC's user study).
4. **Token efficiency** — DSLs reduce token consumption vs. generating low-level code directly (μCUTLASS saves 19–43% of tokens).
5. **Traceability** — ARC maintains strict mappings from requirements DSL statements → design → code → tests, enabling maintenance and reuse.
6. **Modular compiler backends** — Multiple DSL-to-platform compilers (AKG supporting 4 DSLs) allow one agent system to target diverse environments.

---

## Summary

The state of the art in AI-driven DSL creation from requirements centers on using DSLs as structured intermediates that constrain LLM output, raise abstraction levels, and enable compile-time verification. The most mature approach is the **DSL-as-firewall** pattern (HAVEN, ARGUS), where a curated DSL combined with rule-based compilation produces correct-by-construction outputs. The **DSL-as-requirements-format** pattern (ARC) is the most ambitious — it compiles human-authored DSL documents directly into full-stack applications with tests. Across all systems, the trend is toward tight integration of agent orchestration (LangGraph-style), structured DSL intermediates, and bidirectional test/feedback loops.
