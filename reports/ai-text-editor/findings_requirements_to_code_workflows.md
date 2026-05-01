# Findings: Requirements-Driven AI Code Generation Workflows

## 1. Overview

This report documents frameworks, tools, and methodologies for translating requirements documents (PRDs, spec files, markdown specs) into working code using AI agents. The space has evolved rapidly from simple prompt-to-code tools to sophisticated multi-agent, multi-step workflows.

---

## 2. Key Tools & Frameworks

### 2.1 GPT Engineer (gpt-engineer)
- **URL:** https://github.com/AntonOsika/gpt-engineer (archived, precursor to Lovable.dev)
- **Stars:** 55.2k
- **Core Workflow:** Write a `prompt` file in natural language -> AI writes and executes code -> human asks for improvements iteratively.
- **Key Features:** Supports "improve existing code" mode (`-i` flag), custom preprompts for agent identity, vision input for architecture diagrams, and local/open-source model support.
- **Quote:** "Specify software in natural language. Sit back and watch as an AI writes and executes the code."
- **Relevance:** The original "spec-first" code generation CLI platform that inspired many successors.

### 2.2 Smol Developer (smol-ai/developer)
- **URL:** https://github.com/smol-ai/developer
- **Stars:** 12.2k
- **Core Workflow:** Three-step pipeline: (1) `plan(prompt)` -> shared_dependencies.md, (2) `specify_file_paths(prompt, deps)` -> file list, (3) `generate_code_sync(prompt, deps, file_path)` -> per-file code generation.
- **Key Innovation:** Intermediate `shared_dependencies.md` step solves "whole program coherence" by forcing the AI to establish cross-file contracts before generating code.
- **Quote:** "Markdown is all you need — Markdown is the perfect way to prompt for whole program synthesis because it is easy to mix english and code."
- **Pattern:** "Human writes a basic prompt -> main.py generates code -> Human runs/reads code -> Human pastes errors back into prompt -> Loop until happiness."

### 2.3 AutoGPT (Significant-Gravitas)
- **URL:** https://github.com/Significant-Gravitas/AutoGPT
- **Stars:** 184k
- **Core Workflow:** Continuous AI agent platform for automating complex workflows. Agent Builder + Workflow Management (block-based).
- **Relevance:** More general-purpose agent platform than spec-to-code, but includes a code ability module and supports building agents that can autonomously code from specs.

### 2.4 Aider (Aider-AI)
- **URL:** https://github.com/Aider-AI/aider
- **Stars:** 44.2k
- **Core Workflow:** AI pair programming in the terminal. Maps entire codebase, makes surgical changes, auto-commits with git.
- **Key Features:** Repomap for codebase understanding, lint/test integration, voice-to-code, works with 100+ languages.
- **Quote:** "aider is AI pair programming in your terminal" — the evolution from GPT Engineer that is "a well maintained hackable CLI."
- **Relevance:** Top recommendation from GPT Engineer's README as the maintained alternative for spec-driven development.

### 2.5 E2B Fragments
- **URL:** https://github.com/e2b-dev/fragments
- **Stars:** 6.3k
- **Core Workflow:** Open-source template for "apps like Claude Artifacts, Vercel v0, or GPT Engineer."
- **Key Features:** Sandboxed code execution, streaming UI, multi-stack support (Next.js, Vue, Python, Streamlit, Gradio), multiple LLM providers.
- **Relevance:** Demonstrates the "sandboxed execution + AI generation" pattern for safe spec-to-code pipelines.

### 2.6 GitHub Spark
- **URL:** https://github.com/features/spark
- **Core Workflow:** "Describe what you want in natural language -> AI generates full-stack app -> Instant preview -> One-click deploy."
- **Quote:** "Dream it. See it. Ship it."
- **Relevance:** Latest GitHub-native spec-to-product pipeline. Includes PRD.md tracking in project, integrated with Copilot.

---

## 3. Workflow Patterns

