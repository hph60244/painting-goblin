# AI Agent Benchmarks: Task Categories, Structure, and Scoring

## Overview

This report catalogs major AI agent benchmarks, describing what types of agent tasks they evaluate, their specific task categories, and how tasks are structured and scored. Benchmarks are grouped by domain focus.

---

## 1. SWE-bench (Software Engineering)

**Domain:** Code repair / software engineering
**Venue:** ICLR 2024 (Oral)

**What it evaluates:** LLMs given a real GitHub codebase and an issue description must generate a patch (diff) that resolves the described problem.

**Task categories:**
- **SWE-bench** -- 2,294 task instances from 12 Python repositories (e.g., django, sympy, scikit-learn). Tasks are real GitHub issues with associated pull requests.
- **SWE-bench Lite** -- A subset of 300 curated instances for faster evaluation.
- **SWE-bench Verified** -- 500 instances confirmed solvable by human software engineers (collaboration with OpenAI Preparedness).
- **SWE-bench Multimodal** -- Extends to visual software domains (e.g., HTML/CSS, GUI code).
- **SWE-bench Multilingual** -- Extends across multiple programming languages.

**Task structure:** Each instance includes: a commit hash (base codebase state), a GitHub issue text, and a "gold" patch (the human-written fix). The agent must generate a patch.

**Scoring:** **Execution-based**. The agent's patch is applied to the repository, test suites are run, and metrics are:
- **% resolved** (pass to fail / fail to pass): the patch must make previously failing tests pass without breaking previously passing tests.
- Evaluated in Docker containers for reproducibility.

---

## 2. AgentBench (LLM-as-Agent Multi-Domain)

**Domain:** General-purpose LLM agent evaluation across 8 environments
**Venue:** ICLR 2024

**What it evaluates:** LLMs operating as autonomous agents in diverse interactive environments.

**Task categories (8 environments):**
- **Operating System (OS)** -- Interact with a Linux command-line; install packages, manage files, configure services.
- **Database (DB)** -- Write SQL queries against MySQL to answer questions or perform data operations.
- **Knowledge Graph (KG)** -- Query Freebase via SPARQL for multi-hop reasoning.
- **Digital Card Game (DCG)** -- Play a strategy card game requiring planning and opponent modeling.
- **Lateral Thinking Puzzles (LTP)** -- Solve puzzles by asking yes/no questions to an oracle.
- **House-Holding (HH)** -- Text-based household tasks (adapted from ALFWorld): navigate rooms, find/place objects.
- **Web Shopping (WS)** -- Navigate a simulated e-commerce site to find/purchase items (adapted from WebShop).
- **Web Browsing (WB)** -- Real website interaction via Mind2Web: fill forms, click buttons, navigate.

**Task structure:** Multi-turn interaction. Dev split: ~4k LLM calls; Test split: ~13k LLM calls. Each task is containerized in Docker.

**Scoring:** Task-specific **success rate** (binary pass/fail per episode). Overall score is the average across all 8 environments.

---

## 3. WebArena (Web Navigation)

**Domain:** Web agent for realistic web tasks
**Venue:** NeurIPS 2024 (Oral)

**What it evaluates:** Autonomous agents completing high-level tasks on fully functional websites in a sandboxed environment.

**Task categories:**
- **WebArena** -- 812 tasks across 5 categories of websites:
  - **Shopping** (e.g., One Stop Market)
  - **Social Forum** (e.g., Reddit-style)
  - **Software Development** (e.g., GitLab)
  - **Content Management** (e.g., WordPress)
  - **Map/Navigation** (e.g., OpenStreetMap)
- **VisualWebArena** (ACL 2024) -- 241 tasks requiring visual understanding (screenshots, images).
- **WebArena-Infinity** -- Continuous/scalable evaluation in evolving web environments.
- **TheAgentCompany** (ICML 2025) -- Tasks simulating real-world business workflows.

**Task structure:** Each task provides a natural language instruction, initial URL, and a specific goal. Tasks are multi-step (mean 8-15 steps). The environment is a live, fully functional website.

**Scoring:** **Execution-based**: automated evaluation scripts check for specific outcomes (e.g., "is the shopping cart item correctly added?", "is the GitLab issue created with correct labels?"). Binary pass/fail per task. Reproducibility via Docker.

---

## 4. GAIA (General AI Assistants)

**Domain:** General-purpose AI assistant with tool use, reasoning, multi-modality
**Venue:** 2023

**What it evaluates:** Real-world questions requiring reasoning, multi-modal handling, web browsing, and tool-use proficiency.

**Task categories (466 questions, 300 with held-out answers):**
Questions conceptually simple for humans but hard for AI. Three difficulty levels:
- **Level 1** -- Questions answerable with basic tools (e.g., web search, calculator).
- **Level 2** -- Questions requiring multi-step reasoning with multiple tools.
- **Level 3** -- Questions requiring complex reasoning, multiple tool calls, and information synthesis across sources.

