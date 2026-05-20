# NLP Core Evaluation Dimensions & Domain-Specific Evaluations for LLMs

## Core Evaluation Dimensions

### 1. Reasoning
**Sub-dimensions:** Logical reasoning, mathematical reasoning, commonsense reasoning, symbolic reasoning

| Benchmark | Description | Typical Metrics |
|-----------|-------------|-----------------|
| **MMLU** (Massive Multitask Language Understanding) | 57 subjects across STEM, humanities, social sciences | Accuracy (0-100%) |
| **GSM8K** | Grade-school math word problems | Accuracy, exact match |
| **MATH** | Competition-level math problems (Hendrycks et al.) | Accuracy |
| **ARC** (AI2 Reasoning Challenge) | Science exam questions (grade-school level) | Accuracy |
| **HellaSwag** | Commonsense NLI: choose most plausible sentence ending | Accuracy |
| **BIG-Bench** | 204+ tasks testing reasoning, logic, and knowledge | Accuracy, multiple metrics |
| **BBH** (BIG-Bench Hard) | 23 challenging BIG-Bench tasks | Accuracy |
| **DROP** | Discrete reasoning over paragraphs | F1, exact match |
| **StrategyQA** | Multi-hop yes/no reasoning questions | Accuracy |

### 2. Comprehension
**Sub-dimensions:** Reading comprehension, document QA, dialogue understanding

| Benchmark | Description | Typical Metrics |
|-----------|-------------|-----------------|
| **SQuAD 2.0** | Reading comprehension with unanswerable questions | F1, exact match (EM) |
| **RACE** | Middle/high school English reading comprehension | Accuracy |
| **BoolQ** | Yes/no reading comprehension questions | Accuracy |
| **NarrativeQA** | Story-based question answering | F1, BLEU, ROUGE-L |
| **MultiRC** | Multi-sentence reading comprehension | F1, exact match |
| **CoQA** | Conversational question answering | F1 |
| **QuAC** | Question answering in context (dialogue) | F1, HEAQ |
| **DREAM** | Dialogue-based multiple-choice reading comprehension | Accuracy |
| **MuSiQue** | Multi-hop reading comprehension | F1, exact match |

### 3. Generation
**Sub-dimensions:** Summarization, translation, creative writing, dialogue

| Benchmark | Description | Typical Metrics |
|-----------|-------------|-----------------|
| **CNN/DailyMail** | News article summarization | ROUGE-1/2/L, ROUGEsum |
| **XSum** | Extreme summarization | ROUGE-1/2/L |
| **WMT** (Workshop on Machine Translation) | Translation between language pairs | BLEU, chrF, TER, COMET |
| **MT-Bench** | Multi-turn conversation quality | GPT-4 judge score (1-10) |
| **Chatbot Arena** | Crowd-sourced pairwise preference | Elo rating, Bradley-Terry |
| **GigaWord** | Sentence compression / headline generation | ROUGE |
| **SamSum** | Dialogue summarization | ROUGE |
| **WikiLingua** | Cross-lingual summarization | ROUGE, BLEU |
| **PersonaChat** | Persona-consistent dialogue generation | F1, perplexity, human eval |

### 4. Knowledge Retrieval
**Sub-dimensions:** Closed-book QA, fact verification

| Benchmark | Description | Typical Metrics |
|-----------|-------------|-----------------|
| **Natural Questions** | Google search query QA (closed-book) | Exact match, F1 |
| **TriviaQA** | Trivia question answering | Exact match, F1 |
| **WebQuestions** | Freebase-based QA | Exact match, F1 |
| **FEVER** | Fact extraction and verification | Accuracy, FEVER score |
| **TruthfulQA** | Questions that may trigger misconceptions | Accuracy, truthfulness |
| **HotpotQA** | Multi-hop factoid QA | Exact match, F1 |
| **2WikiMultihop** | Multi-hop Wikipedia QA | Exact match, F1 |
| **PopQA** | Long-tail knowledge QA | Accuracy |
| **MMLU** (knowledge sub-set) | Subject-specific knowledge recall | Accuracy |

### 5. Safety / Alignment
**Sub-dimensions:** Truthfulness, bias, toxicity, honesty

