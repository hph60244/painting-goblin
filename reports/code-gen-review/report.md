# Effective Methods for Reviewing Coding Agent Output

## Executive Summary

Reviewing AI-generated code requires a fundamentally different approach than reviewing human-written code. AI failure modes are distinct (hallucinated APIs, wrong type contracts, invented edge cases), and research shows developers using AI assistants write **less secure code** while being **more confident** in its security. This report synthesizes findings from academic studies, OWASP guidelines, industry tools, and expert practitioners into a practical review methodology.

---

## The Review Stack: A Layered Approach

The most effective strategy combines **automated tooling** at multiple layers with **structured human review** that understands AI's specific failure modes.

### Layer 1: IDE/Pre-Commit (Real-Time)
- **Tools**: Qodo IDE plugin, CodeRabbit IDE plugin, Semgrep MCP Server
- **What it catches**: Basic issues during write-time — style, types, obvious bugs, security red flags
- **Key insight**: Shift-left to catch AI mistakes before they enter version control

### Layer 2: PR Auto-Review (Gate)
- **Tools**: CodeRabbit, Qodo, GitHub Copilot Code Review
- **What it catches**: Cross-repo impacts, breaking changes, missing tests, complex logic errors
- **Key insight**: Let AI review AI first — then send to humans with pre-filtered results

### Layer 3: Security Scanning
- **Tools**: Semgrep (SAST/SCA/secrets with AI triage), traditional linters
- **What it catches**: ~40% of Copilot-generated programs contain vulnerabilities (Pearce et al. 2022)
- **Key insight**: AI-augmented SAST tools (like Semgrep) reduce false positives by ~80%

### Layer 4: Human Review
- **Scope**: Architectural fit, design decisions, security validation, edge case logic
- **Key insight**: Humans are most effective "on the loop" — building and evolving the review harness

---

## The Human Review Mindset

### The Donkey Persona
Treat the AI as an **eager, inexperienced junior** — well-read but lacking wisdom, stubborn, and unable to admit ignorance. The reviewer is the responsible "parent" who ultimately owns the commit.

### The "On-Call" Litmus Test
> *"If you were on call for the application, at which point would you be ok with deploying a 1,000 or 5,000 LOC change set?"*

Grounds review in real accountability.

### Three-Factor Risk Assessment
| Factor | Questions |
|--------|-----------|
| **Impact** | What's the blast radius? Is the domain critical? |
| **Probability** | Is the problem complex? Was sufficient context available? |
| **Detectability** | How good is the overall safety net (tests, monitors)? |

### The "Stress the Code" Timebox
If debugging an AI suggestion takes more than a few minutes, **regenerate or rewrite** rather than patching broken output.

---

## Structured Review Checklist

