# Findings: Common Failure Modes in AI/LLM-Generated Code

> Research compiled from academic studies, OWASP guidelines, and industry analysis.
> Date: 2026-04-29

---

## 1. Security Vulnerabilities (Most Heavily Studied)

### 1.1 Copilot Generates Vulnerable Code ~40% of the Time

**Source:** "Asleep at the Keyboard? Assessing the Security of GitHub Copilot's Code Contributions" — Pearce et al., IEEE S&P 2022 (arXiv:2108.09293)

> *"We prompt Copilot to generate code in scenarios relevant to high-risk CWEs... In total, we produce 89 different scenarios for Copilot to complete, producing 1,689 programs. Of these, we found approximately 40% to be vulnerable."*

Key findings:
- 40% of Copilot-generated programs contained exploitable vulnerabilities
- Tested across 89 scenarios spanning MITRE Top 25 CWEs
- Vulnerabilities appeared across diverse weaknesses, prompts, and domains

### 1.2 AI Assistants Lead Users to Write *Less* Secure Code

**Source:** "Do Users Write More Insecure Code with AI Assistants?" — Perry et al., ACM CCS 2023 (arXiv:2211.03622)

> *"Participants who had access to an AI assistant based on OpenAI's codex-davinci-002 model wrote significantly less secure code than those without access."*

> *"Participants with access to an AI assistant were more likely to believe they wrote secure code than those without access."*

This creates a **double risk**: AI-generated code is more vulnerable, AND developers are **overconfident** about its security, making them less likely to review or test thoroughly.

> *"Participants who trusted the AI less and engaged more with the language and format of their prompts provided code with fewer security vulnerabilities."*

### 1.3 Most Common Vulnerability Types in AI-Generated Code

Based on the Pearce et al. study and Copilot's own disclosure:
- **Hardcoded credentials** (CWE-798)
- **SQL injection** (CWE-89)
- **Path injection / path traversal** (CWE-22)
- Buffer overflows
- OS command injection
- Improper input validation
- Insecure cryptographic practices

GitHub Copilot's own documentation acknowledges: *"Public code may contain insecure coding patterns, bugs, or references to outdated APIs or idioms. When GitHub Copilot synthesizes code suggestions based on this data, it can also synthesize code that contains these undesirable patterns."*

---

## 2. Logic Errors and Reasoning Failures

### 2.1 LLMs Cannot Truly Perform Compositional Reasoning

**Source:** "Faith and Fate: Limits of Transformers on Compositionality" — Dziri et al., NeurIPS 2023 (arXiv:2305.18654)

> *"Transformer LLMs solve compositional tasks by reducing multi-step compositional reasoning into linearized subgraph matching, without necessarily developing systematic problem-solving skills."*

> *"Autoregressive generations' performance can rapidly decay with increased task complexity."*

This means AI-generated code tends to fail on problems requiring:
- Multi-step logical chaining
- Multi-digit arithmetic (e.g., multiplication of large numbers)
- Dynamic programming
- Complex state management
- Non-trivial algorithmic composition

The model matches patterns rather than reasoning through problems. When the required computation exceeds what can be matched from training data, performance degrades rapidly.

### 2.2 Hallucinated APIs and Non-Existent Functions

LLMs frequently generate calls to:
- Library functions that do not exist
- Incorrect method signatures for real functions
- Deprecated or removed APIs
- Imaginary parameters
- Non-existent modules/packages

This is because the model probabilistically assembles tokens that *look like* plausible API calls without any grounding in actual documentation or runtime behavior.

### 2.3 Off-by-One and Boundary Errors

AI models frequently produce:
- Off-by-one errors in loops and array access
- Incorrect handling of edge cases (empty inputs, null values, single-element collections)
- Missing bounds checks
- Integer overflow vulnerabilities
- Incorrect comparison operators (using `=` instead of `==`, or `>` instead of `>=`)

---

## 3. OWASP Top 10 for LLM Applications (2025)

**Source:** OWASP GenAI Security Project (genai.owasp.org)

These are risks that specifically affect applications that USE or are BUILT WITH LLMs:

| Rank | Risk | Relevance to Code Generation |
|------|------|------------------------------|
| LLM01 | Prompt Injection | Attackers can manipulate prompts to produce malicious code |
| LLM02 | Sensitive Information Disclosure | LLMs may leak training data secrets into generated code |
| LLM03 | Supply Chain | AI-generated code may introduce vulnerable dependencies |
| LLM04 | Data and Model Poisoning | If training data is poisoned, generated code inherits the flaws |
| LLM05 | Improper Output Handling | Code output from LLMs used without validation is dangerous |
| LLM06 | Excessive Agency | Autonomous coding agents with too much freedom can cause damage |
| LLM07 | System Prompt Leakage | System instructions leaked to users |
| LLM08 | Vector and Embedding Weaknesses | RAG-based code generation can retrieve bad examples |
| LLM09 | Misinformation | LLMs may hallucinate APIs, algorithms, or security practices |
| LLM10 | Unbounded Consumption | Runaway code generation loops, resource exhaustion |

