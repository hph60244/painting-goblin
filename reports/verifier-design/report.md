# Verifier Design Report: Mapping Task Types to Automated Verification Methods

## Executive Summary

A **verifier** is a mechanism that checks whether an AI agent's output is correct. The ease of building a verifier is the single most important factor determining which tasks get automated first (Chopra, 2026). This report maps task types from two foundational taxonomies — knowledge work domains and AI evaluation task categories — to suitable verifiers, providing a decision framework for AI agent implementation.

---

## Part 1: Verifier Taxonomy

### 1.1 Ten Verifier Types

| # | Verifier Type | Mechanism | Automation Level | Cost | False Positive Risk |
|---|--------------|-----------|-----------------|------|-------------------|
| **V1** | Execution-Based | Run code/test in real environment | Full | High | Low |
| **V2** | Ground-Truth Matching | Compare against known correct answer | Full | Low | Low |
| **V3** | Reference-Based | Compare against reference via n-gram overlap | Full | Low | Medium |
| **V4** | LLM-as-Judge | Use another LLM to evaluate quality | Partial | Medium | Medium-High |
| **V5** | Rule-Based | Check against explicit constraints (format, length, keywords) | Full | Low | Low |
| **V6** | Environment Execution | Run in real/simulated interactive environment | Full | Very High | Low |
| **V7** | Safety/Security | Check toxicity, bias, harmful content | Full | Medium | Medium |
| **V8** | Human Evaluation | Human judges or crowdsourced ratings | Manual | Very High | Low |
| **V9** | Composite/Chain | Combine multiple verifiers in sequence | Full | High | Low |
| **V10** | Statistical Validation | Reproducibility, cross-validation, significance tests | Full | Medium | Medium |

### 1.2 Verifier Decision Tree

```
Is there a ground-truth answer?
├── YES → Can it be checked programmatically?
│   ├── YES → V2 (Ground-Truth Matching) — Best: exact match, accuracy, F1
│   └── NO  → Does the task produce executable output?
│       ├── YES → V1 (Execution-Based) — Best: pass@k, unit tests
│       └── NO  → V4 (LLM-as-Judge) or V8 (Human Evaluation)
└── NO  → Does the task have a reference/comparison corpus?
    ├── YES → V3 (Reference-Based) — Best: ROUGE, BLEU, chrF++
    └── NO  → Does the task operate in an interactive environment?
        ├── YES → V6 (Environment Execution) — Best: pass rate, success rate
        └── NO  → Are there explicit constraints?
            ├── YES → V5 (Rule-Based) — Best: format checks, constraint validation
            └── NO  → V4 (LLM-as-Judge) or V8 (Human Evaluation)
```

---

## Part 2: Verifier Mapping for Knowledge Work Domains

### Domain 1: 技術開發 (Technical Development)
*Software engineering, system architecture, DevOps, cybersecurity*

| Task Type | Recommended Verifier | Specific Method | Implementation |
|-----------|---------------------|-----------------|----------------|
| Function/code generation | **V1 Execution-Based** | pass@k | Run generated code against unit test suite; pass if all tests pass |
| Bug fixing / code repair | **V1 Execution-Based** | % Resolved | Run existing test suite before and after fix; verify all tests pass |
| Code review | **V9 Composite** | Lint check + test pass + LLM review | Static analysis (linter) + unit tests + code style check |
| System architecture design | **V4 LLM-as-Judge** | Architecture review rubric | LLM evaluates against checklist: scalability, security, maintainability, cost |
| DevOps pipeline config | **V1 Execution-Based** | Dry-run + integration test | Run pipeline in staging; verify each stage completes successfully |
| Security audit | **V9 Composite** | SAST + dependency check + compliance | Static analysis + CVE database check + policy rule engine |

**Verifiability Score**: 5/5 (Easiest to verify — automation frontier leader)

### Domain 2: 創意設計 (Creative Design)
*Advertising, architecture, UX/UI, brand design*

