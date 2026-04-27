# Findings: Inherent Task Characteristics That Determine AI Suitability

## Background: The Three-Axis Framework

Paras Chopra's original framework proposes three orthogonal axes for evaluating AI task suitability:
1. **Ease of building a verifier** — how easy it is to check whether the AI's output is correct
2. **Causal complexity** — the number of confounding variables and difficulty of establishing cause-effect
3. **Economic attractiveness** — whether the economics of automation justify the investment

This research identifies **10 additional dimensions** that influence task suitability for AI, drawing on labor economics, cognitive science, and AI safety research.

---

## Dimension 1: Data Availability & Quality Requirements

### Key Insight
AI systems are fundamentally pattern recognizers. A task is more suitable for AI when high-quality, labeled, representative training data exists in sufficient quantity.

### Spectrum
- **AI-favorable**: Tasks with abundant historical data (credit scoring, language translation, ad targeting)
- **AI-unfavorable**: Tasks with scarce, proprietary, or rapidly changing data (early-stage scientific discovery, niche crafts, emerging market analysis)

### Key Facts
- The OpenAI GPTs are GPTs paper found that ~80% of the U.S. workforce could have at least 10% of tasks affected by LLMs, but this assumes the availability of sufficient training data across domains (Eloundou et al., 2023).
- Data-hungry deep learning approaches require orders of magnitude more examples than human learners to reach comparable performance — a task requiring few-shot or zero-shot generalization remains harder for AI even with large pre-training.

> "around 80% of the U.S. workforce could have at least 10% of their work tasks affected by the introduction of LLMs, while approximately 19% of workers may see at least 50% of their tasks impacted"
> — *Eloundou, Manning, Mishkin & Rock, "GPTs are GPTs," arXiv:2303.10130*

**Source**: https://arxiv.org/abs/2303.10130

---

## Dimension 2: Physical Dexterity & Robotics Integration

### Key Insight
Moravec's paradox states that tasks requiring sensorimotor skills (perception, mobility, manipulation) are paradoxically harder for AI than tasks requiring abstract reasoning, because the former have been optimized by hundreds of millions of years of evolution.

### Spectrum
- **AI-favorable**: Purely digital/information tasks (data entry, code generation, text summarization)
- **AI-unfavorable**: Tasks requiring fine motor manipulation, unstructured physical environments, or real-time physical interaction (surgery, plumbing, child care)

### Key Facts
- Hans Moravec (1988): "it is comparatively easy to make computers exhibit adult level performance on intelligence tests or playing checkers, and difficult or impossible to give them the skills of a one-year-old when it comes to perception and mobility."
- Steven Pinker (1994): "the main lesson of thirty-five years of AI research is that the hard problems are easy and the easy problems are hard."
- Rodney Brooks noted that early AI research mistakenly defined intelligence as "the things that highly educated male scientists found challenging" while ignoring sensorimotor capabilities that even children master.
- Andrew Ng's (2017) rule of thumb: "almost anything a typical human can do with less than one second of mental thought, we can probably now or in the near future automate using AI."

> "Encoded in the large, highly evolved sensory and motor portions of the human brain is a billion years of experience about the nature of the world and how to survive in it."
> — *Hans Moravec, "Mind Children" (1988)*

**Source**: https://en.wikipedia.org/wiki/Moravec%27s_paradox

---

## Dimension 3: Social Intelligence & Emotional Labor

### Key Insight
Tasks requiring genuine empathy, trust-building, negotiation, reading non-verbal cues, or managing human emotions are difficult for AI. AI can *simulate* empathy but cannot *experience* it, which matters for tasks where authentic human connection is central.

### Spectrum
- **AI-favorable**: Scripted customer service, information delivery, standardized counseling
- **AI-unfavorable**: Psychotherapy, end-of-life care, conflict mediation, team motivation, leadership

### Key Facts
- HBR's Collaborative Intelligence research (Wilson & Daugherty, 2018) found that humans and AI work best when human strengths (creativity, empathy, judgment) are augmented by AI strengths (scale, speed, pattern recognition) rather than replaced.
- The most automation-resistant roles tend to involve high levels of social intelligence, negotiation, and care work — which are difficult to codify into algorithms.

> "Never before have digital tools been so responsive to us, nor we to our tools. While AI will radically alter how work gets done and who does it, the technology's larger impact will be in complementing and augmenting human capabilities, not replacing them."
> — *H. James Wilson & Paul R. Daugherty, "Collaborative Intelligence," Harvard Business Review (2018)*

**Source**: https://hbr.org/2018/07/collaborative-intelligence-humans-and-ai-are-joining-forces

---

## Dimension 4: Stakes of Failure / Safety-Criticality

### Key Insight
When the cost of a mistake is very high, the bar for AI adoption rises dramatically — even if the AI performs well on average. High-stakes tasks demand explainability, reliability guarantees, and often human-in-the-loop oversight.

