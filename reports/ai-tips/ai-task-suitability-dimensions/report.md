# AI Task Suitability: An Expanded Dimensional Framework

## Source Article Analysis
**"What domains will be the last ones to get automated from AI?"** — Paras Chopra, Inverted Passion (April 2026)
URL: https://invertedpassion.com/what-domains-will-be-the-last-ones-to-get-automated-from-ai/

---

## 1. The Original 3-Axis Framework (Paras Chopra)

The article proposes three orthogonal axes for evaluating which domains AI will automate and in what order:

### Axis 1: Ease of Building a Verifier
How easy is it to check whether the AI's output is correct?
- **Easy** (e.g., coding — compilation/tests verify correctness) → automated first
- **Hard** (e.g., lab equipment manipulation — requires expensive instrumentation to verify) → automated last

### Axis 2: Causal Complexity / Number of Confounds
How many confounding variables affect the outcome?
- **Low** (e.g., math problems — answers don't depend on external factors) → automated first
- **High** (e.g., startup success — depends on many random, interconnected factors) → automated last

### Axis 3: Economic Attractiveness
Is there sufficient economic incentive to invest in automation?
- **High** (e.g., coding — massive market, clear ROI) → automated first
- **Low** (e.g., niche domains with small markets) → automated last

### Key Insight
Domains where all three axes align favorably — easy to verify, low causal complexity, high economic attractiveness — are automated first. Coding is the canonical example. The thesis predicts a sequence of automation as companies exhaust each "next best" domain.

---

## 2. Additional Dimensions (Expanded Framework)

Based on research across labor economics, AI capability research, and human-AI collaboration literature, I identify **13 additional dimensions** that complement and extend Chopra's framework:

### Dimension 4: Data Availability & Quality
A task is more suitable for AI when high-quality, labeled, representative training data exists in sufficient quantity.
- **AI-favorable**: Abundant historical data (credit scoring, translation, ad targeting)
- **AI-unfavorable**: Scarce, proprietary, or rapidly shifting data (early scientific discovery, niche crafts, emerging markets)
- *Source: Eloundou et al., "GPTs are GPTs" (arXiv:2303.10130)*

### Dimension 5: Physical Dexterity Requirement (Moravec's Paradox)
Sensorimotor skills are paradoxically harder for AI than abstract reasoning.
- **AI-favorable**: Purely digital/information tasks (data entry, code gen, text)
- **AI-unfavorable**: Fine motor manipulation, unstructured physical environments (surgery, plumbing, childcare)
- *Source: Moravec, "Mind Children" (1988)*

### Dimension 6: Social Intelligence & Emotional Labor
Tasks needing genuine empathy, trust-building, or reading non-verbal cues resist automation.
- **AI-favorable**: Scripted customer service, information delivery
- **AI-unfavorable**: Psychotherapy, end-of-life care, conflict mediation
- *Source: Wilson & Daugherty, HBR "Collaborative Intelligence" (2018)*

### Dimension 7: Stakes of Failure / Safety-Criticality
When errors are costly, the bar for AI adoption rises dramatically.
- **AI-favorable**: Low-stakes, high-volume tasks (spam filtering, recommendations)
- **AI-unfavorable**: Life-critical decisions (medical diagnosis, criminal sentencing, aircraft control)

### Dimension 8: Creativity Type (Recombination vs. Paradigm Shift)
Genuine conceptual novelty remains difficult for pattern-matching AI.
- **AI-favorable**: Style imitation, variation generation (copywriting, logo variations)
- **AI-unfavorable**: Paradigm-shifting theories, convention-breaking art, novel business models

### Dimension 9: Decision Frequency & Feedback Speed
High-frequency decisions with fast feedback loops enable AI learning and amortize development cost.
- **AI-favorable**: High volume, fast feedback (ad bidding, fraud detection, routing)
- **AI-unfavorable**: Rare, strategic decisions (CEO acquisitions, constitutional rulings)

### Dimension 10: Need for Explainability & Regulatory Compliance
Black-box models cannot be deployed where "right to explanation" laws apply.
- **AI-favorable**: Low-regulation, internal tools (entertainment recs, internal analytics)
- **AI-unfavorable**: Regulated industries (finance, healthcare, law, hiring, credit decisions)

### Dimension 11: Domain Specificity vs. Generality
Narrow, well-bounded domains are easier to master than cross-domain integration.
- **AI-favorable**: Narrow, scoped domains (chess, radiology, tax filing, legal doc review)
- **AI-unfavorable**: Cross-domain tasks (general management, parenting, political leadership)

### Dimension 12: Speed Requirement (Real-Time vs. Batch)
Real-time constraints limit model complexity and deployment options.
- **AI-favorable**: Batch, offline, latency-tolerant (periodic reporting, async translation)
- **AI-unfavorable**: Hard real-time control (ABS braking, flight control, high-frequency trading)

### Dimension 13: Need for Common Sense / World Knowledge
Tasks relying on implicit understanding of the physical/social world are surprisingly hard.
- **AI-favorable**: Fully specified formal domains (programming languages, formal logic, chess)
- **AI-unfavorable**: Implicit world knowledge (housekeeping, event planning, understanding sarcasm)
- *Source: Schick et al., "Toolformer" (arXiv:2302.04761)*

### Dimension 14: Tacit Knowledge Requirement (Polanyi's Paradox)
Tasks depending on knowledge the practitioner cannot fully articulate resist automation.
- **AI-favorable**: Codifiable, rule-based, explicit
- **AI-unfavorable**: Intuitive, experience-based, tacit ("we know more than we can tell")
- *Source: Autor, "Polanyi's Paradox and the Shape of Employment Growth" (2014)*

### Dimension 15: Task Routineness (ALM Framework)
The classic labor economics taxonomy predicts substitution vs. complementarity.
- **Routine cognitive/manual** → HIGH automation suitability (bookkeeping, assembly line)
- **Non-routine cognitive (analytical/interpersonal)** → LOW automation suitability (problem-solving, managing)
- **Non-routine manual** → LOW-MEDIUM (cleaning, driving in traffic)
- *Source: Autor, Levy, Murnane (2003)*

### Dimension 16: Human-AI Interaction Mode
Not every task should be automated — some are best done with human-AI complementarity.
- **Full automation**: Well-defined, repetitive, low-stakes, high-volume
- **Augmentation**: Pattern recognition + human judgment (radiology, code review)
- **Human-only**: Moral reasoning, genuine empathy, novel edge cases, accountability-critical
- *Source: Pew Research (2022), HITL literature*

---

## 3. Synthesis: How These Dimensions Interact

### Sweet Spot for AI (the "low-hanging fruit")
Tasks scoring favorably on multiple dimensions:
- Easy verifier + Low causal complexity + High data availability + High frequency + Low stakes + Low physical requirement = **ideal for AI now**
- Examples: code generation, translation, ad targeting, content moderation, data entry

### Hard but Reachable (active frontier)
Tasks with mixed scores:
- Moderate verifier + moderate complexity + some data + moderate stakes = **AI making progress**
- Examples: medical imaging triage, legal document review, customer service chatbots, stock trading

### Likely Last to Automate
Tasks scoring poorly on multiple dimensions:
- Hard verifier + High causal complexity + Low/expensive data + High stakes + High tacit knowledge + Physical + Social = **resists automation**
- Examples: novel scientific discovery, psychotherapy, political leadership, general management, childcare, plumbing, fine dining cooking

### Dimension Interaction Effects
- **High stakes + low explainability** = particularly difficult combination (autonomous driving, medical AI)
- **Low data + high causal complexity** = nearly impossible for current AI (early-stage drug discovery)
- **High frequency + easy verifier + low stakes** = the sweet spot for AI adoption (ad placement, content moderation)
- **Low economic attractiveness + hard verifier** = no one will invest in automating it (niche crafts, exotic domains)

---

## 4. Practical Application: Task Evaluation Matrix

To evaluate whether a specific task should be given to AI, score it on a scale of 1-5 across these dimensions:

| Dimension | Score 1 (Give to AI) | Score 5 (Keep Human) |
|---|---|---|
| Verifiability | Easily automated verification | Verification requires human expert |
| Causal complexity | Few confounds, clear cause-effect | Many confounds, unclear causality |
| Economic incentive | Huge market, clear ROI | Tiny market, unclear ROI |
| Data availability | Abundant labeled data | No data / hard to collect |
| Physical dexterity | Purely digital | Unstructured physical environment |
| Social/emotional need | No empathy required | Genuine human connection needed |
| Stakes of failure | Errors are cheap | Errors are catastrophic |
| Creativity type | Recombination within style | Paradigm-breaking novelty |
| Decision frequency | Millions of decisions/day | A few decisions/year |
| Explainability needed | No regulatory constraint | Legally mandated explainability |
| Domain scope | Narrow, bounded | Cross-domain integration required |
| Speed constraint | Batch/low latency OK | Hard real-time required |
| Common sense need | Domain fully formalized | Requires implicit world knowledge |
| Tacit knowledge | Fully codifiable | Practitioner can't articulate it |
| Task routineness | Routine, repetitive | Non-routine, novel |

A low total score → strong candidate for AI automation.
A mid-range score → candidate for human-AI complementarity/augmentation.
A high total score → likely remain human-performed.

---

## Sources

1. Chopra, P. (2026). "What domains will be the last ones to get automated from AI?" Inverted Passion.
   https://invertedpassion.com/what-domains-will-be-the-last-ones-to-get-automated-from-ai/

2. Eloundou, T., Manning, S., Mishkin, P., & Rock, D. (2023). "GPTs are GPTs." arXiv:2303.10130.
   https://arxiv.org/abs/2303.10130

3. Wilson, H.J. & Daugherty, P.R. (2018). "Collaborative Intelligence." Harvard Business Review.
   https://hbr.org/2018/07/collaborative-intelligence-humans-and-ai-are-joining-forces

4. Schick, T. et al. (2023). "Toolformer: Language Models Can Teach Themselves to Use Tools." arXiv:2302.04761.
   https://arxiv.org/abs/2302.04761

5. Autor, D. (2014). "Polanyi's Paradox and the Shape of Employment Growth." NBER.
   https://www.nber.org/papers/w20485

6. Autor, D., Levy, F., & Murnane, R. (2003). "The Skill Content of Recent Technological Change." Quarterly Journal of Economics.

7. Moravec, H. (1988). "Mind Children." Harvard University Press.
   https://en.wikipedia.org/wiki/Moravec%27s_paradox

8. Brookings Institution (2019). "Automation and Artificial Intelligence."
   https://www.brookings.edu/articles/automation-and-artificial-intelligence-how-machines-affect-people-and-places/

9. Pew Research Center (2022). "AI and Human Enhancement."
   https://www.pewresearch.org/internet/2022/03/17/ai-and-human-enhancement-americans-openness-is-tempered-by-a-range-of-concerns/

10. Stanford HAI. "AI Index Report."
    https://hai.stanford.edu/ai-index/2025

11. Davis, F.D. (1989). "Perceived usefulness, perceived ease of use, and user acceptance of information technology." MIS Quarterly.
    https://en.wikipedia.org/wiki/Technology_acceptance_model

12. Venkatesh, V. et al. (2003). "User acceptance of information technology: Toward a unified view." MIS Quarterly.