---

## 4. Anti-Patterns and Quality Issues

### 4.1 Boilerplate Bloat
- Generating unnecessarily verbose code
- Repeating identical patterns instead of extracting functions
- Over-engineering simple solutions

### 4.2 Missing Error Handling
- No try/catch or error propagation
- Silent failure modes
- Incorrect exception types
- No input validation

### 4.3 Poor Testing Patterns
- Tests that assert tautologies (e.g., `assert True`)
- Tests that don't actually test the behavior described
- Fragile tests tied to implementation details
- Incomplete test coverage — only happy paths

### 4.4 Inconsistent Style and Conventions
- Mixing naming conventions (snake_case + camelCase)
- Inconsistent indentation
- Improper use of language idioms
- Copy-paste from different codebases with incompatible patterns

### 4.5 Dependency Management Issues
- Suggesting outdated or deprecated packages
- Missing dependency declarations
- Incorrect version specifiers
- Using libraries with known vulnerabilities

---

## 5. Differences Between AI-Generated and Human-Written Code

| Dimension | Human-Written Code | AI-Generated Code |
|-----------|-------------------|-------------------|
| Error distribution | Concentrated in complex/new logic | Evenly distributed; also fails on simple tasks |
| Security posture | Developers can explain rationale | Overconfidence in security leads to less review |
| API usage | Real, tested integrations | Hallucinated or plausible-but-wrong APIs |
| Edge cases | Experienced humans handle common ones | Often misses edge cases entirely |
| Consistency | Generally follows project conventions | May mix conventions from different sources |
| Reasoning | Genuine understanding of trade-offs | Pattern-matching without understanding |
| Testing | Varies by discipline | Often generates tautological or shallow tests |

---

## 6. Testing Strategies for AI-Generated Code

Based on the research findings, the following strategies are recommended:

1. **Do not trust AI-generated code.** Treat it as you would code from an unfamiliar junior developer.
2. **Always run static analysis / SAST.** Tools like CodeQL, SonarQube, or Semgrep catch most injection and cryptographic vulnerabilities that AIs commonly introduce.
3. **Verify every API call.** Assume function signatures may be hallucinated. Check documentation.
4. **Test edge cases explicitly.** AI is poor at handling null inputs, empty collections, boundary values, and error states.
5. **Review for logic errors manually.** AI-generated algorithmic code requires human review — the model did not actually reason through the problem.
6. **Use AI to generate tests for human-written code (not the reverse).** Tests generated by AI for AI code compound the trust problem — both may share the same blind spots.
7. **Fuzz AI-generated functions.** Fuzz testing catches the kinds of boundary and input-validation issues AIs tend to miss.
8. **Check for hardcoded secrets.** Use secret scanning (e.g., GitGuardian, truffleHog) on AI-generated code aggressively.

---

## 7. Summary of Key Facts

| Stat | Source |
|------|--------|
| ~40% of Copilot code contributions contained vulnerabilities | Pearce et al. 2022 |
| AI-assistant users wrote *less* secure code | Perry et al. 2023 |
| AI-assistant users were *more likely* to believe code was secure | Perry et al. 2023 |
| LLMs match patterns, don't perform systematic reasoning | Dziri et al. 2023 |
| Top common vulns: hardcoded creds, SQLi, path traversal | Pearce et al. 2022 |
| Performance decays rapidly with task complexity | Dziri et al. 2023 |
| OWASP LLM Top 10 includes Prompt Injection, Supply Chain, Misinformation | OWASP 2025 |

---

## Source URLs

1. Pearce et al., "Asleep at the Keyboard? Assessing the Security of GitHub Copilot's Code Contributions" — https://arxiv.org/abs/2108.09293
2. Perry et al., "Do Users Write More Insecure Code with AI Assistants?" — https://arxiv.org/abs/2211.03622
3. Dziri et al., "Faith and Fate: Limits of Transformers on Compositionality" — https://arxiv.org/abs/2305.18654
4. OWASP Top 10 for LLM Applications (2025) — https://genai.owasp.org/llm-top-10/
5. GitHub Copilot Features & FAQ — https://github.com/features/copilot
