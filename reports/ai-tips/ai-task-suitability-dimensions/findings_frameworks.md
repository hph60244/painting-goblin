# Findings: Frameworks for Classifying AI-Suitable vs AI-Unsuitable Tasks

## 1. McKinsey's Automation Potential Framework

McKinsey's framework (cited extensively in Brookings Metro report and McKinsey's own "Where machines could replace humans" research) identifies automation potential along several task dimensions:

- **Technical automation potential** varies by occupation — not whole jobs but individual **tasks** are automated. McKinsey models estimate that ~25% of jobs face "high risk" (>70% of tasks automatable).
- **Five activity categories** used in their capability assessments:
  1. **Physical and manual work** in predictable environments (highly automatable)
  2. **Data processing and collection** (highly automatable)
  3. **Cognitive routine tasks** (highly automatable)
  4. **Applying expertise, problem-solving, creativity** (low automation potential)
  5. **Managing and developing people** (low automation potential)
- Key insight: "Machines substitute for **tasks**, not **jobs**" (Brookings synthesis of McKinsey approach)

**Characteristics of automatable tasks** (per McKinsey methodology):
- Routine, repetitive, predictable
- Codifiable into clear sets of rules
- Occur in structured/predictable environments
- Can be learned from large labelled datasets

**Characteristics of automation-resistant tasks**:
- Require creativity, problem-solving, intuition
- Demand situational adaptability and common sense
- Involve in-person interactions and emotional intelligence
- Require physical dexterity in unstructured environments

*Source: https://www.brookings.edu/articles/automation-and-artificial-intelligence-how-machines-affect-people-and-places/*

---

## 2. Stanford HAI (Human-Centered AI / AI Index Report)

The Stanford Institute for Human-Centered AI publishes an annual **AI Index Report** tracking AI capabilities benchmarks.

**Key observations from Stanford HAI research:**
- AI systems have achieved **superhuman performance** in specific narrow domains: image classification (ImageNet), language understanding (GLUE/SuperGLUE), game-playing (Go, chess, StarCraft)
- But they lag in **generalization, common-sense reasoning, and adaptability** across contexts
- The AI Index tracks benchmarks across: computer vision, natural language processing, robotics, and reasoning — showing a pattern of narrow outperformance vs. broad underperformance

**Capability-appropriate task dimensions from HAI analysis:**
- Tasks with **clear evaluation metrics** and **static environments** are most suitable
- Tasks requiring **cross-domain transfer** remain challenging
- The "last mile" of deployment (real-world variability) remains the hardest

*Source: https://hai.stanford.edu/ai-index/2025 (Stanford HAI landing page)*

---

## 3. Task-Technology Fit (TTF) Models Applied to AI

### Technology Acceptance Model (TAM)
Groundbreaking model by Fred Davis (1989) — the most widely applied IS theory. Two core determinants:

- **Perceived Usefulness (PU)**: "the degree to which a person believes that using a particular system would enhance their job performance"
- **Perceived Ease of Use (PEOU)**: "the degree to which a person believes that using a particular system would be free from effort"

**TAM Extension (TAM2 — Venkatesh & Davis, 2000)** added: social influence processes (subjective norm, voluntariness, image) and cognitive instrumental processes (job relevance, output quality, result demonstrability, perceived ease of use).

### Unified Theory of Acceptance and Use of Technology (UTAUT)
Venkatesh et al. (2003) — integrates eight competing models, achieves Adjusted R² of 69% in explaining behavioral intention to use technology. Four core determinants: performance expectancy, effort expectancy, social influence, and facilitating conditions.

### Relevance to AI task suitability:
- **Job relevance** (TAM2 construct): personal perspective on "the extent to which the target system is suitable for the job"
- **Task fit** (Eason, via Stewart 1986): described in terms of "fit between systems, tasks and job profiles"
- These models consistently suggest AI-tool suitability depends on: how well the AI matches the task's demands (usefulness), how easily it integrates (ease-of-use), and how demonstrably it improves outcomes.

*Sources:*
- *https://en.wikipedia.org/wiki/Technology_acceptance_model*
- *Davis, F.D. (1989) "Perceived usefulness, perceived ease of use, and user acceptance of information technology"*
- *Venkatesh, V. & Davis, F.D. (2000) "A theoretical extension of the technology acceptance model"*

---

## 4. Academic Taxonomies of AI-Suitable vs AI-Unsuitable Tasks

### Key Taxonomy: Routine vs. Non-Routine (Autor, Levy, Murnane — ALM Framework)

