# Research Findings: Harness Engineering for AI Agent Reliability

**Research Date:** 2026-04-28
**Source Article (Start Point):** https://codelove.tw/@tony/post/qO2Rda (Chinese translation of https://juejin.cn/post/7620226704209592360)
**Original Author:** mCell (via Cell Stack: https://stack.mcell.top/blog/2026/harness-engineering-agent-engineering-explained)

---

## 1. What Is Harness Engineering?

### Definition

**Harness Engineering** is the discipline of designing the total engineering environment in which an AI agent operates. It is not a model, not a prompt, not a tool call, and not a framework. It is the "sum total of the engineering environment" at agent runtime.

> "Harness is not a model. Not a prompt. Not a tool call. Not a framework. Harness is the sum total of the engineering environment at agent runtime." — mCell

### What the "Environment Sum" Includes

1. How tasks are expressed
2. How context is organized
3. How tools are exposed, governed, and intercepted
4. How state is saved, restored, and trimmed
5. How feedback flows back to the model
6. How errors are classified, retried, and escalated
7. How safety boundaries are established
8. How the system verifies the agent actually completed the task

### Analogy

> "If you think of an Agent as a brain that can call tools, then Harness is: the body, sensors, guardrails, control panel, process systems, receipt systems, and insurance you give that brain." — mCell

---

## 2. How Harness Engineering Differs from Prompt and Context Engineering

| Discipline | Focus | Concern |
|---|---|---|
| **Prompt Engineering** | How to say it | System prompts, few-shot, wording |
| **Context Engineering** | What info to give the model | Documents, history, AGENTS.md, memory |
| **Harness Engineering** | What environment the model operates in | Tools, approvals, safety, state, recovery |

> "Context Engineering is a component of Harness, but Harness is not equal to Context." — mCell

### Supporting Sources

- **Wikipedia:** "Context engineering is the related area of software engineering that focuses on the management of non-prompt contexts supplied to the GenAI model, such as metadata, API tools, and tokens." (https://en.wikipedia.org/wiki/Prompt_engineering)
- **Comet:** "Context engineering is the discipline of designing, governing, and optimizing that surrounding information so models consistently do the right work with the right data." (https://www.comet.com/site/blog/context-engineering/)
- **LangChain:** Andrej Karpathy calls it the "delicate art and science of filling the context window with just the right information for the next step." Cognition says it is "effectively the #1 job of engineers building AI agents." (https://blog.langchain.com/context-engineering-for-agents/)

---

## 3. The Five Layers of Harness

### Layer 1: Context Assembly System
The prompt is a dynamic assembly system with six layers: base template, user preferences (SOUL.md), project context (AGENTS.md), Skills, tool descriptions, tool definition JSON. Different sources have different priorities and freshness — you must build hierarchy at the engineering level before handing it to the model.

### Layer 2: Tool Governance System
Four problems: how the model discovers tools, parameter validation, risk classification, call interception. Three sub-layers: Declarative DSL, Risk & Approval (read/write/execute/critical), Orchestration (validation, interception, trimming, errors). "Make tool calling a governable system, not a bunch of bare interfaces."

### Layer 3: Security & Approval System
Three defensive lines: Subprocess Management (session pools, limits, timeouts), Command Guard (parsing, blacklists, system hints), Approval System (risk分级, modes, fingerprint caching). "Safety cannot rely solely on model self-discipline. The real safety boundary must live at runtime."

### Layer 4: Feedback & State System
Translate internal system events into model-consumable feedback. Tool results, approval status, truncation, rejections, plan updates, session recoverability — all must be translated so the model understands *why* something failed and can take correct next action.

### Layer 5: Entropy Management System
Systems inevitably decay: prompts grow, rules stale, AGENTS.md becomes a dump, tools accumulate, memory fills with noise. Harness must continuously: expire old rules, compress long contexts, evict low-value history, let knowledge settle sustainably. "Without this awareness, even the strongest agent will drift off course."

---

## 4. OpenAI Codex App Server Harness Implementation

Referenced from OpenAI's February 2026 article (https://openai.com/index/codex-app-server/ returned 403 during research; details from mCell's article):

> "Engineers' work is shifting from writing code to designing environments, specifying intent, building feedback loops so agents can work reliably. A small team produced ~1M lines of code in a few months with Codex."

Codex App Server harness components:
- User-Model-Tools core loop
- Thread lifecycle and persistence
- Configuration and authentication
- Tool execution and extension
- Client-runtime protocol layer

> "The real harness is not a prompt file — it is a complete runtime."

---

## 5. The Formula: Agent = Loop(Model + Harness)

**Original:** Agent = Loop(LLM + Context + Tools)
**Upgraded:** Agent = Loop(Model + Harness)

Context and Tools are now part of Harness. What determines an agent's ceiling is not having components but engineering them into a sustainable environment.

Three most important words: **Constraint, Feedback, Stability.**

Core insight: **Agent capability = Model x Environment** (not just model capability).

Practical order:
1. Build environment before chasing models
2. Systematize tools (discoverable, validatable, gradable, interceptable, auditable)
3. Assemble prompts dynamically, don't write one blob
4. Safety boundaries at runtime, not in prompts
5. Make all failures explainable
6. Design state and recovery for long tasks
7. Do regular entropy management

---

## 6. Source URLs

| Source | URL |
|---|---|
| Start point (CodeLove) | https://codelove.tw/@tony/post/qO2Rda |
| Original Chinese (Juejin) | https://juejin.cn/post/7620226704209592360 |
| Author site (Cell Stack) | https://stack.mcell.top/blog/2026/harness-engineering-agent-engineering-explained |
| Wikipedia: Prompt Engineering | https://en.wikipedia.org/wiki/Prompt_engineering |
| Comet: Context Engineering | https://www.comet.com/site/blog/context-engineering/ |
| LangChain: Context Engineering | https://blog.langchain.com/context-engineering-for-agents/ |

---

## 7. Key Quotes

> "Harness is not a new technical invention. It is the part of Agent engineering that has always existed but never had a complete name." — mCell

> "Agent = Loop(LLM + Context + Tools). The loop itself is not complex. What is truly difficult is software engineering." — mCell

> "The real battlefield of an Agent project is not the model layer — it is the runtime environment layer." — mCell

> "I wanted to verify not how talented the model is, but how high environmental design can elevate an ordinary model." — mCell

> "The core of Agent is simple. What is truly difficult is Harness." — mCell

> "The focus of Agent is not on the model — it is on the environment." — mCell

> "Context engineering ... is effectively the #1 job of engineers building AI agents." — Cognition

> "Context engineering is the discipline behind reliable LLM applications and agents." — Matt M. Casey, Comet
