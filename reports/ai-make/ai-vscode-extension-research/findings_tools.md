# Findings: AI-Powered VS Code Extension Generation Tools

## OpenSpec (Fission AI) - 44.5k stars
- **URL**: https://github.com/Fission-AI/OpenSpec
- **Description**: Spec-driven development (SDD) framework for AI coding assistants. CLI tool that structures the process from requirements to task breakdown.
- **Key Features**:
  - Slash commands: `/opsx:propose` (propose feature), `/opsx:apply` (implement), `/opsx:archive` (archive completed work)
  - Works with 25+ AI coding tools (Claude Code, Cursor, Copilot, etc.)
  - Lightweight spec layer: proposal.md, specs/, design.md, tasks.md per change
  - Dashboard for managing specs visually
  - Philosophy: fluid not rigid, iterative not waterfall
- **Workflow**: Propose → Spec generation → Implementation → Archive
- **Relevance**: Can be used by Code Agents to structure VS Code extension development from specs

## OpenSpec for Copilot (VS Code Extension)
- **URL**: https://marketplace.visualstudio.com/items?itemName=atman-dev.openspec-for-copilot
- **GitHub**: https://github.com/atman-33/openspec-for-copilot
- **Description**: A VS Code extension that brings OpenSpec's Spec-Driven Development workflow into VS Code with GitHub Copilot integration
- **Key Features**:
  - Visual spec management in VS Code
  - One-click spec generation via Copilot Chat
  - CodeLens "Start Task" on tasks.md
  - Archive workflow for completed specs
  - Custom prompt management (.github/prompts)
- **This is itself a VS Code extension built with AI assistance**, making it a meta-example

## Spec Kit
- **URL**: https://speckit.org
- **Description**: AI-powered specification-driven development toolkit. Alternative to OpenSpec but more heavyweight with rigid phase gates.

## SRS Writer
- **URL**: https://marketplace.visualstudio.com/items?itemName=Testany.srs-writer-plugin
- **Description**: VS Code extension for AI-powered Software Requirements Specification writing.

## Key Insight
The dominant pattern is **Spec-Driven Development (SDD)**: write structured specs first, then have AI generate code based on those specs. OpenSpec is the most popular (44.5k stars) and works with all major AI coding tools.
