# Research Findings: Requirements-to-DSL Pipeline with AI Code Agents

## Overview

This report synthesizes findings from recent academic research (2025-2026) on using Large Language Models (LLMs) and multi-agent systems to transform natural-language requirements into Domain-Specific Language (DSL) specifications. Sources include papers from ICSE, EASE, FSE, and arXiv.

---

## 1. Common Pipeline Architectures (Prompt -> LLM -> DSL -> Validate -> Refine)

### EXEOS (Kinaxis/ICSE-SEIP 2026)
- **Pattern**: NL problem description -> LLM generates DSL (AMPL) + Python -> solver feedback -> iterative refinement
- **Key insight**: DSL quality is competitive with Python when iterative refinement with domain-specific solver feedback is used
- **Source**: arXiv:2601.00469

### ARC - Agentic Requirement Compilation (2026)
- **Pattern**: Multi-modal requirement documents -> DSL documents -> bidirectional test-driven agentic loop
  - Top-down: architecture agent decomposes requirements into verifiable interfaces
  - Bottom-up: code generation agents produce implementation to satisfy tests
- **Key insight**: Strict traceability across requirements, design, and code enables intelligent asset reuse
- **Source**: arXiv:2602.13723

### BMW Multi-File DSL Case Study (EASE 2026)
- **Pattern**: Single NL instruction -> structured JSON encoding folder hierarchies -> LLM generates multi-file Xtext DSL artifacts -> QLoRA fine-tuning
- **Key insight**: Encoding DSL folder hierarchies as path-preserving JSON enables repository-scale single-response generation
- **Findings**: Fine-tuning yields highest gains; one-shot ICL gives smaller but consistent improvements
- **Source**: arXiv:2604.24678

### Scenic DSL for Autonomous Driving (2026)
- **Pattern**: Crash reports (text + sketches) -> LLM extracts structured DSL configs -> intermediate Scenic DSL layer -> CARLA simulator
- **Key insight**: An intermediate DSL layer separates high-level semantic understanding from low-level scenario rendering, reducing errors
- **Source**: arXiv:2602.20644

### LintCFG (FSE 2026)
- **Pattern**: NL coding standards -> tool-agnostic DSL representation -> DSL configuration instructions -> linter-specific config generation
- **Key insight**: Compiler-inspired design parsing NL into structured DSL improves accuracy by >100% over baselines
- **Source**: arXiv:2602.07783

### HAVEN - UVM Testbench Generation (2026)
- **Pattern**: Design specs -> LLM agents analyze -> structured architectural plan -> template engine + Protocol-Aware DSL -> rule-based code gen
- **Key insight**: LLMs generate DSL sequences (not HDL directly), achieving 100% compilation success
- **Source**: arXiv:2604.27643

---

## 2. Multi-Agent Collaboration Patterns for DSL Creation

### ARC's Bidirectional Agent Loop
- **Architecture Agent**: Top-down requirement decomposition into interfaces
- **Implementation Agent**: Bottom-up code generation verified against tests
- **Test Agent**: Generates unit, modular, and integration test suites
- **Traceability Agent**: Maintains links across requirements, design, and code

### AKG Kernel Agent (Multi-Agent Framework)
- Specialized agents for: DSL parsing, code generation, cross-platform compilation, performance tuning
- Agents share a shared memory/context of generated artifacts

### AscendCraft / AscendKernelGen
- **DSL Agent**: Generates kernels in a lightweight intermediate DSL (abstracting hardware complexity)
- **Transcompilation Agent**: Converts DSL to vendor-specific code via constraint-driven LLM lowering passes
- **Evaluation Agent**: Tests compilation, correctness, and performance iteratively

### RedParrot (Xiaohongshu - Semantic Cache Pattern)
- **Skeleton Construction Agent**: Offline analysis of query patterns into normalized "query skeletons"
- **Matching Agent**: Online entity-agnostic embedding model for robust matching
- **RAG Agent**: Heterogeneous retrieval for unseen entities
- **Key insight**: Bypasses costly LLM pipeline for repeated queries using a semantic cache; 3.6x speedup

---

## 3. Validation and Testing Approaches for AI-Generated DSLs

### Well-Formedness + Correctness Framework (Delgado et al. 2026)
- **Well-formedness**: DSL artifact parses and passes syntax/grammar checks
- **Correctness**: DSL artifact matches expected semantics from requirements
- **Techniques**:
  - Code repair: asking LLM to fix incorrect code improves quality
  - Multiple attempts: generating N candidates per task improves pass rate
  - Normalization: canonical file form for consistent comparison
  - Extensible parsing: syntax analysis before costly execution tests
- **Source**: arXiv:2603.05278

### Structural Fidelity Metrics (BMW Case Study)
- **Edit correctness**: how accurately changes match the intended modification
- **Repository structural fidelity**: whether generated folder/file structure matches expectations
- **Execution-based checking**: running generated DSL through existing code generators

### SMT-Based Validation (ARGUS GPU Framework)
- Compile-time data-flow invariants verified via abstract interpretation over a layout algebra + SMT solving
- Zero runtime overhead; counterexamples returned identifying exact thread/data/program point

