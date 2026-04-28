# LLM Benchmarks: Research Findings

## 1. MMLU (Massive Multitask Language Understanding)

- **What it evaluates:** General knowledge and problem-solving across 57 academic subjects
- **Task categories:** Multiple-choice question answering
- **Sub-categories:** 57 subjects organized into STEM, humanities, social sciences, and other domains (e.g., abstract algebra, international law, professional medicine, nutrition, religion, virology, physics, US history, etc.)
- **Format:** 15,908 multiple-choice questions (4 answer choices each)
- **Key note:** Human domain experts score ~89.8%; current SOTA models achieve ~88%

---

## 2. HumanEval

- **What it evaluates:** Functional correctness of code generated from docstrings (Python)
- **Task categories:** Code generation / program synthesis
- **Sub-categories:** 164 hand-written programming problems testing diverse algorithmic and data structure concepts
- **Format:** Models generate Python functions from natural-language docstrings; evaluated via functional correctness (pass@k)
- **Key note:** Introduced alongside OpenAI Codex; GPT-3 scored 0%, Codex scored 28.8%

---

## 3. GSM8K (Grade School Math 8K)

- **What it evaluates:** Multi-step mathematical reasoning ability
- **Task categories:** Math word problem solving / arithmetic reasoning
- **Sub-categories:** Grade-school-level math problems requiring 2-8 steps of reasoning (addition, subtraction, multiplication, division, logic)
- **Format:** 8,500 linguistically diverse math word problems; free-form natural language answer
- **Key note:** Even large transformers struggled; solved via training verifiers to judge solution correctness

---

## 4. HellaSwag

- **What it evaluates:** Commonsense natural language inference and sentence completion
- **Task categories:** Commonsense reasoning / contextual language understanding
- **Sub-categories:** Situations involving physical actions, social interactions, procedural activities
- **Format:** Multiple-choice (pick the most likely ending to a sentence/description)
- **Key note:** Built via Adversarial Filtering (AF); humans score >95%, SOTA models <48% at release

---

## 5. ARC (AI2 Reasoning Challenge)

- **What it evaluates:** Advanced question answering requiring knowledge and reasoning
- **Task categories:** Science question answering / knowledge-intensive QA
- **Sub-categories:** Challenge Set (hard) and Easy Set; grade-school science questions (7,787 total)
- **Format:** Multiple-choice; includes a corpus of 14M science sentences
- **Key note:** Challenge Set questions were answered incorrectly by both retrieval-based and word co-occurrence algorithms

---

## 6. TruthfulQA

- **What it evaluates:** Truthfulness — whether models avoid mimicking human falsehoods and misconceptions
- **Task categories:** Factual accuracy / truthfulness / misinformation resistance
- **Sub-categories:** 38 categories including health, law, finance, politics, conspiracy theories, stereotypes, and misconceptions
- **Format:** 817 questions; generative (model produces free-text answers)
- **Key note:** Larger models were generally less truthful; best model at release: 58% vs human 94%

---

## 7. BIG-bench (Beyond the Imitation Game Benchmark)

- **What it evaluates:** Broad capabilities of large language models across diverse tasks
- **Task categories:** 200+ tasks organized into high-level keyword groups:
  - **Traditional NLP tasks:** contextual QA, reading comprehension, summarization, paraphrase, translation, word sense disambiguation, grammar, syntax, dialogue
  - **Logic, math, code:** logical reasoning (59 tasks), mathematics (28), arithmetic (22), algorithms (5), computer code (12), fallacy (4), negation (4), probabilistic reasoning (1)
  - **Understanding the world:** causal reasoning (17), common sense (50), physical reasoning (2), visual reasoning (14)
  - **Understanding humans:** theory of mind (10), emotional understanding (16), social reasoning (19), humor (2), figurative language (4)
  - **Scientific/technical:** biology, chemistry, physics, medicine
  - **Pro-social behavior:** social bias (9), gender bias (9), racial bias (4), religious bias (5), truthfulness (8), toxicity (1), alignment (4)
  - **Other:** analogical reasoning (19), creativity (15), multilingual (13), low-resource language (11), non-English (18)
- **Format:** Mix of JSON-based (172 tasks) and programmatic (42 tasks); multiple-choice and free-response
- **Key note:** BIG-bench Lite (BBL) is a 24-task subset for efficient evaluation

---

## 8. WinoGrande

- **What it evaluates:** Commonsense reasoning via pronoun resolution
- **Task categories:** Coreference resolution / commonsense reasoning
- **Sub-categories:** Winograd Schema Challenge-style problems at scale (44k problems)
- **Format:** Multiple-choice (select the correct referent for a pronoun in a sentence)
- **Key note:** Built with AfLite bias reduction algorithm; human performance 94%, SOTA 59-79%

---

## 9. BBQ (Bias Benchmark for QA)

- **What it evaluates:** Social bias in question answering
- **Task categories:** Fairness / bias measurement
- **Sub-categories:** 9 social dimensions: age, disability status, gender identity, nationality, physical appearance, race/ethnicity, religion, socioeconomic status, sexual orientation
- **Format:** Multiple-choice QA with under-informative and adequately informative contexts
- **Key note:** Tests whether models rely on stereotypes when context is ambiguous, and whether biases override correct answers when context is sufficient

---

## 10. Additional Notable Benchmarks

### GLUE / SuperGLUE
- **Task categories:** General language understanding (sentiment analysis, textual entailment, paraphrase detection, etc.)
- Legacy benchmarks that preceded MMLU; largely saturated

### MATH
- **Task categories:** Advanced mathematical reasoning (competition-level math problems)
- **Sub-categories:** Algebra, geometry, number theory, counting & probability, precalculus

### MBPP (Mostly Basic Python Programming)
- **Task categories:** Code generation (similar to HumanEval but simpler)
- 974 Python programming problems

### HELM (Holistic Evaluation of Language Models)
- **Task categories:** Holistic evaluation covering accuracy, calibration, robustness, fairness, bias, toxicity, and efficiency across many scenarios

### SWE-bench
- **Task categories:** Real-world software engineering (GitHub issue resolution)
- Tests models on actual pull request generation

---

## Summary of Task Categories Mapped to Benchmarks

| Task Category | Benchmark(s) |
|---|---|
| Knowledge & QA | MMLU, ARC, TruthfulQA |
| Code generation | HumanEval, MBPP, SWE-bench |
| Math reasoning | GSM8K, MATH |
| Commonsense reasoning | HellaSwag, WinoGrande |
| Truthfulness / hallucination | TruthfulQA |
| Bias & fairness | BBQ, BIG-bench (social bias) |
| Broad / multi-capability | BIG-bench (200+ tasks), HELM, GLUE/SuperGLUE |
| Reading comprehension | ARC, BIG-bench (36 reading comp tasks) |
| Logical reasoning | BIG-bench (59 tasks) |
| Scientific reasoning | ARC, MMLU (STEM), BIG-bench (physics/chem/bio) |
