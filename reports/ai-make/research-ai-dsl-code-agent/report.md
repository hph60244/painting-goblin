# Comparative Analysis: AI Code Agents Creating DSLs from Requirement Documents

## Executive Summary

This report surveys 20+ systems (2025-2026) where AI code agents create or use Domain-Specific Languages (DSLs) from requirement documents. Two dominant paradigms emerge: (1) **DSL-as-intermediate-representation** — agents generate DSL code as a constrained bridge between natural language and final output, and (2) **DSL-as-requirements-format** — humans (or agents) write DSL documents that a pipeline compiles into full applications. The most reliable approach uses bidirectional test-driven loops, compile-time verification, and iterative refinement with execution feedback.

---

## 1. Paradigm Comparison

| Paradigm | Description | Examples | Maturity |
|----------|-------------|----------|----------|
| **DSL as Safe IR** | DSL constrains LLM output; rule-based compiler transforms to correct code | HAVEN, ARGUS | High (proven in correctness-critical domains) |
| **DSL as Abstraction Layer** | DSL raises reasoning level, saves tokens, preserves optimization levers | μCUTLASS, AKG, GEAK | High (hardware optimization, verified speedups) |
| **DSL as Requirements Format** | Human/agent writes DSL doc; pipeline compiles to full-stack app | ARC, Basalt | Medium (ARC shows strong results, but early-stage) |
| **DSL as Subproblem Manager** | DSL decomposes complex reasoning into manageable subproblems | Delta Prover | High (95.9% success on miniF2F-test) |
| **LLM-Generated DSL Constructs** | LLM directly generates DSL statements from NL descriptions | LLM-DSL-Gen, Rubric | Medium (strong case studies, but tool-specific) |

---

## 2. Pipeline Architecture Patterns

### Pattern A: Bidirectional Test-Driven Loop (Recommended)
```
Requirements → [Architecture Agent] → DSL Doc → [Impl Agent + Test Agent] → Code + Tests
                    ↑                              |
                    └─────── Test feedback ────────┘
```
**Source:** ARC (arXiv:2602.13723) — 50.6% more tests passed vs. SOTA

### Pattern B: DSL Firewall with Rule-Based Compilation
```
Requirements → LLM Agent → DSL Constructs → [Rule-Based Compiler] → Correct Code
                                         ↑                        |
                                         └── Compiler feedback ───┘
```
**Source:** HAVEN (arXiv:2604.27643) — 100% compilation success, 90.6% coverage

### Pattern C: Multi-Agent Specialization
```
[Architecture Agent] → DSL interfaces
[Implementation Agent] → DSL → Code
[Test Agent] → Unit/Integration tests
[Traceability Agent] → Requirements ↔ Code links
```
**Source:** ARC, AKG (arXiv:2512.23424), AscendCraft (arXiv:2601.22760)

### Pattern D: Iterative Refinement with Solver Feedback
```
NL Problem → LLM → DSL + Code → [Solver/Simulator] → Refinement Feedback
                                                    ↓
                                            Iterate until pass
```
**Source:** EXEOS/Kinaxis (arXiv:2601.00469), GEAK (arXiv:2507.23194)

---

## 3. Key Design Principles

| Principle | Description | Evidence |
|-----------|-------------|----------|
| **Bidirectional feedback** | Test/compiler errors flow back to refine DSL | ARC, HAVEN, ARGUS, GEAK |
| **Compile-time verification** | Verify DSL at compile time, not runtime | ARGUS (SMT), ARC (test gen) |
| **Human-in-the-loop** | DSL artifacts are human-readable/reviewable | ARC (novices authored DSL in ~5.6h) |
| **Token efficiency** | DSL reduces token cost vs. raw code | μCUTLASS: 19-43% token savings; Basalt: ~20x cheaper |
| **Traceability** | Requirements → DSL → Code → Tests links | ARC's strict mapping |
| **Closed grammars** | Valid DSL = valid output | Basalt: "if it's valid .bs, output is valid code" |
| **Validation loops** | Generate → validate → fix → iterate | Rubric, ARC, HAVEN |

---

## 4. What Works (from Case Studies)