### SOL (Speed-of-Light) Guidance (muCUTLASS)
- First-principles performance bounds to budget search and detect benchmark-gaming
- Prevents wasted iterations when near theoretical peak

### Coverage-Guided Testing (HAVEN)
- Iteratively analyze coverage gap reports -> compose additional targeted DSL sequences

### Normalized Trace Replay (Policy-First Tooling)
- Controlled fault and misuse injection into trace replay for violation prevention measurement

---

## 4. Prompt Engineering Techniques for DSL Generation

### In-Context Learning Approaches
- **One-shot ICL**: Providing a single DSL example in the prompt yields consistent (if modest) improvement over zero-shot
- **Structured JSON encoding**: Representing multi-file project structure as path-preserving JSON within a single prompt

### Context Window Management
- DSL generation requires managing both the constraint/domain model AND the DSL itself within context
- Small-context open-source LLMs struggle; larger context windows (or structured chunking) is needed
- Chain-of-thought reasoning datasets (e.g., Ascend-CoT) improve DSL code quality

### Fine-Tuning Strategies
- **QLoRA**: Parameter-efficient fine-tuning on domain-specific DSL examples yields the largest gains
- Domain-adaptive models (KernelGen-LM) trained via SFT + RL with execution feedback

### Prompt Template Design
- Template choice has LESS impact than code repair or multiple-attempt strategies
- More important: clear grammar specification, DSL syntax examples, and domain model context

### Constraint-Driven Generation
- Specify DSL grammar rules explicitly in the system prompt
- Use tag functions to propagate symbolic annotations through data and control flow
- Tag assertions enforce relational constraints at use sites

### Retrieval-Augmented Generation (RAG)
- Heterogeneous RAG integrating diverse knowledge sources for unseen entities
- Query skeleton matching + DSL adaptation bypasses full pipeline for repeated patterns

---

## 5. Source URLs

| # | Title | URL |
|---|-------|-----|
| 1 | EXEOS: DSL or Code? (Kinaxis/ICSE-SEIP 2026) | https://arxiv.org/abs/2601.00469 |
| 2 | ARC: Compiling Requirements into Runnable Systems | https://arxiv.org/abs/2602.13723 |
| 3 | BMW Multi-File DSL Code Generation (EASE 2026) | https://arxiv.org/abs/2604.24678 |
| 4 | Scenic DSL for Autonomous Driving Safety | https://arxiv.org/abs/2602.20644 |
| 5 | LintCFG: DSL-Based LLM Compilation (FSE 2026) | https://arxiv.org/abs/2602.07783 |
| 6 | HAVEN: UVM Testbench with DSL Sequences | https://arxiv.org/abs/2604.27643 |
| 7 | AKG Kernel Agent (Multi-Agent Framework) | https://arxiv.org/abs/2512.23424 |
| 8 | A Framework for Assessing DSL Code Gen with LLMs | https://arxiv.org/abs/2603.05278 |
| 9 | RedParrot: NL-to-DSL via Semantic Cache | https://arxiv.org/abs/2604.22758 |
| 10 | ARGUS: Agentic GPU Optimization with Data-Flow Invariants | https://arxiv.org/abs/2604.18616 |
| 11 | muCUTLASS: DSL for GPU Kernel Optimization | https://arxiv.org/abs/2603.29010 |
| 12 | AscendCraft: DSL-Guided NPU Kernel Transcompilation | https://arxiv.org/abs/2601.22760 |
| 13 | AscendKernelGen: LLM Kernel Generation for NPUs | https://arxiv.org/abs/2601.07160 |
| 14 | Evaluating LLM-Generated DSL: LAMMPS Molecular Dynamics | https://arxiv.org/abs/2603.20630 |
| 15 | GitHub: LLM-DSL-Gen (Lokad/Ecole Polytechnique) | https://github.com/SaturnTsen/LLM-DSL-Gen |
| 16 | arXiv search: LLM DSL generation (66 results) | https://arxiv.org/search/?query=LLM+DSL+generation&searchtype=all |

---

## Key Takeaways

1. **Intermediate DSL layers** are critical -- they separate semantic understanding from low-level generation, reducing error propagation
2. **Bidirectional test-driven loops** (top-down architecture + bottom-up implementation) outperform monolithic generation
3. **Iterative refinement with execution feedback** (solver output, coverage gaps, compilation errors) dramatically improves DSL quality
4. **Fine-tuning (QLoRA)** on domain-specific DSL examples yields the largest gains; one-shot ICL is a distant second
5. **Prompt template choice matters less** than code repair loops or multiple-attempt strategies
6. **Validation needs two axes**: well-formedness (syntax/grammar) and correctness (semantic match to requirements)
7. **Multi-agent decomposition** (architect, implementer, tester, tracers) is the dominant paradigm for complex DSL generation
8. **Semantic caching** (query skeletons -> cached DSL patterns) is an effective optimization for production-scale NL-to-DSL

---

*Research conducted April 2026. Primary source: arXiv cs.SE / cs.AI recent submissions.*