### Spectrum
- **AI-favorable**: Low-stakes, high-volume tasks (content recommendations, spam filtering, movie subtitling)
- **AI-unfavorable**: Life-critical or legally consequential decisions (medical diagnosis, criminal sentencing, aircraft control, nuclear reactor management)

### Key Facts
- Autonomous systems in safety-critical domains require extensive validation, certification, and regulatory approval — processes that can take years or decades longer than deployment in low-stakes contexts.
- A key unresolved problem is distributional shift: an AI that performs perfectly in training may fail catastrophically in edge cases that were not anticipated during development.
- The "verifier" dimension from the original 3-axis framework is closely related — when stakes are high, the verifier must be near-perfect, which dramatically raises the bar.

---

## Dimension 5: Need for Creativity & Novelty Generation

### Key Insight
Tasks requiring genuine novelty — not just recombination of existing patterns but true out-of-distribution invention — remain difficult for current AI. Current LLMs excel at *synthesis and recombination* but struggle with *genuine conceptual innovation*.

### Spectrum
- **AI-favorable**: Pattern completion, variation generation, style imitation (copywriting, logo variations, music in an existing style)
- **AI-unfavorable**: Paradigm-shifting scientific theories, artistic movements that break conventions, novel business models

### Key Facts
- Current AI systems (including LLMs) are fundamentally next-token predictors — they generate output that is statistically plausible given their training distribution. This makes them inherently conservative; they cannot easily produce output that genuinely diverges from the training distribution.
- Creative tasks that involve defining new problem spaces or new evaluation criteria are harder for AI. AI can generate many candidates, but human judgment is typically still needed for selecting and refining genuinely novel ideas.

---

## Dimension 6: Decision Frequency & Scale

### Key Insight
Tasks requiring high-volume, repeated decisions with clear feedback loops are naturally suited to AI because the cost of development can be amortized across millions of decisions and the AI can continuously improve.

### Spectrum
- **AI-favorable**: High-frequency decisions with fast feedback (ad bidding, fraud detection, routing, inventory management)
- **AI-unfavorable**: Low-frequency, high-impact strategic decisions (CEO acquisitions, constitutional rulings, rare medical diagnoses)

### Key Facts
- The economic attractiveness axis from the original framework interacts strongly here: high-frequency tasks offer more data for training, more opportunities for iteration, and better return on automation investment.
- "Thin" AI applications (single task, high volume) have a much higher success rate than attempts to build general-purpose "thick" AI that can handle many different decisions.

---

## Dimension 7: Need for Explainability & Regulatory Compliance

### Key Insight
Tasks operating under legal or regulatory frameworks that require auditable, explainable decision-making face higher barriers for AI adoption. Black-box models may perform well but cannot be deployed if regulations require reasoning transparency.

### Spectrum
- **AI-favorable**: Low-regulation domains, internal-facing tools, discretionary recommendations (entertainment recommendations, internal analytics)
- **AI-unfavorable**: Regulated industries (finance, healthcare, law, hiring, credit), public sector decisions, any domain covered by "right to explanation" laws

### Key Facts
- GDPR's "right to explanation" clause, Fair Lending laws, and similar regulations create legal requirements for explainability that many high-performing AI models (especially deep neural networks) cannot satisfy.
- The "ease of building a verifier" axis from the original framework is related but distinct: a verifier checks correctness; explainability requires tracing *how* the decision was reached, which is harder.
- Regulatory compliance costs for AI in finance and healthcare can be prohibitive for all but the largest organizations.

---

## Dimension 8: Domain Specificity vs. Generality

### Key Insight
Narrow, well-bounded domains are easier for AI to master because the input space, output space, and success criteria are clearly defined. General-purpose tasks that require spanning multiple domains or adapting to novel contexts are harder.

### Spectrum
- **AI-favorable**: Narrow, well-scoped domains (chess, Go, legal document review, radiology image classification, tax filing)
- **AI-unfavorable**: Broad, cross-domain tasks that require integrating multiple knowledge areas (general management, parenting, political leadership)

### Key Facts
- Deep Blue (chess) and AlphaGo (Go) achieved superhuman performance in narrow domains long before AI approached human-level performance on broader tasks.
- LLMs blur this line somewhat — they show surprising generality across tasks — but they still struggle with tasks requiring deep integration of specialized knowledge from disparate domains, or tasks requiring sustained multi-step reasoning (e.g., complex mathematical proofs, long-horizon planning).

---

## Dimension 9: Speed Requirements (Real-Time vs. Batch)

### Key Insight
Tasks with real-time or low-latency requirements constrain the types of AI models that can be deployed. Complex models (large ensembles, deep networks with heavy compute) may be infeasible when sub-second response is required.

### Spectrum
- **AI-favorable**: Batch processing, offline analysis, latency-tolerant tasks (fraud detection with minutes of delay, periodic reporting, asynchronous translation)
- **AI-unfavorable**: Hard real-time control systems (anti-lock braking, flight control, high-frequency trading), tasks requiring immediate interactive response with complex reasoning

