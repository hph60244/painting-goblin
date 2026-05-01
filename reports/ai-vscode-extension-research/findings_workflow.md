# Findings: Workflow Patterns for Code Agent Extension Development

## Pattern 1: Spec-Driven Development (SDD) with OpenSpec
1. **Define requirements** in structured spec format (proposal.md)
2. **AI generates specs** (requirements, design, tasks) based on proposal
3. **Implement task by task** using AI coding agent
4. **Archive** completed work
5. **Tools**: OpenSpec CLI + Claude Code / Cursor / Copilot

## Pattern 2: Manual Scaffold + AI API Integration
1. **Scaffold** extension with `yo code` (generates boilerplate)
2. **Install AI SDK** (Anthropic, OpenAI, etc.)
3. **Implement** extension logic with AI API calls
4. **Configure** package.json with commands, settings, keybindings
5. **Test** with Extension Development Host (F5)
6. **Package** with `vsce package`

## Pattern 3: AI Agent Generates Extension from Scratch
1. **Provide requirement document** to AI coding agent (Claude Code, Cursor)
2. **Agent scaffolds** the project structure
3. **Agent implements** extension logic iteratively
4. **Human reviews** and provides feedback
5. **Agent refines** based on feedback

## Recommended Workflow for Code Agent → VS Code Extension

### Phase 1: Spec Generation
```
Human: Write requirement document
  → Code Agent: Generate structured spec (using OpenSpec or similar)
  → Output: proposal.md, design.md, tasks.md
```

### Phase 2: Implementation (Task by Task)
```
For each task in tasks.md:
  Code Agent reads task description
  Code Agent implements the task (modifies extension.ts, package.json, etc.)
  Human reviews and provides feedback
  Code Agent refines
```

### Phase 3: Testing & Packaging
```
Code Agent: Runs npm run compile
Code Agent: Helps set up tests
Human: Tests in Extension Dev Host (F5)
Code Agent: Final refinements
Human: Packages with vsce
```

## Key Considerations for Code Agents
1. **Context window management**: VS Code extensions have many config files (package.json, tsconfig, etc.) - need to manage context
2. **Iterative development**: Best to break down into small tasks and implement one at a time
3. **File structure awareness**: Agent needs to understand the standard VS Code extension project layout
4. **Extension API knowledge**: Agent should be prompted with relevant VS Code API patterns
5. **Testing in real environment**: Some things (like webviews, decoration) need visual verification

## AGENTS.md / Custom Instructions Pattern
Place AGENTS.md in project root or .github/ to give the Code Agent persistent context about:
- Project structure conventions
- Coding standards
- VS Code extension best practices
- Testing approach

## Source: OpenSpec for Copilot workspace layout
```
.github/
├── prompts/         # Markdown prompts for AI
├── agents/          # Agent definitions
├── instructions/    # Project instructions
openspec/
├── AGENTS.md        # Steering rules
├── project.md       # Project spec
├── <spec>/
│   ├── requirements.md
│   ├── design.md
│   └── tasks.md
```