Examples: "What is the date of the most recent solar eclipse visible from Paris?" "How many countries have a flag that contains the color purple?"

**Task structure:** Each question has a precise answer (a short string, number, or date). Questions may require web browsing, file parsing (PDF/CSV/images), code execution, or API calls.

**Scoring:** **Exact-match accuracy**. Answers are compared against a curated ground truth. The answer must be exact (string match, numeric tolerance). Human performance: 92%; GPT-4+Plugins: 15% -- highlighting a large gap.

---

## 5. ToolBench / ToolLLM (Tool/API Use)

**Domain:** Tool learning and API calling
**Venue:** ICLR 2024 (Spotlight)

**What it evaluates:** LLMs using 16,464 real-world REST APIs from RapidAPI across 49 categories to fulfill human instructions.

**Task categories (3 difficulty levels):**
- **G1 (Single Tool)** -- Instructions solvable with a single API call.
- **G2 (Intra-Category Multi-Tool)** -- Multiple APIs needed, all from the same category (e.g., multiple sports APIs).
- **G3 (Intra-Collection Multi-Tool)** -- Multiple APIs needed, spanning different categories.

**Task structure:** 126,486 instruction instances with annotated solution paths. Uses DFSDT (Depth-First Search-based Decision Tree) for path annotation. Includes real API execution during training/evaluation.

**Scoring (via ToolEval):**
- **Pass Rate** -- Proportion of successfully completed instructions within a limited number of API calls.
- **Preference (Win Rate)** -- Pairwise comparison by ChatGPT evaluator between two candidate answers, scored on correctness, efficiency, and completeness. Human agreement: 87.1% on pass rate, 80.3% on win rate.

---

## 6. API-Bank (Tool-Augmented LLMs)

**Domain:** API calling and tool use
**Venue:** EMNLP 2023

**What it evaluates:** LLMs' ability to plan, retrieve, and call APIs across 2,138 APIs spanning 1,000 domains.

**Task categories (3 levels of ability):**
- **Level 1 (API Retrieval)** -- Given a query, retrieve the correct API from a large pool.
- **Level 2 (API Calling)** -- Given a query and a specific API, correctly invoke it with the right parameters.
- **Level 3 (Planning + Calling)** -- Given a complex instruction, plan a sequence of API calls, retrieve the required APIs, and execute them in order.

**Task structure:** 314 evaluation dialogues with 753 annotated API calls. Training set: 1,888 tool-use dialogues. APIs are from real services (weather, translation, finance, etc.).

**Scoring:** **Execution-based success rate**. Each API call is checked against ground truth parameters and return values. For Level 3, the entire plan must succeed end-to-end. The Lynx model (fine-tuned Alpaca) was trained on this data.

---

## 7. ALFWorld (Embodied / Household Tasks)

**Domain:** Embodied AI -- text-based household navigation and manipulation
**Venue:** ICLR 2021

**What it evaluates:** Agents performing everyday household tasks in a simulated environment, aligned with the ALFRED embodied benchmark.

**Task categories:** Based on the ALFRED task taxonomy:
- **Pick & Place** -- Pick up an object and place it somewhere.
- **Stack & Place** -- Pick up an object, stack it on another, and place.
- **Clean & Place** -- Clean an object and place it.
- **Heat & Place** -- Heat an object and place it.
- **Cool & Place** -- Cool an object and place it.
- **Toggle & Place** -- Toggle a device on/off and place.

**Task structure:** Text-based interaction (via TextWorld) parallel to embodied THOR environments. Agents receive text observations and output text commands (e.g., "go to kitchen 1", "pick up apple 1").

**Scoring:** **Success rate** -- binary pass/fail based on whether the final goal condition is met (e.g., "apple is on counter"). Also tracks **steps to completion** and **progress rate**.

---

## 8. MiniWoB++ (Web Interaction / GUI Grounding)

**Domain:** Web-based GUI interaction
**Venue:** Introduced 2018, extended from OpenAI MiniWoB

**What it evaluates:** Agents learning to interact with web page elements (buttons, forms, sliders, menus, etc.) through a browser.

**Task categories (100+ environments):**
- **Clicking** -- click-button, click-checkboxes, click-link, click-menu, click-tab, click-dialog, click-pie, etc.
- **Form Filling** -- enter-text, enter-date, enter-password, form-sequence, login-user, etc.
- **Selection** -- choose-date, choose-list, choose-date-easy, etc.
- **Navigation** -- navigate-tree, search-engine, social-media, book-flight, buy-ticket
- **Drag & Drop** -- drag-box, drag-circle, drag-items, drag-shapes, etc.
- **Text Manipulation** -- copy-paste, highlight-text, text-editor, text-transform
- **Math/Logic** -- simple-algebra, simple-arithmetic, count-shape, find-greatest, odd-or-even
- **GUI Widgets** -- use-autocomplete, use-colorwheel, use-slider, use-spinner