| Benchmark | Description | Typical Metrics |
|-----------|-------------|-----------------|
| **TruthfulQA** | Model's tendency to reproduce common misconceptions | Truthfulness %, informativeness |
| **BBQ** (Bias Benchmark for QA) | Social bias in ambiguous contexts | Accuracy differential, bias score |
| **StereoSet** | Stereotype measurement across groups | Stereotype score (SS), LMS |
| **CrowS-Pairs** | Crowdsourced stereotypes pairs | % of stereotypical choices |
| **RealToxicityPrompts** | Toxicity of model continuations | Toxicity probability, max toxicity |
| **BOLD** (Bias in Open-ended Language Generation) | Bias across domains | Sentiment, toxicity scores |
| **HONEST** | Hurtful sentence completions | HONEST score (binary) |
| **Winogender** | Gender pronoun coreference bias | Accuracy, bias rate |
| **WinoBias** | Anti-stereotype coreference | Accuracy, F1 |
| **Anthropic HH-RLHF** | Helpfulness/harmlessness preference data | Preference accuracy |
| **Safety-Prompts** (e.g., Beaver) | Refusal rate on unsafe inputs | Refusal rate, compliance rate |
| **Red-Teaming** (e.g., GARCON) | Adversarial attack success rate | Harmfulness score, attack success rate |

### 6. Instruction Following

| Benchmark | Description | Typical Metrics |
|-----------|-------------|-----------------|
| **MT-Bench** | Multi-turn instruction following quality | GPT-4 judge score (1-10) |
| **AlpacaEval** | Instruction-following vs. GPT-4 baseline | Win rate %, length-controlled win rate |
| **IFEval** | Verifiable instruction-following (constraints) | Strict/loose accuracy |
| **BELLE** | Chinese instruction following | BLEU, human evaluation |
| **FollowBench** | Multi-level constraints following | Step-wise accuracy |
| **Natural Instructions** | 1600+ diverse NLP task instructions | ROUGE-L, exact match |
| **Self-Instruct** | Self-generated instruction validation | Quality score |

### 7. Long Context Handling

| Benchmark | Description | Typical Metrics |
|-----------|-------------|-----------------|
| **LongBench** | 6 task categories, 21 datasets (avg 5-15k tokens) | F1, ROUGE, Accuracy |
| **SCROLLS** | Long-document QA, summarization | Exact match, ROUGE |
| **L-Eval** | Long-context QA (20 tasks, up to 100k tokens) | Accuracy, F1 |
| **CLRT** (Controlled Long-Range Tasks) | Needle-in-a-haystack retrieval | Retrieval accuracy |
| **ZeroSCROLLS** | Long-context under zero-shot conditions | ROUGE, F1, Accuracy |
| **NIAH** (Needle In A Haystack) | Fact retrieval from long contexts | Retrieval accuracy |
| **RULER** | Extended context reasoning beyond training length | Task-specific accuracy |

---

## Domain-Specific Evaluations

### 8. Coding

| Benchmark | Description | Typical Metrics |
|-----------|-------------|-----------------|
| **HumanEval** | 164 hand-written Python function completion | pass@k (functional correctness) |
| **MBPP** (Mostly Basic Python Programming) | ~1000 Python programming tasks | pass@k |
| **APPS** (Automated Programming Progress) | 10,000 competitive programming problems | pass@k, test case accuracy |
| **CodeContests** | Competitive programming (Codeforces, etc.) | pass@k |
| **SWE-bench** | Real GitHub issue resolution | % resolved (patch acceptance) |
| **SWE-bench Multilingual** | Cross-language SWE-bench variants | % resolved |
| **DS-1000** | Data science / library-specific coding | pass@k |
| **BigCodeBench** | Diverse programming tasks with constraints | pass@k, exact match |
| **CRUXEval** | Code execution reasoning | Output prediction accuracy |
| **CodeReviewEval** | Automated code review quality | Accuracy, precision/recall of issues found |
| **DeepFix** / **DrRepair** | Program repair / bug fixing | Fix rate, exact match |

**Common Metrics:** pass@k, functional correctness, test case pass rate, exact match, BLEU (for comments/docs)