### Key Facts
- Real-time constraints often force trade-offs between model accuracy and inference speed. Simpler, faster models may be used in production even when more accurate but slower models exist.
- Edge deployment (on-device AI) adds additional constraints: model size, power consumption, and compute capacity all limit what is feasible for real-time tasks running on local hardware.
- Latency requirements are particularly binding for robotics and autonomous systems, where control loops must run at millisecond-level frequencies.

---

## Dimension 10: Need for Common Sense / World Knowledge

### Key Insight
Tasks that rely on broad common-sense reasoning about the physical and social world — things "everyone knows" — are surprisingly difficult for AI. This is related to the frame problem and the qualification problem in AI.

### Spectrum
- **AI-favorable**: Tasks where domain knowledge is fully specified and self-contained (formal logic, programming languages, chess)
- **AI-unfavorable**: Tasks requiring implicit understanding of physical causality, social norms, or unstated assumptions (housekeeping, event planning, social etiquette, understanding sarcasm)

### Key Facts
- LLMs have made significant progress on this front by absorbing massive amounts of text from the web, which encodes a great deal of common-sense knowledge implicitly. However, they still make absurd errors (hallucinations) that reveal a lack of genuine world understanding.
- The distinction between *statistical pattern matching* and *genuine understanding* matters here: an AI can produce text that *looks* like it has common sense without actually possessing the causal models that underpin genuine common-sense reasoning.
- Tasks requiring physical common sense (e.g., "if I push this cup off the table, what happens?") were historically very hard for AI; progress with multimodal models is improving this, but robustness remains an issue.

> Toolformer (Schick et al., 2023) shows that LMs "struggle with basic functionality, such as arithmetic or factual lookup, where much simpler and smaller models excel" — and proposes teaching LMs to use external tools to compensate for these gaps.
> — *Schick et al., "Toolformer: Language Models Can Teach Themselves to Use Tools," arXiv:2302.04761*

**Source**: https://arxiv.org/abs/2302.04761

---

## Synthesis: A Multi-Dimensional Framework

The original 3-axis framework (ease of verifier, causal complexity, economic attractiveness) remains a useful starting point, but these 10 additional dimensions substantially expand the analysis:

| Dimension | Makes Task MORE Suitable for AI | Makes Task LESS Suitable for AI |
|---|---|---|
| Data availability | Abundant, labeled, stable data | Scarce, unlabeled, shifting data |
| Physical dexterity | Purely digital/information work | Physical manipulation in unstructured environments |
| Social intelligence | Task can be done without empathy | Requires authentic human connection |
| Stakes of failure | Low cost of errors; reversible | Life-critical; irreversible consequences |
| Creativity type | Recombination within known styles | Paradigm-breaking conceptual novelty |
| Decision frequency | High volume, fast feedback | Rare, strategic, high-impact decisions |
| Explainability need | No regulatory transparency requirement | Legally mandated explainability |
| Domain scope | Narrow, well-bounded domain | Cross-domain integration |
| Speed requirement | Batch or latency-tolerant | Hard real-time constraints |
| Common sense | Domain fully and formally specified | Relies on implicit world knowledge |

These dimensions interact with each other and with the original 3 axes. For example:
- **High stakes + low explainability** is a particularly difficult combination (autonomous driving, medical AI).
- **Low data + high causal complexity** makes a task nearly impossible for current AI (early-stage drug discovery).
- **High frequency + easy verifier + low stakes** is the sweet spot for AI adoption (ad placement, content moderation).

---

## Sources

1. Eloundou, T., Manning, S., Mishkin, P., & Rock, D. (2023). *GPTs are GPTs: An Early Look at the Labor Market Impact Potential of Large Language Models*. arXiv:2303.10130.
   - https://arxiv.org/abs/2303.10130

2. Wilson, H.J. & Daugherty, P.R. (2018). *Collaborative Intelligence: Humans and AI Are Joining Forces*. Harvard Business Review.
   - https://hbr.org/2018/07/collaborative-intelligence-humans-and-ai-are-joining-forces

3. Schick, T., Dwivedi-Yu, J., Dessi, R., Raileanu, R., Lomeli, M., Zettlemoyer, L., Cancedda, N., & Scialom, T. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools*. arXiv:2302.04761.
   - https://arxiv.org/abs/2302.04761

4. Moravec, H. (1988). *Mind Children*. Harvard University Press. (Via Wikipedia: Moravec's paradox)
   - https://en.wikipedia.org/wiki/Moravec%27s_paradox

5. Pinker, S. (1994/2007). *The Language Instinct*. Harper. (Via Wikipedia: Moravec's paradox)
   - https://en.wikipedia.org/wiki/Moravec%27s_paradox

6. Brooks, R. (2002). *Flesh and Machines*. Pantheon Books. (Via Wikipedia: Moravec's paradox)
   - https://en.wikipedia.org/wiki/Moravec%27s_paradox
