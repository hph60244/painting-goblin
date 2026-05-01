# Research Report: Building VS Code Extensions with Code Agents

## Summary

This research identifies **three major approaches** for using Code Agents to build VS Code extensions from requirement documents, with the **Spec-Driven Development (SDD)** pattern being the most mature and recommended approach.

---

## Key Findings

### 1. Most Popular Framework: OpenSpec (44.5k stars)

[OpenSpec](https://github.com/Fission-AI/OpenSpec) is the leading spec-driven development framework that works with 25+ AI coding tools. It structures extension development as:

```
/opsx:propose "add-dark-mode"
  → Creates: proposal.md, specs/, design.md, tasks.md

/opsx:apply
  → AI implements tasks one by one

/opsx:archive
  → Archives completed work, specs updated
```

**Why it matters for Code Agents**: OpenSpec provides a structured format that lets Code Agents understand what to build before writing code, reducing unpredictability.

### 2. Direct Reference: OpenSpec for Copilot (VS Code Extension)

[OpenSpec for Copilot](https://github.com/atman-33/openspec-for-copilot) is itself a VS Code extension built with AI assistance. It brings SDD workflow into VS Code with:
- Visual spec management in VS Code sidebar
- One-click spec generation via Copilot Chat
- "Start Task" CodeLens on task lists
- Custom prompt management with `.github/prompts/`

**This serves as a direct reference example** of a VS Code extension created with AI tooling.

### 3. Tutorial: Build VS Code Extension with Claude API (45 min)

From [Markaicode](https://markaicode.com/vs/build-a-vs-code-extension-with-ai-in-45-minutes/):

**Architecture Pattern** (extension using AI API):
```
package.json → contributes.commands, contributes.configuration, contributes.keybindings
src/extension.ts → registerCommand → get active editor → call Claude API → replace selection
```

**Standard Extension Project Structure**:
```
├── src/extension.ts    # Main logic
├── package.json         # Extension manifest
├── tsconfig.json
└── .vscodeignore
```

### 4. Workflow for Code Agent → VS Code Extension

| Phase | Action | Tooling |
|-------|--------|---------|
| 1. Spec Generation | Convert requirements → structured spec | OpenSpec or manual spec docs |
| 2. Scaffolding | Generate extension boilerplate | `yo code` (generator-code) |
| 3. Implementation | Implement task by task | Code Agent (Claude Code/Cursor/Copilot) |
| 4. Configuration | Wire commands, settings, keybindings | package.json edits |
| 5. Testing | Verify in Extension Dev Host | F5 in VS Code |
| 6. Packaging | Create .vsix | `vsce package` |

### 5. Recommended Approach

**For a Code Agent building a VS Code extension from requirements:**

1. **Place AGENTS.md** in the project with VS Code extension conventions and context
2. **Use OpenSpec** or structured markdown specs to define what to build
3. **Scaffold with `yo code`** (or have the Code Agent create files directly)
4. **Implement iteratively** - one feature/command at a time
5. **Build for the right AI model** - the extension can integrate Claude, OpenAI, or local models

---

## Source References

- [OpenSpec GitHub](https://github.com/Fission-AI/OpenSpec) - 44.5k stars, MIT license
- [OpenSpec for Copilot GitHub](https://github.com/atman-33/openspec-for-copilot) - VS Code extension reference
- [Build VS Code Extension with AI in 45 min](https://markaicode.com/vs/build-a-vs-code-extension-with-ai-in-45-minutes/) - Tutorial with Claude API
- [Build Custom VSCode Extension with AI in 60 min](https://learn.ryzlabs.com/ai-coding-assistants/how-to-build-a-custom-vscode-extension-with-ai-features-in-60-minutes) - Tutorial with OpenAI API
- [OpenSpec for Copilot Blog Post](https://tech-bridge-log.com/blog/openspec-for-copilot) - Detailed feature breakdown