1. **DSL as intermediate representation** — Basalt, Rubric, and LLM-DSL-Runtime-Emacs use constrained DSLs as bridges between NL and code
2. **Self-validating workflows** — Rubric's generate → validate → fix → generate code → validate loop
3. **Token cost reduction** — Basalt reports 20x cost reduction (10 lines DSL vs. 200 lines TypeScript)
4. **Closed/constrained grammars** — LLM can only produce valid DSL tokens → inherently reliable output
5. **Multi-file project generation** — BMW EASE case study uses JSON-encoded folder hierarchies for single-response DSL project generation

## 5. What Fails

1. **Building on unstable foundations** — MCP-DSL paused because the underlying MCP spec evolved faster than the DSL
2. **Speculative DSLs without implementations** — SWAN-DSL produced specs with no working compiler
3. **IDE/tool lock-in** — Rubric is Cursor-only; many tools tied to specific platforms
4. **Over-ambitious scope** — Biggest failures came from expanding too fast before DSL stability
5. **Token overhead without validation** — Rubric acknowledges increased token usage

---

## 6. Prompt & Training Strategies (Ranked by Impact)

1. **QLoRA fine-tuning** on domain-specific DSL examples → largest gains (BMW EASE study)
2. **Code repair / multiple attempts** → bigger impact than prompt template choice (Delgado et al. 2026)
3. **One-shot ICL** with one DSL example → modest but consistent improvement
4. **Structured JSON encoding** of multi-file project structure → enables repo-scale generation
5. **Constraint-driven generation** (grammar rules in system prompt, tag functions, tag assertions)
6. **RAG** for unseen entities and query skeleton matching

---

## 7. Open-Source Reference Projects

| Project | Domain | Approach | URL |
|---------|--------|----------|-----|
| **Basalt** | Backend API code gen | DSL-as-IR, NL→DSL→code | https://github.com/DiegoDev2/Basalt |
| **Rubric** | Architecture enforcement | Self-validating DSL workflow | https://github.com/graciolli-f/Rubric |
| **LLM-DSL-Gen** | Lokad DSL generation | LLM directly generates DSL | https://github.com/SaturnTsen/LLM-DSL-Gen |
| **SWAN-DSL** | UI interaction modeling | AI-generated full DSL spec | https://github.com/NAIV-Dev/swan-dsl |
| **MCP-DSL** | AI agent orchestration | AI-assisted DSL design (paused) | https://github.com/jmajerus/MCP-DSL |
| **LLM-DSL-Runtime-Emacs** | Safe LLM code execution | DSL as safety IR for Emacs | https://github.com/kroq86/llm-dsl-runtime-emacs |

---

## 8. Recommendations for Building Code Agent → DSL Pipeline

1. **Start small, with a closed grammar** — Define a minimal DSL that covers the core domain. Add constructs only when needed.
2. **Build bidirectional feedback** — Compiler errors, test failures, and coverage gaps should flow back to the agent for self-correction.
3. **Use multi-agent decomposition** — Separate architecture design, DSL generation, code generation, and testing into specialized agents.
4. **Include AI generation guidelines in the DSL spec** — As Basalt does: "Output only the DSL content, no explanations, no markdown."
5. **Validate on two axes** — Well-formedness (syntax) and correctness (semantic match to requirements).
6. **Consider fine-tuning (QLoRA)** if the domain is stable and has sufficient DSL examples.
7. **Design for human review** — DSL artifacts should be human-readable so domain experts can validate AI output.

---

## Sources

- ARC: arXiv:2602.13723 — https://arxiv.org/abs/2602.13723
- HAVEN: arXiv:2604.27643 — https://arxiv.org/abs/2604.27643
- ARGUS: arXiv:2604.18616 — https://arxiv.org/abs/2604.18616
- μCUTLASS: arXiv:2603.29010 — https://arxiv.org/abs/2603.29010
- EXEOS: arXiv:2601.00469 — https://arxiv.org/abs/2601.00469
- BMW DSL: arXiv:2604.24678 — https://arxiv.org/abs/2604.24678
- LintCFG: arXiv:2602.07783 — https://arxiv.org/abs/2602.07783
- AKG: arXiv:2512.23424 — https://arxiv.org/abs/2512.23424
- Delta Prover: arXiv:2507.15225 — https://arxiv.org/abs/2507.15225
- Basalt: https://github.com/DiegoDev2/Basalt
- Rubric: https://github.com/graciolli-f/Rubric
- LLM-DSL-Gen: https://github.com/SaturnTsen/LLM-DSL-Gen