**Task structure:** Each environment is a simplified HTML page with a task description. The agent outputs DOM-level actions (click element, type text, select option). Uses Gymnasium API with Selenium WebDriver.

**Scoring:** **Cumulative reward**. Each task has a defined reward function (typically +1 for success, -1 for failure, or proportional reward based on progress). Some tasks have partial-credit rewards.

---

## 9. OSWorld (Open-Ended Computer Tasks)

**Domain:** Real OS-level computer use (multimodal agent)
**Venue:** 2024

**What it evaluates:** Multimodal agents performing open-ended tasks on real Ubuntu/Windows/macOS desktop environments, using arbitrary applications.

**Task categories (369 tasks):**
- **Web Applications** -- Chrome, Firefox tasks (e.g., form filling, data extraction)
- **Desktop Applications** -- LibreOffice (Calc, Writer), VS Code, GIMP, Thunderbird, VLC, etc.
- **OS File I/O** -- File management, directory operations, permissions
- **Cross-App Workflows** -- Tasks spanning multiple applications (e.g., download data from web, process in spreadsheet, send email)
- **Multi-App Sequences** -- Complex multi-step chains across apps

**Task structure:** Full virtual machine environment. Each task specifies an initial state (files, open apps, browser state) and a goal. Agent receives screenshots and accessibility tree; outputs mouse/keyboard actions.

**Scoring:** **Execution-based evaluation**. 134 custom evaluation scripts check specific outcomes (file contents, app state, system configuration). Binary pass/fail per task. Human baseline: 72.36%; best model (as of 2024): 12.24%.

---

## 10. AgentInstruct (Multi-Agent Training Data)

**Domain:** General instruction-following for agents
**Venue:** Microsoft Research, 2024

**What it evaluates:** LLMs' ability to follow diverse instructions across multiple domains, used as training data to create generalist agents.

**Task categories:** Data generated across 6 domains:
- **Coding** -- Code generation, debugging, refactoring
- **Reading & Writing** -- Summarization, editing, comprehension
- **Math & Reasoning** -- Problem solving, logic puzzles
- **Web Interaction** -- Browsing, form filling, information extraction
- **Tool Use** -- API calling, calculator use, database queries
- **Safety** -- Refusal, bias mitigation, content moderation

**Task structure:** Synthetic multi-turn dialogues generated by iterating between an "instructor" and "assistant" model. 1.8M+ training examples.

**Scoring:** Typically evaluated through downstream task performance on other benchmarks (MT-Bench, HumanEval, AgentBench, etc.) after fine-tuning.

---

## Cross-Benchmark Comparison

| Benchmark | Domain | # Tasks | Real Env | Scoring | Key Gap (Human vs. Best AI) |
|---|---|---|---|---|---|
| SWE-bench | Code repair | 2,294 | Yes (Docker) | Test pass/fail | ~30% vs. ~48% (best) |
| AgentBench | Multi-domain | ~13k turns | Yes (Docker) | Avg success rate | Significant gap |
| WebArena | Web | 812 | Yes (live sites) | Exec-based pass/fail | ~78% vs. ~30% |
| GAIA | General assistant | 466 | No (static QA) | Exact match | 92% vs. ~60% |
| ToolBench | API calling | 126k | Yes (RapidAPI) | Pass rate + Win rate | ~71% vs. ~67% |
| API-Bank | API calling | 314 | Yes (simulated) | Exec success rate | Significant gap |
| ALFWorld | Household | ~3k tasks | Yes (simulated) | Success rate | ~100% vs. ~70% |
| MiniWoB++ | Web GUI | 100+ | Yes (browser) | Cumulative reward | Near 100% vs. ~50% |
| OSWorld | Computer use | 369 | Yes (VM) | Exec-based pass/fail | 72% vs. 12% |
| AgentInstruct | General | 1.8M+ | No | Downstream metrics | N/A (training data) |

---

## Key Themes

1. **Execution-based evaluation** is the gold standard -- running code, calling live APIs, or interacting with real environments to verify outcomes.
2. **The gap is largest** in open-ended, real-world tasks (OSWorld, GAIA) where agents must plan, ground GUI elements, and recover from errors.
3. **Multimodality** is an emerging trend (VisualWebArena, OSWorld, SWE-bench Multimodal) -- agents must process screenshots alongside text.
4. **Scalability** varies widely: some benchmarks offer hundreds of tasks (WebArena, GAIA), others tens of thousands (ToolBench, AgentInstruct).
5. **Most benchmarks use Docker** or VMs for reproducible, sandboxed evaluation.