ALM (2003) taxonomy categorizes tasks along two axes:

| Type | Characteristics | Automation Suitability |
|------|----------------|----------------------|
| **Routine cognitive** | Rule-based, codifiable (e.g., bookkeeping, clerical) | HIGH |
| **Routine manual** | Repetitive physical (e.g., assembly line) | HIGH |
| **Non-routine cognitive (analytical)** | Problem-solving, creativity, persuasion | LOW (complemented) |
| **Non-routine cognitive (interpersonal)** | Managing, negotiating, caring | LOW (complemented) |
| **Non-routine manual** | Physical adaptability, situational (e.g., cleaning, driving in traffic) | LOW-MEDIUM |

### Autor's "Polanyi's Paradox" extension (2014):
- Tasks requiring **tacit knowledge** — knowledge we cannot fully articulate — resist automation
- Two stubbornly resistant categories:
  - **Abstract tasks**: problem-solving, intuition, creativity, persuasion (professional, managerial, technical)
  - **Manual tasks**: situational adaptability, visual recognition, language understanding, in-person interactions (service, laborer)
- Routine tasks (middle-skill, codifiable) have been **substituted** — driving labor market polarization

### Moravec's Paradox:
"It is harder for computers to master low-level physical and cognitive skills that are natural and easy for humans to perform" — Pinker summarized: "The main lesson of 35 years of AI research is that the hard problems are easy and the easy problems are hard."

*Sources:*
- *https://en.wikipedia.org/wiki/Polanyi%27s_paradox*
- *https://www.nber.org/papers/w20485 (Autor, 2014)*
- *Autor, D. (2014) "Polanyi's Paradox and the Shape of Employment Growth"*

---

## 5. Polanyi's Paradox and Tasks that Resist Automation

**Core statement** (Michael Polanyi, 1966): "We can know more than we can tell."

**The paradox**: Our tacit knowledge of how the world works often exceeds our explicit understanding. Tasks relying on tacit knowledge — which cannot be fully codified — resist automation by rule-based systems.

**David Autor's formulation (2014):**
> "The challenges to substituting machines for workers in tasks requiring adaptability, common sense, and creativity remain immense. Contemporary computer science seeks to overcome Polanyi's paradox by building machines that learn from human examples, thus inferring the rules that we tacitly apply but do not explicitly understand."

**Three dynamics determining automation impact** (per Autor/Brookings synthesis):
1. What technology doesn't replace, it *complements* — workers whose tasks are complemented benefit
2. Wages depend on ease of filling roles in demand — higher barriers to entry = larger wage gains for complemented tasks
3. Job quantity is shaped by complex interaction of price, quality, and wealth changes from automation

**Modern ML's attempt to overcome the paradox** (Susskind, 2017):
- Deep learning systems (like AlphaGo) infer tacit rules from data rather than relying on human-coded rules
- But these systems remain: **brittle** (fail on distribution shift), **data-hungry**, **uninterpretable**, and **narrow** (single-task)

**Broader implications for AI task suitability:**
A general principle emerges: **the more a task depends on knowledge the practitioner cannot fully articulate to another human, the harder it is to automate** — even with modern ML. Tasks that survive automation are those requiring:
- Situational judgment in unstructured environments
- Interpersonal trust and emotional labour
- Physical adaptability (Moravec's paradox)
- Cross-domain integration

*Sources:*
- *https://en.wikipedia.org/wiki/Polanyi%27s_paradox*
- *https://www.nber.org/papers/w20485*
- *Brookings Institution (2019) "Automation and Artificial Intelligence: How machines are affecting people and places"*

---

## Summary: Cross-Cutting Dimensions for AI Task Suitability

Across all five frameworks, these dimensions consistently predict AI suitability:

| Dimension | AI-Suitable | AI-Unsuitable |
|-----------|-------------|---------------|
| **Codifiability** | Explicit, rule-based, codifiable | Tacit, intuitive, experience-based |
| **Predictability** | Structured, predictable environment | Unstructured, novel situations |
| **Data availability** | Abundant labelled examples | Sparse or shifting data distributions |
| **Routineness** | Repetitive, same patterns | Creative, one-off, problem-solving |
| **Interpersonal need** | Minimal human interaction | Requires trust, empathy, negotiation |
| **Evaluation clarity** | Clear objective function | Subjective, multi-criteria, conflicting goals |
| **Decontextualization** | Task independent of context | Deeply context-dependent |
| **Physical adaptability** | Stable, controlled physical setup | Unpredictable physical environments |