| Task Type | Recommended Verifier | Specific Method | Implementation |
|-----------|---------------------|-----------------|----------------|
| UI/UX prototype | **V4 LLM-as-Judge** | Design principle scoring | LLM evaluates against usability heuristics (Nielsen's 10), accessibility (WCAG), consistency |
| Brand asset creation | **V5 Rule-Based** | Brand guideline compliance | Check color palette, typography, logo usage rules against specification |
| Advertisement copy | **V9 Composite** | Rule check + LLM judge + A/B test | Tone check + brand alignment + conversion prediction |
| Architecture design | **V4 LLM-as-Judge** | Building code + aesthetic scoring | Structural requirements check + style coherence evaluation |
| Design iteration feedback | **V4 LLM-as-Judge** | Rubric-based evaluation | Score against design brief criteria: originality, coherence, feasibility, audience fit |

**Verifiability Score**: 2/5 (Hard to verify — subjective quality domain)

### Domain 3: 分析研究 (Analytical Research)
*Data science, market analysis, academic research*

| Task Type | Recommended Verifier | Specific Method | Implementation |
|-----------|---------------------|-----------------|----------------|
| Data analysis / statistics | **V10 Statistical Validation** | Reproducibility check | Run analysis script; verify output matches reported figures; validate statistical assumptions |
| Machine learning model training | **V10 Statistical Validation** | Cross-validation + metric check | Verify train/test split; check metrics (F1, AUC, MSE); compare against baseline |
| Market research report | **V9 Composite** | Fact check + data source + LLM review | Verify claims against cited sources; check data recency; LLM evaluates logic coherence |
| Academic literature review | **V9 Composite** | Citation check + coverage analysis | Verify citation accuracy; check coverage of key papers; identify gaps |
| Experiment design | **V4 LLM-as-Judge** | Methodological soundness check | Evaluate against: sample size adequacy, confounding control, randomization, blinding |

**Verifiability Score**: 3/5 (Moderate — partially automatable verification)

### Domain 4: 行政管理 (Administrative Management)
*Project management, HR, operations*

| Task Type | Recommended Verifier | Specific Method | Implementation |
|-----------|---------------------|-----------------|----------------|
| Project plan creation | **V5 Rule-Based** | Completeness checklist | Verify all required sections exist: scope, timeline, resources, risks, milestones |
| Budget report | **V10 Statistical Validation** | Numerical reconciliation | Sum all line items; verify matches total; check category allocations against policy |
| Schedule management | **V5 Rule-Based** | Dependency + constraint check | Verify no circular dependencies; check resource overallocation; validate critical path |
| Compliance document | **V5 Rule-Based** | Regulation checklist | Check against regulatory requirement checklist; verify all mandatory clauses present |
| Meeting minutes | **V4 LLM-as-Judge** | Action item extraction accuracy | LLM compares extracted actions, decisions, and owners against recording transcript |

**Verifiability Score**: 4/5 (Fairly easy — rule-based and checklist-driven)

### Domain 5: 策略規劃 (Strategic Planning)
*Corporate strategy, policy making, consulting*

| Task Type | Recommended Verifier | Specific Method | Implementation |
|-----------|---------------------|-----------------|----------------|
| Business strategy proposal | **V4 LLM-as-Judge** | Strategic soundness evaluation | LLM evaluates: internal consistency, market assumption validity, competitive response, financial feasibility |
| Risk assessment | **V9 Composite** | Scenario stress-test + coverage check | Verify all risk categories covered; test under multiple scenarios; validate probability estimates |
| Policy recommendation | **V4 LLM-as-Judge** | Stakeholder impact analysis | Evaluate policy against: stakeholder groups, second-order effects, implementation feasibility, legal constraints |
| SWOT analysis | **V4 LLM-as-Judge** | Completeness + accuracy check | Verify each quadrant populated; check claims against known data; evaluate strategic coherence |
| Decision memo | **V9 Composite** | Logic tree + evidence + conclusion | Verify logic tree completeness; check evidence supports conclusions; identify logical fallacies |

**Verifiability Score**: 2/5 (Hard to verify — high uncertainty and causal complexity)

### Domain 6: 知識傳播與教育 (Knowledge Dissemination & Education)
*Teaching, training, knowledge management*

| Task Type | Recommended Verifier | Specific Method | Implementation |
|-----------|---------------------|-----------------|----------------|
| Course curriculum design | **V9 Composite** | Learning objective alignment | Verify Bloom's taxonomy coverage; check prerequisite sequencing; assess assessment-to-objective mapping |
| Educational content | **V5 Rule-Based** + **V4 LLM-as-Judge** | Accuracy check + pedagogical quality | Fact-check content; evaluate clarity, age-appropriateness, engagement level |
| Assessment / quiz creation | **V2 Ground-Truth Matching** | Answer key validation | Verify answer key correctness; check distractor quality; validate question difficulty distribution |
| Knowledge base article | **V5 Rule-Based** | Knowledge base format compliance | Check required fields: title, summary, category, keywords, related articles |
| Training effectiveness | **V10 Statistical Validation** | Pre/post test comparison | Statistical significance test of learning gain; effect size calculation |

**Verifiability Score**: 3/5 (Moderate — mix of objective and subjective elements)

---

## Part 3: Verifier Mapping for AI Evaluation Task Categories

### Category 1: 知識與問答 (Knowledge & QA)

| Sub-task | Verifier | Metric | Notes |
|----------|----------|--------|-------|
| Multiple-choice QA (MMLU, ARC) | **V2 Ground-Truth** | Accuracy | Trivial to verify — single correct answer |
| Reading comprehension (SQuAD, RACE) | **V2 Ground-Truth** | F1, Exact Match | Span extraction — compare spans |
| Multi-hop reasoning (HotpotQA) | **V2 Ground-Truth** | F1, Exact Match | Cross-document reasoning |
| Open-domain QA (Natural Questions) | **V2 Ground-Truth** | Exact Match, F1 | No external context provided |

### Category 2: 推理 (Reasoning)

| Sub-task | Verifier | Metric | Notes |
|----------|----------|--------|-------|
| Math word problems (GSM8K) | **V2 Ground-Truth** | Exact Match | Compare final answer; increasingly check intermediate steps |
| Competition math (MATH, AIME) | **V2 Ground-Truth** | Accuracy | Verify answer against solution key |
| Logical reasoning (BBH) | **V2 Ground-Truth** | Accuracy | Multiple-choice format simplifies verification |
| Formal proof (ProofNet, MiniF2F) | **V1 Execution-Based** | Proof Completion Rate | Formal verification system checks proof correctness |

### Category 3: 常識推理 (Commonsense Reasoning)

| Sub-task | Verifier | Metric | Notes |
|----------|----------|--------|-------|
| Situation completion (HellaSwag) | **V2 Ground-Truth** | Accuracy | Multiple-choice — straightforward |
| Pronoun resolution (WinoGrande) | **V2 Ground-Truth** | Accuracy | Binary classification |
| Physical/social reasoning | **V2 Ground-Truth** | Accuracy | BIG-bench tasks are multiple-choice |

### Category 4: 生成 (Generation)

| Sub-task | Verifier | Metric | Notes |
|----------|----------|--------|-------|
| Summarization (CNN/DailyMail) | **V3 Reference-Based** | ROUGE-1/2/L | N-gram overlap against reference summary |
| Machine translation (WMT) | **V3 Reference-Based** | BLEU, chrF++, COMET | Lexical overlap; COMET uses neural evaluator |
| Creative writing | **V4 LLM-as-Judge** | GPT-4 Score (1-10) | LLM evaluates creativity, coherence, style |
| Dialogue generation (MT-Bench) | **V4 LLM-as-Judge** | GPT-4 Score | Multi-turn quality assessment |

### Category 5: 程式碼 (Coding)

| Sub-task | Verifier | Metric | Notes |
|----------|----------|--------|-------|
| Function generation (HumanEval, MBPP) | **V1 Execution-Based** | pass@k | Run unit tests in sandboxed environment |
| Competition programming (APPS) | **V1 Execution-Based** | pass@k, Test Case Accuracy | More comprehensive test suites |
| Bug fixing (SWE-bench) | **V1 Execution-Based** | % Resolved | Clone repo, apply patch, run test suite |
| Code execution prediction (CRUXEval) | **V1 Execution-Based** | Output Prediction Accuracy | Execute code and compare predicted output |

### Category 6: 工具使用與 API 調用 (Tool Use & API Calling)

| Sub-task | Verifier | Metric | Notes |
|----------|----------|--------|-------|
| Single tool call (ToolBench G1) | **V1 Execution-Based** | Pass Rate, Success Rate | Call actual API; check response matches expected |
| Multi-tool composition (ToolBench G2-G3) | **V9 Composite** | End-to-End Success | Verify tool sequence correctness + final output |
| API retrieval (API-Bank L1) | **V2 Ground-Truth** | Retrieval Accuracy | Compare selected API against ground-truth |

### Category 7: 網頁互動 (Web Interaction)

| Sub-task | Verifier | Metric | Notes |
|----------|----------|--------|-------|
| Shopping / forum tasks (WebArena) | **V6 Environment Execution** | Execution pass rate | Run in headless browser; verify final state |
| Visual web tasks (VisualWebArena) | **V6 Environment Execution** | Execution pass rate | Screenshot-based interaction verification |
| Form filling (MiniWoB++) | **V6 Environment Execution** | Cumulative Reward | Check DOM state after actions |

### Category 8: 作業系統與電腦操作 (OS & Computer Use)

| Sub-task | Verifier | Metric | Notes |
|----------|----------|--------|-------|
| Linux command line (AgentBench OS) | **V1 Execution-Based** | Success Rate | Run commands; check output matches expected |
| Desktop application (OSWorld) | **V6 Environment Execution** | Execution pass rate | Full VM; check application state after actions |
| Cross-app workflows | **V6 Environment Execution** | Execution pass rate | Verify file created, email sent, etc. |

### Category 9: 資料庫與知識圖譜 (Database & Knowledge Graph)

| Sub-task | Verifier | Metric | Notes |
|----------|----------|--------|-------|
| SQL query (AgentBench DB) | **V1 Execution-Based** | Success Rate | Execute SQL; compare result set against expected |
| SPARQL query (AgentBench KG) | **V1 Execution-Based** | Success Rate | Execute query; verify entities returned match |

### Category 10: 安全性與對齊 (Safety & Alignment)

| Sub-task | Verifier | Metric | Notes |
|----------|----------|--------|-------|
| Truthfulness (TruthfulQA) | **V2 Ground-Truth** | Truthfulness %, Informativeness | Adversarially crafted true/false questions |
| Social bias (BBQ, StereoSet) | **V7 Safety** | Bias Score, Differential | Measure disparity in model outputs across demographic groups |
| Toxicity (RealToxicityPrompts) | **V7 Safety** | Toxicity Probability | Classifier-based toxicity detection |
| Harmful content refusal | **V5 Rule-Based** | Refusal Rate | Check LLM response contains refusal pattern |

### Category 11: 指令遵循 (Instruction Following)

| Sub-task | Verifier | Metric | Notes |
|----------|----------|--------|-------|
| Multi-turn dialogue (MT-Bench) | **V4 LLM-as-Judge** | GPT-4 Judge (1-10) | LLM rates response quality |
| Verifiable constraints (IFEval) | **V5 Rule-Based** | Strict/Loose Accuracy | Check format: length, keywords, JSON structure, etc. |
| Multi-level constraints (FollowBench) | **V5 Rule-Based** | Step-wise Accuracy | Verify each constraint independently |

### Category 12: 長上下文處理 (Long Context)

| Sub-task | Verifier | Metric | Notes |
|----------|----------|--------|-------|
| Long-document QA (LongBench) | **V2 Ground-Truth** | F1, ROUGE, Accuracy | Compare against ground-truth answers |
| Needle-in-haystack (NIAH) | **V2 Ground-Truth** | Retrieval Accuracy | Insert known fact; check if model retrieves it |
| Ultra-long context (RULER) | **V2 Ground-Truth** | Task-specific Accuracy | Varies by sub-task (count, locate, etc.) |

### Category 13: 領域特定評測 (Domain-Specific)

| Sub-task | Verifier | Metric | Notes |
|----------|----------|--------|-------|
| Medical exam (MedQA) | **V2 Ground-Truth** | Accuracy | Multiple-choice — straightforward |
| Clinical NER | **V2 Ground-Truth** | F1, Precision, Recall | Compare entity boundaries and types |
| Legal reasoning (ECHR) | **V2 Ground-Truth** | Accuracy | Case outcome prediction |
| Financial QA (FinQA) | **V2 Ground-Truth** | Exact Match, Program Acc | Numerical reasoning with computation |

### Category 14: 多語言與多模態 (Multilingual & Multimodal)

| Sub-task | Verifier | Metric | Notes |
|----------|----------|--------|-------|
| Cross-lingual NLU (XTREME) | **V2 Ground-Truth** | Accuracy, F1 | Standard classification/QA evaluation |
| Image captioning (COCO) | **V3 Reference-Based** | CIDEr, BLEU, ROUGE, SPICE | Multiple reference captions; SPICE captures semantic content |
| Visual QA (VQA v2) | **V2 Ground-Truth** | Accuracy | Answer set matching |
| Document understanding (DocVQA) | **V2 Ground-Truth** | ANLS | Average Normalized Levenshtein Similarity |

---

## Part 4: Verifier Implementation Guide for AI Agents

### 4.1 Generic Verifier Protocol

Each verifier should implement the following interface:

```
Input:
  - task_spec: description of what was requested
  - agent_output: what the agent produced
  - expected_output (optional): ground truth if available
  - environment (optional): execution context if needed

Output:
  - passed: boolean
  - score: float (0.0 - 1.0)
  - details: structured feedback (what passed, what failed)
  - diagnostics: error messages or improvement suggestions
```

### 4.2 Real-Time Error Hints Architecture

```
Agent produces output
        ↓
[Stage 1] Quick Pre-Checks (V5 Rule-Based)
  ├── Format validation → hint if malformed
  ├── Completeness check → hint if missing required sections
  └── Constraint verification → hint if constraint violated
        ↓
[Stage 2] Execution Checks (V1/V6 if applicable)
  ├── Run in sandbox/environment
  └── Capture errors → send diagnostics back to agent
        ↓
[Stage 3] Quality Evaluation (V2/V3/V4/V10)
  ├── Compare against expected
  └── Provide score with improvement suggestions
```

### 4.3 Verifier Selection by Automation Level

| Automation Level | Use Case | Recommended Verifier Combination |
|-----------------|----------|--------------------------------|
| **Fully Automated** (no human in loop) | High-volume, low-stakes | V1/V2/V5 — deterministic, zero human intervention |
| **Augmented** (AI produces, human reviews) | Moderate stakes, quality-sensitive | V4 + V9 — AI flags issues, human reviews flagged items |
| **Assisted** (AI proposes, human approves) | High stakes, judgment needed | V9 + V8 — AI provides diagnostics, human makes final call |

### 4.4 Verifier Implementation Priority

Based on difficulty of building a verifier (from easiest to hardest):

| Priority | Domain | Easiest Verifier Type | Why |
|----------|--------|-----------------------|-----|
| **1** | Coding | V1 (Execution) | Tests are already written in most projects |
| **2** | DB/KG queries | V1 (Execution) | Execute and compare result sets |
| **3** | Multiple-choice QA | V2 (Ground-Truth) | Exact comparison |
| **4** | Math reasoning | V2 (Ground-Truth) | Final answer comparison |
| **5** | Web interaction | V6 (Environment) | Headless browser automation |
| **6** | OS/Computer use | V6 (Environment) | Full VM automation (expensive) |
| **7** | Translation/Summarization | V3 (Reference) | N-gram metrics, but imperfect |
| **8** | Safety check | V7 (Safety) | Classifier-based, but adversarial |
| **9** | Instruction following | V5 (Rule) | Format checks are easy |
| **10** | Tool use | V1 (Execution) | Depends on API availability |
| **11** | Creative writing | V4 (LLM Judge) | Subjective, LLM bias |
| **12** | Strategy/Planning | V4 (LLM Judge) | Highly subjective |
| **13** | Design/Creative | V4 (LLM Judge) | Highly subjective |
| **14** | Research/Analysis | V10 (Statistical) | Partially automatable |

---

## Part 5: Quick-Reference Verifier Selection Matrix

### By Knowledge Work Domain (Report 1)

| Domain | Primary Verifier | Secondary Verifier | Implementation Effort |
|--------|-----------------|-------------------|----------------------|
| 技術開發 | V1 Execution-Based | V9 Composite (lint + test + review) | Medium |
| 創意設計 | V4 LLM-as-Judge | V5 Rule-Based (guidelines) | Low |
| 分析研究 | V10 Statistical | V9 Composite (fact + logic check) | Medium |
| 行政管理 | V5 Rule-Based | V4 LLM-as-Judge | Low |
| 策略規劃 | V4 LLM-as-Judge | V9 Composite (stress-test) | High |
| 知識傳播 | V5 Rule-Based | V4 LLM-as-Judge | Low |

### By AI Task Category (Report 2)

| Category | Primary Verifier | Metric(s) | Automation Readiness |
|----------|-----------------|-----------|---------------------|
| Knowledge & QA | V2 Ground-Truth | Accuracy, F1, EM | Ready now |
| Reasoning | V2 Ground-Truth | Accuracy, EM | Ready now |
| Commonsense | V2 Ground-Truth | Accuracy | Ready now |
| Generation | V3 Reference / V4 LLM Judge | ROUGE, BLEU, GPT Score | Ready now (imperfect) |
| Coding | V1 Execution | pass@k, % Resolved | Ready now |
| Tool Use | V1 Execution | Success Rate | Ready now |
| Web Interaction | V6 Environment | Pass Rate | Ready now (expensive) |
| OS & Computer | V6 Environment | Pass Rate | Ready now (very expensive) |
| DB & KG | V1 Execution | Success Rate | Ready now |
| Safety | V7 Safety | Bias, Toxicity | Ready now |
| Instruction Following | V5 Rule / V4 LLM | Strict/Loose Accuracy | Ready now |
| Long Context | V2 Ground-Truth | F1, Accuracy | Ready now |
| Domain-Specific | V2 Ground-Truth | Accuracy, F1 | Ready now |
| Multilingual/Multimodal | V2 / V3 | Accuracy, CIDEr, BLEU | Ready now |

---

## Part 6: Implementation Recommendations

### 6.1 Immediate Actions

1. **Build V5 Rule-Based Verifier** for the verify-task skill — this is the simplest and most generalizable. Start with format checks, completeness checks, and constraint validation.

2. **Implement V2 Ground-Truth Matching** for tasks with known answers (QA, math, classification). Use regex/exact match for simple cases, semantic similarity for paraphrased answers.

3. **Integrate V1 Execution-Based verifier** for coding tasks. Use Docker sandbox with Python/Node.js runtime, run unit tests, return pass/fail with error output.

### 6.2 Medium-Term

4. **Build V4 LLM-as-Judge wrapper** — configure an LLM with evaluation rubrics for subjective domains (design, strategy, creative). Always use a different model than the one being evaluated.

5. **Create V6 Environment Execution harness** for web and OS tasks (Playwright/Selenium for web, Docker + VNC for desktop).

### 6.3 Long-Term

6. **Build V9 Composite Verifier Engine** — a pipeline that chains multiple verifiers, aggregates scores, and provides structured diagnostics to the agent for real-time error hints.

7. **Develop task-specific verifier templates** for each knowledge work domain and AI task category, stored as reusable reference files in the verify-task skill.

---

## References

1. Chopra, P. (2026). "What domains will be the last ones to get automated from AI?" Inverted Passion. — Identifies "ease of building a verifier" as primary automation axis
2. AI-Task-Suitability Dimensions Report — Expands verifier concept across 16 dimensions
3. Knowledge Work Difficulty Report — 6-domain taxonomy of knowledge work
4. AI Evaluation Task Categories Report — 14-category taxonomy with existing benchmarks
5. Cobbe et al. (2021). "Verification and Validation of AI Systems"
6. Ribeiro et al. (2020). "CheckList: Beyond Accuracy for Behavioral Testing of NLP Models"
