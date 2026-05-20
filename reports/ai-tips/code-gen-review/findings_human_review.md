# Human Review Strategies for LLM/Coding Agent Generated Code

> Research conducted: April 2026

---

## 1. Key Mindset Shift: LLMs Are Not Compilers

> "LLMs are NOT compilers, interpreters, transpilers or assemblers of natural language, they are **inferrers**. A compiler takes a structured input and produces a repeatable, predictable output. LLMs do not do that." — Birgitta Böckeler, *I still care about the code* (martinfowler.com, July 2025)

**Implication for review:** Unlike traditional code generation tools, LLM output is non-deterministic. Every output must be treated as a *suggestion* to be validated, not a translation to be accepted.

> "Hallucinations are the core feature of LLMs. We just call it 'hallucinations' when they do something we don't want, and 'intelligence' in the cases where it's useful to us." — Birgitta Böckeler, *I still care about the code*

**Source:** https://martinfowler.com/articles/exploring-gen-ai/i-still-care-about-the-code.html

---

## 2. The "On-Call" Litmus Test

> "If you were on call for the application you're working on, at which point would you be ok with deploying a 1,000 or 5,000 LOC change set?" — Birgitta Böckeler, *I still care about the code*

This question grounds the review process in real accountability: the reviewer should imagine being paged for production incidents caused by the code they are reviewing.

**Source:** https://martinfowler.com/articles/exploring-gen-ai/i-still-care-about-the-code.html

---

## 3. Constant Risk Assessment Framework (Böckeler's Model)

A three-factor risk assessment for every AI-generated code contribution:

| Factor | Questions to ask |
|--------|-----------------|
| **Impact** | Will I be called at night? Is the domain critical? What's the blast radius? |
| **Probability** | How sophisticated is the AI setup? Is the problem simple or complex? Was sufficient context available? |
| **Detectability** | How likely am I to catch problems? What type of review is applied? How good is the overall safety net? |

**Source:** https://martinfowler.com/articles/exploring-gen-ai/i-still-care-about-the-code.html

---

## 4. Confidence Assessment: Feedback Loop Questions

Böckeler's framework for gauging confidence in AI suggestions:

1. **Do I have a quick feedback loop?** (syntax highlighting, compiler integration, test runner)
2. **Do I have a reliable feedback loop?** (trust in the test suite; was the test also AI-generated?)
3. **What is the margin of error?** (new patterns have larger blast radius; security = low margin)
4. **Do I need very recent information?** (LLM training cutoffs mean stale library docs)

> "If I'm unsure of my test coverage, I can even use the assistant itself to raise my confidence, and ask it for more edge cases to test." — Birgitta Böckeler, *How to tackle unreliability of coding assistants*

**Source:** https://martinfowler.com/articles/exploring-gen-ai/08-how-to-tackle-unreliability.html

---

## 5. The Donkey Persona: Mental Model for the Reviewer

Böckeler suggests anthropomorphizing the AI coding assistant as an "eager, stubborn donkey" with these traits:
- Eager to help
- Stubborn (will insist on wrong approaches)
- Very well-read, but inexperienced (high intelligence, low wisdom)
- Won't admit when it doesn't "know" something

> "The one thing you should never say is 'Dusty caused that incident!', because Dusty is basically underage, they don't have a license to commit. We are kind of the parents who are ultimately responsible for the commits, and 'parents are liable for their children'." — Birgitta Böckeler

**Source:** https://martinfowler.com/articles/exploring-gen-ai/08-how-to-tackle-unreliability.html

---

## 6. Humans In/On/Outside the Loop (Kief Morris's Model)

| Role | Description | Risk |
|------|-------------|------|
| **Humans outside the loop** | "Vibe coding" — human defines what, agent defines how | Code quality decay, tech debt accumulation, agent spirals |
| **Humans in the loop** | Gatekeeping each line of AI-generated code | Bottleneck; humans can't keep pace with agent output |
| **Humans on the loop** | Building and maintaining the "harness" — specs, quality checks, workflow guidance | Balances speed with quality; treats the process as an evolvable system |

### Key insight — "on the loop":

> "The 'in the loop' way is to fix the artefact, whether by directly editing it, or by telling the agent to make the correction we want. The 'on the loop' way is to change the harness that produced the artefact so it produces the results we want." — Kief Morris, *Humans and Agents in Software Engineering Loops*

### The Agentic Flywheel:
1. Define the harness (tests, specs, guidelines)
2. Agents run the how loop
3. Agents analyze results and recommend harness improvements
4. Humans review recommendations, approve changes to the harness
5. Loop improves iteratively

**Source:** https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html

---

## 7. Concrete Anti-Patterns Found in LLM Code (Doernenburg's Observations)

From Erik Doernenburg's experience adding GitLab support to CCMenu using AI agents (Claude Code, Windsurf):