### 9. Math

| Benchmark | Description | Typical Metrics |
|-----------|-------------|-----------------|
| **GSM8K** | Grade-school math word problems (arithmetic) | Accuracy, exact match |
| **MATH** | Competition-level (AIME/AMC) problems | Accuracy |
| **SVAMP** | Simple math word problems with variations | Accuracy |
| **MAWPS** | Math word problem collection | Accuracy |
| **MultiArith** | Multi-step arithmetic word problems | Accuracy |
| **AQuA** | Algebraic word problems (SAT-level) | Accuracy |
| **NumGLUE** | Numerical reasoning across 8 tasks | Accuracy, exact match |
| **ProofNet** | Formal mathematical proofs (Lean/Coq) | Proof completion rate |
| **MiniF2F** | Formal-to-formal math proof translation | Accuracy (proof checking) |
| **DeepMind Math** | Arithmetic via chain-of-thought | Accuracy, step correctness |

**Common Metrics:** Accuracy, exact match, pass@k, proof completion rate

### 10. Medical

| Benchmark | Description | Typical Metrics |
|-----------|-------------|-----------------|
| **MedQA** (USMLE) | US medical licensing exam (multiple-choice) | Accuracy |
| **MedMCQA** | Indian medical entrance exam QA | Accuracy |
| **PubMedQA** | Biomedical research QA | Accuracy, F1 |
| **BioASQ** | Biomedical semantic QA | Accuracy, F1, SOTA recall |
| **ClinicalBERT / BioBERT eval** | Clinical NER, relation extraction | F1, precision, recall |
| **Med-PaLM evaluations** | Long-form clinical QA safety/alignment | Clinician preference, factuality |
| **DDInter** | Drug-drug interaction prediction | F1, accuracy, AUROC |
| **DiagnosisBench** | Differential diagnosis generation | Accuracy, recall@k |
| **MedUnderstanding** | Radiology report understanding | ROUGE, BLEU, factual accuracy |
| **ChatDoctor** | Patient-doctor dialogue | Human evaluation, BLEU |

**Common Metrics:** Accuracy, F1, ROUGE, clinician evaluation, factual consistency

### 11. Legal

| Benchmark | Description | Typical Metrics |
|-----------|-------------|-----------------|
| **CaseHOLD** | Legal holdings identification | Accuracy |
| **LexGLUE** | Legal GLUE (6 legal NLU tasks) | Accuracy, F1 |
| **ECHR** (European Court of Human Rights) | Case outcome prediction | Accuracy |
| **COLIEE** | Legal document retrieval and entailment | R precision, F1 |
| **CUAD** (Contract Understanding Atticus Dataset) | Contract clause QA / risk identification | F1, AUPR |
| **LegalBERT evaluations** | Legal NER, classification | F1 |
| **Overruling** | Case law overruling detection | F1, accuracy |
| **NLLP** (NLP for Legal Purposes) | Statute/regulation QA | Accuracy, F1 |
| **MultiLegalPile** | Multi-jurisdictional legal text understanding | F1, accuracy |

**Common Metrics:** Accuracy, F1, AUPR, precision, recall

### 12. Finance

| Benchmark | Description | Typical Metrics |
|-----------|-------------|-----------------|
| **FinQA** | Financial report QA with numerical reasoning | Exact match, program accuracy |
| **ConvFinQA** | Conversational financial QA | Exact match, F1 |
| **TAT-QA** | Table-and-text financial QA | Exact match, F1 |
| **FiQA SA** (Sentiment Analysis) | Financial news sentiment classification | Accuracy, F1 (macro) |
| **NER-Finance** | Financial named entity recognition | F1, precision, recall |
| **EDGAR Corpus** | SEC filing analysis / summarization | ROUGE, factual consistency |
| **FinBen** | 35 financial tasks across 11 categories | Task-specific metrics |
| **BloombergGPT evaluations** | Financial classification, QA, sentiment | Accuracy, F1 |
| **AlphaFactor** | Financial reasoning (forecasting logic) | Accuracy, directional accuracy |

**Common Metrics:** Exact match, F1, ROUGE, accuracy, program accuracy