### 3.1 The Smol Developer Three-Step Pipeline
1. **Plan** — AI reads the prompt/spec and generates a shared dependencies document (shared_dependencies.md) describing cross-file contracts
2. **Specify** — AI enumerates all file paths needed based on the plan
3. **Generate** — For each file path, AI generates code using the plan context

**Key insight:** Intermediate "shared dependencies" step ensures cross-file coherence, which is the main failure mode of one-shot code generation.

### 3.2 GPT Engineer Iterative Loop
1. Write `prompt` file with requirements
2. Run `gpte <project>` — AI generates codebase
3. Review output — run code, identify errors
4. Write improvement instructions in `prompt` file
5. Run `gpte <project> -i` — AI improves existing code
6. Repeat

### 3.3 The "Human-in-the-Loop" Pattern (Smol Developer)
> "AI is only used as long as it is adding value — once it gets in your way, just take over the codebase from your smol junior developer with no fuss."

1. Human writes basic spec prompt
2. AI scaffolds entire codebase
3. Human runs code, identifies errors
4. Human pastes errors back into prompt
5. AI generates fixes
6. Loop until done

### 3.4 Aider's Codebase-Aware Pattern
1. Aider maps the entire codebase (repomap) for context
2. Developer describes desired change in natural language
3. AI makes surgical edits to relevant files
4. Changes auto-linted and tested
5. Changes auto-committed with sensible messages
6. Developer reviews via familiar git diff tools

### 3.5 Prompt Engineering Patterns for Spec-to-Code

From Smol Developer's documented insights:
- **"Markdown is all you need"** — Mix English and code blocks in spec files
- **"Copy and paste programming"** — Paste API docs (curl input/output) into specs to teach AI new APIs past its training cutoff
- **"Logbook-driven programming"** — Paste error messages into the prompt with vague descriptions of desired handling
- **"Shared dependencies document"** — Add intermediate step to establish cross-file contracts before code generation

---

## 4. Notable Methodologies

### 4.1 "Write Spec First, Then Let AI Implement"
The common thread across all tools. The spec (prompt.md, prompt file, PRD) is the single source of truth. AI implements from it. Humans edit the spec to iterate.

### 4.2 "Engineering with Prompts, Rather than Prompt Engineering"
> From Smol Developer: "This is engineering with prompts, rather than prompt engineering" — the emphasis is on iterative spec refinement (engineering practice) rather than one-shot prompt crafting.

### 4.3 Spec-to-Code Pipeline Architecture
Common architecture across tools:
1. **Spec ingestion** (natural language prompt, markdown, structured PRD)
2. **Planning phase** (shared deps doc, architecture plan, file listing)
3. **Code generation phase** (per-file generation with context from planning)
4. **Validation phase** (lint, test, compile, runtime check)
5. **Feedback loop** (error messages back to spec or directly to fix pass)

### 4.4 "Self-Healing" via Error Feedback
Tools increasingly support feeding runtime errors back to the AI for automatic fixing. Smol Developer's `debugger.py` reads the whole codebase + error message to suggest specific fixes.

---

## 5. Key Takeaways

| Approach | Representative Tool | Best For |
|---|---|---|
| Spec file -> entire codebase | GPT Engineer, Smol Developer | Greenfield projects, prototypes |
| Terminal pair programming | Aider | Existing codebases, surgical changes |
| Sandboxed artifact generation | E2B Fragments | Safe experimentation, web apps |
| Autonomous agent workflows | AutoGPT | Complex multi-step automation |
| Full-stack from natural language | GitHub Spark | Rapid prototyping to production |

1. **Intermediate planning improves coherence** — The shared_dependencies.md pattern from Smol Developer is a critical innovation.
2. **Iteration is essential** — All successful tools emphasize a tight human-in-the-loop feedback cycle, not one-shot generation.
3. **Spec is the control surface** — The most effective workflow is "edit the spec, regenerate the code."
4. **Error feedback loops** — Automatically feeding runtime errors back to the AI for self-healing is an emerging best practice.
5. **Markdown as universal spec format** — Markdown naturally accommodates mixed natural language and code, making it the de facto standard for spec files.