| Anti-Pattern | Example | Root Cause |
|-------------|---------|------------|
| **Wrong type signatures** | Token declared non-optional when it should be optional | LLM didn't propagate the optionality contract |
| **"Vibe fix" instead of correct fix** | `token ?? ""` instead of making the parameter `String?` | AI solves the compiler error locally instead of addressing the design issue |
| **Unnecessary complexity** | Complicated logic to handle a non-existent edge case | LLM invented a problem (user/org overlap in GitLab that doesn't exist) |
| **Forgotten existing utilities** | Replicated URL-construction logic instead of reusing existing functions | LLM doesn't have full context of the codebase's utilities |
| **Spurious caching** | Introduced a completely unnecessary cache | LLM pattern-matched "performance concern" without justification |
| **Overconfidence in API knowledge** | Insisted avatar URL was in GitLab response when it required a separate API call | LLM conflated similar API endpoints |

> "Without careful oversight, though, the AI agents seem to have a strong tendency to introduce technical debt, making future development harder, for humans and agents." — Erik Doernenburg, *Assessing internal quality while coding with an agent*

**Source:** https://martinfowler.com/articles/exploring-gen-ai/ccmenu-quality.html

---

## 8. Structured Review Checklist for LLM-Generated Code

Based on the patterns observed above, a practical review checklist:

### Correctness
- [ ] Does the code actually solve the stated problem? (don't assume — test it)
- [ ] Are all API endpoints, library functions, and framework APIs real? (LLMs hallucinate API signatures)
- [ ] Are edge cases handled? (ask the LLM: "what edge cases am I missing?")
- [ ] Are error paths tested, not just happy paths?
- [ ] Does the code compile/build without warnings? (warnings often signal deeper issues)

### Type Safety & Contracts
- [ ] Are types correct and idiomatic for the language? (e.g., `String?` vs `String` in Swift, `Optional[T]` vs `T` in Rust)
- [ ] Are null/optional/nil states handled properly?
- [ ] Are function signatures self-documenting and semantically correct?
- [ ] Does the code use existing utility/helper functions rather than duplicating logic?

### Internal Quality
- [ ] Would you be comfortable owning this code long-term?
- [ ] Does it follow the team's established patterns and conventions?
- [ ] Are variable/function names meaningful? (LLMs often generate bland or misleading names)
- [ ] Is the code unnecessarily complex? (does the simplest solution work?)
- [ ] Is there any dead code, unused imports, or unnecessary abstractions?

### Security
- [ ] Does the code handle user input safely? (LLMs frequently introduce injection vulnerabilities)
- [ ] Are secrets/tokens handled correctly? (not logged, not hardcoded, not committed)
- [ ] Are security headers, authentication, and authorization properly implemented?
- [ ] Are dependencies pinned to known-good versions? (LLMs may suggest unpatched libraries)

### Architectural Fit
- [ ] Does the code follow the same architectural patterns as the rest of the codebase?
- [ ] Does it reuse existing infrastructure (caching, logging, error reporting)?
- [ ] Does it introduce unnecessary coupling or dependencies?
- [ ] If a new pattern is introduced, is there a good reason it couldn't follow the existing patterns?

### Testing
- [ ] Were tests also AI-generated? (if so, double their scrutiny)
- [ ] Do the tests actually test the right thing? (LLMs often write tautological tests)
- [ ] Are there missing edge cases the LLM didn't consider?
- [ ] Are the tests themselves readable and maintainable?

### Prompt-to-Code Verification
- [ ] Re-read the original prompt/requirement side by side with the generated code
- [ ] Does the code match the specification precisely, or did it drift?
- [ ] Were there any implicit assumptions the LLM made that weren't in the spec?
- [ ] Does the code handle failure scenarios implied by the spec but not explicitly stated?

---

## 9. The "Stress the Code" Approach

> "If a suggestion doesn't bring me value with little additional effort, I move on. If an input is not helping me quick enough, I always assume the worst about the assistant, rather than giving it the benefit of the doubt and spending 20 more minutes on making it work." — Birgitta Böckeler

Apply a **timebox** to AI-generated code. If a fix requires more than a few minutes of debugging, prefer writing it yourself or asking the LLM to regenerate from a different angle rather than trying to patch the broken output.

**Source:** https://martinfowler.com/articles/exploring-gen-ai/08-how-to-tackle-unreliability.html

---

## 10. Recommendations for Our Team's Review Workflow

1. **Treat AI-generated PRs with higher scrutiny than human PRs** — not because AI is worse, but because its failure modes are different (hallucinated APIs, wrong type contracts, invented edge cases, unnecessary complexity).

2. **Shift left with AI harness engineering** — invest in automated quality checks (linters, type checkers, test coverage, security scanners) so the AI catches its own problems before human review.

3. **Review tests as carefully as production code** — especially when the LLM wrote the tests. LLMs often write tests that pass trivially (tautological tests) or miss crucial edge cases.

4. **Use the "on-call" framing** — ask: "Would I be comfortable being paged about this code at 3 AM?"

5. **Keep human judgment for design-level decisions** — let AI handle boilerplate and routine transformations, but humans should validate:
   - Architectural fit
   - Security implications
   - API contract correctness
   - Non-functional requirements (performance, resilience)

6. **Build a team-specific review checklist** from this research — customize by language, framework, and domain.

---

## Sources

| Title | Author(s) | Date | URL |
|-------|-----------|------|-----|
| I still care about the code | Birgitta Böckeler | Jul 2025 | https://martinfowler.com/articles/exploring-gen-ai/i-still-care-about-the-code.html |
| How to tackle unreliability of coding assistants | Birgitta Böckeler | Nov 2023 | https://martinfowler.com/articles/exploring-gen-ai/08-how-to-tackle-unreliability.html |
| Assessing internal quality while coding with an agent | Erik Doernenburg | Jan 2026 | https://martinfowler.com/articles/exploring-gen-ai/ccmenu-quality.html |
| Humans and Agents in Software Engineering Loops | Kief Morris | Mar 2026 | https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html |