### 13. Multilingual

| Benchmark | Description | Typical Metrics |
|-----------|-------------|-----------------|
| **XTREME** (Cross-lingual TRansfer Evaluation of Multilingual Encoders) | 9 tasks across 40 languages | Accuracy, F1, exact match |
| **XTREME-R** | XTREME + 10 more tasks, additional languages | Accuracy, F1 |
| **XGLUE** | Cross-lingual GLUE benchmark | Accuracy, F1 |
| **WMT** (Workshop on Machine Translation) | Translation quality across language pairs | BLEU, chrF++, COMET, TER |
| **FLORES-200** | Translation evaluation for 200+ languages | BLEU, chrF, spBLEU |
| **Belebele** | Reading comprehension in 122 languages | Accuracy |
| **MASSIVE** | Multilingual NLU (51 languages) | Accuracy, F1 |
| **TyDiQA** | Typologically diverse QA (11 languages) | F1, exact match |
| **MLQA** | Multi-lingual QA across 7 languages | F1, exact match |
| **WikiAnn** | Cross-lingual NER | F1 |
| **Tatoeba** | Sentence retrieval / translation pairs | Accuracy |

**Common Metrics:** BLEU, chrF, COMET, Accuracy, F1, exact match

### 14. Multimodal (Vision+Language)

| Benchmark | Description | Typical Metrics |
|-----------|-------------|-----------------|
| **COCO Captions** | Image captioning | BLEU, CIDEr, ROUGE, SPICE, METEOR |
| **Flickr30k** | Image captioning | BLEU, CIDEr, ROUGE, METEOR |
| **NoCaps** | Novel object captioning | CIDEr, BLEU, SPICE |
| **VQA v2** | Visual question answering | Accuracy |
| **VQA (GQA)** | Compositional scene understanding QA | Accuracy, binary accuracy |
| **OK-VQA** | Outside-knowledge VQA | Accuracy |
| **VizWiz** | Blind users' visual QA | Accuracy |
| **DocVQA** | Document visual QA | ANLS (Average Normalized Levenshtein Similarity) |
| **TextVQA** | Text-in-image QA | Accuracy |
| **LLaVA-Bench / MMBench** | Multi-modal instruction following | GPT-4 judge, accuracy |
| **MMMU** (Massive Multidisciplinary Multimodal Understanding) | College-level multi-modal problems | Accuracy |
| **MathVista** | Visual math reasoning | Accuracy |
| **ChartQA** | Chart understanding QA | Accuracy, relaxed accuracy |

**Common Metrics:** CIDEr, BLEU, ROUGE, SPICE, Accuracy, ANLS, GPT-4 evaluation score

---

## Summary: Key Takeaways

1. **HELM (Stanford CRFM)** pioneered multi-metric evaluation: accuracy, calibration, robustness, fairness, bias, toxicity, and efficiency — measured simultaneously across 42+ scenarios.
2. **MMLU** is the most widely adopted general-purpose benchmark, covering 57 subjects.
3. **Coding** evaluations have matured significantly with SWE-bench (real bugs), HumanEval, and MBPP as standards, all using functional correctness (`pass@k`).
4. **Domain-specific** benchmarks (medical, legal, finance) increasingly use real-world expert-annotated data (e.g., USMLE for MedQA, SEC filings for FinQA).
5. **Safety** benchmarks focus on bias (BBQ, StereoSet), toxicity (RealToxicityPrompts), truthfulness (TruthfulQA), and adversarial robustness.
6. **Multilingual** evaluation scales from 7 languages (XTREME) to 200+ (FLORES-200, Belebele).
7. **Multimodal** evaluation is moving from captioning (COCO) to complex visual reasoning (MMMU, MathVista, ChartQA).
8. **Long context** is an emerging dimension with benchmarks like LongBench and SCROLLS testing up to 100k+ token inputs.
9. **Instruction following** is evaluated via automated judges (MT-Bench, AlpacaEval) and constraint-checking (IFEval).
10. **Metrics vary by task**: generative tasks use BLEU/ROUGE/CIDEr; classification/QA uses accuracy/F1; coding uses pass@k; safety uses refusal rates and bias scores.