### Correctness
- Does the code actually solve the stated problem? (test it, don't assume)
- Are all API calls, library functions, and framework APIs real? (hallucination is common)
- Are edge cases handled? (ask the LLM: "what edge cases am I missing?")
- Are error paths tested, not just happy paths?
- Does the code compile/build without warnings?

### Type Safety & Contracts
- Are types correct and idiomatic? (`String?` vs `String`, `Optional[T]` vs `T`)
- Are null/optional/nil states handled properly?
- Does the code use existing utilities rather than duplicating logic?

### Quality & Simplicity
- Would you be comfortable owning this code long-term?
- Is the code unnecessarily complex? (LLMs frequently over-engineer)
- Is there dead code, unused imports, or unnecessary abstractions?
- Are variable/function names meaningful?

### Security
| Risk | What to check |
|------|---------------|
| Hardcoded credentials | CWE-798 — scan with secret detection |
| SQL injection | CWE-89 — parameterize all queries |
| Path traversal | CWE-22 — validate file paths |
| Supply chain | Pin dependency versions; check for known CVEs |

### Architectural Fit
- Does it follow the team's established patterns?
- Does it introduce unnecessary coupling or dependencies?
- Does it reuse existing infrastructure (caching, logging, error reporting)?

### Testing (AI-Generated Tests Need Extra Scrutiny)
- Do the tests actually test the right thing? (LLMs write tautological tests)
- Are there missing edge cases?
- Were tests also AI-generated? If so, double their scrutiny.

### Prompt-to-Code Verification
- Re-read the prompt side-by-side with generated code
- Did the AI invent requirements not in the spec?
- Does the code handle failure scenarios implied by the spec?

---

## Known Failure Modes (What to Look For)

### From Academic Research
| Finding | Source |
|---------|--------|
| ~40% of Copilot code contributions contain vulnerabilities | Pearce et al. 2022 |
| AI-assistant users write *less* secure code | Perry et al. 2023 |
| AI users are *more confident* code is secure | Perry et al. 2023 |
| LLMs pattern-match rather than truly reason | Dziri et al. 2023 |
| Performance decays rapidly with task complexity | Dziri et al. 2023 |

### Concrete Anti-Patterns (Doernenburg's Observations)
1. **Wrong type signatures** — LLM didn't propagate optionality contracts
2. **"Vibe fix"** — solves compiler error locally instead of addressing design issue (e.g., `token ?? ""` instead of making parameter optional)
3. **Unnecessary complexity** — invents non-existent edge cases
4. **Forgotten utilities** — replicates existing helper functions
5. **Spurious caching** — introduces caching without justification
6. **Overconfident API claims** — insists an API field exists when it requires a separate call

### OWASP Top 10 for LLM-Generated Code
| Risk | Relevance |
|------|-----------|
| Prompt Injection | Attackers manipulate prompts to produce malicious code |
| Supply Chain | AI code introduces vulnerable dependencies |
| Misinformation | Hallucinated APIs, algorithms, or security practices |
| Improper Output Handling | LLM output used without validation |

---

## Recommended Tooling Stack

| Category | Tool | Best For |
|----------|------|----------|
| AI Code Review | CodeRabbit | PR-level review with 40+ linters, learning from feedback |
| AI Code Review | Qodo | Cross-repo context, living rules, F1 64.3% on Code Review Bench |
| AI Code Review | GitHub Copilot Review | Native GitHub integration, no external setup |
| Security Scanning | Semgrep | SAST/SCA/secrets with AI triage, MCP server for AI tools |
| IDE Layer | Qodo / CodeRabbit / Copilot | Real-time in-editor feedback |

---

## Key Takeaways

1. **Automate first, then review** — Let AI-powered tools catch the common issues before human review
2. **Humans "on the loop", not "in the loop"** — Build a harness (specs, checks, tests) that improves over time
3. **Use a structured checklist** — AI failure modes differ from human ones; don't use the same review process
4. **Extra scrutiny on security** — AI code is statistically more likely to contain vulnerabilities, and developers are less likely to suspect it
5. **Timebox debugging AI code** — If fixing an AI suggestion takes >5 minutes, regenerate from scratch
6. **Build team-specific review rules** — Customize by language, framework, and domain

---

## Sources

| Title | Author(s) | URL |
|-------|-----------|-----|
| I still care about the code | Birgitta Böckeler | https://martinfowler.com/articles/exploring-gen-ai/i-still-care-about-the-code.html |
| How to tackle unreliability of coding assistants | Birgitta Böckeler | https://martinfowler.com/articles/exploring-gen-ai/08-how-to-tackle-unreliability.html |
| Assessing internal quality while coding with an agent | Erik Doernenburg | https://martinfowler.com/articles/exploring-gen-ai/ccmenu-quality.html |
| Humans and Agents in Software Engineering Loops | Kief Morris | https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html |
| Asleep at the Keyboard? (Copilot Security) | Pearce et al. | https://arxiv.org/abs/2108.09293 |
| Do Users Write More Insecure Code with AI? | Perry et al. | https://arxiv.org/abs/2211.03622 |
| Faith and Fate (LLM Reasoning Limits) | Dziri et al. | https://arxiv.org/abs/2305.18654 |
| OWASP Top 10 for LLM Applications (2025) | OWASP | https://genai.owasp.org/llm-top-10/ |
| CodeRabbit | CodeRabbit | https://coderabbit.ai/ |
| Qodo | Qodo | https://www.qodo.ai/ |
| GitHub Copilot Code Review | GitHub | https://docs.github.com/en/copilot/using-github-copilot/code-review/using-copilot-code-review |
| Semgrep | Semgrep | https://semgrep.dev/ |
