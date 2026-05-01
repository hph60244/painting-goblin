# Findings: Tutorials and Guides for Building VS Code Extensions with AI

## 1. "Build a VS Code Extension with AI in 45 Minutes" (Markaicode, Feb 2026)
- **URL**: https://markaicode.com/vs/build-a-vs-code-extension-with-ai-in-45-minutes/
- **Approach**: Build extension manually then integrate Claude API
- **Extension**: AI Refactor Helper - code refactoring via Claude
- **Key Steps**:
  1. Scaffold with `yo code` (Yeoman generator)
  2. Add Anthropic SDK (`@anthropic-ai/sdk`)
  3. Register commands in package.json
  4. Implement activation with API integration
  5. Add settings for API key configuration
  6. Package with `vsce package`
  7. Publish to marketplace
- **Tech Stack**: TypeScript, VS Code Extension API, Claude API, yo generator-code

## 2. "How to Build a Custom VSCode Extension with AI Features in 60 Minutes" (Ryz Labs, Feb 2026)
- **URL**: https://learn.ryzlabs.com/ai-coding-assistants/how-to-build-a-custom-vscode-extension-with-ai-features-in-60-minutes
- **Approach**: Manual build + OpenAI integration
- **Extension**: AI Code Assistant - code suggestions
- **Key Steps**:
  1. Scaffold with `npx yo code`
  2. Install axios for API calls
  3. Register command in package.json
  4. Wire up OpenAI API in extension.ts
  5. Test with F5
- **Tech Stack**: TypeScript, OpenAI API, axios, yo generator-code

## 3. VSCode Extension Generator (yo code)
- **URL**: https://www.npmjs.com/package/generator-code
- **Standard scaffolding tool** for VS Code extensions
- Creates project with: package.json, src/extension.ts, tsconfig.json, etc.

## Common Architecture Pattern
```
VS Code Extension Project Structure:
├── .vscode/
├── node_modules/
├── src/
│   └── extension.ts        # Activation + command registration
├── package.json             # Contributes (commands, config, keybindings)
├── tsconfig.json
└── .vscodeignore
```

## Key VS Code API Concepts
- `vscode.commands.registerCommand` - register commands
- `vscode.window.activeTextEditor` - access editor
- `vscode.workspace.getConfiguration` - read settings
- `vscode.window.withProgress` - show progress
- `editor.edit()` - modify document
- `package.json` `contributes` section - declare commands, config, keybindings
