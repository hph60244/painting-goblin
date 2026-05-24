# AI-Generated Chrome Extensions: Research Findings

## 1. Tutorials Showing AI Building a Chrome Extension Step by Step

### "How to build a Chrome Extension with AI" — Prompt Warrior (Moritz Kremb, May 2025)
- **Approach**: Uses Claude (or ChatGPT) for planning, Cursor as AI code editor, and no programming experience required.
- **Process**: (1) Prompt AI to plan MVP features and technical considerations, (2) Build iteratively in Cursor (core functionality first → main AI feature → supporting features → UI polish), (3) Publish to Chrome Web Store.
- **Key quote**: "The key is to keep things iterative and build up complexity gradually: Start by building the simplest possible version that proves your core idea works."
- **URL**: https://www.thepromptwarrior.com/p/how-to-build-a-chrome-extension-with-ai

### "AI tutorial: I built a browser extension in a few hours — you can, too" — Meryam Bukhari (May 2025)
- **Approach**: Used Claude chatbot + VS Code + Gemini API. No prior extension experience.
- **Process**: (1) Prompt Claude with a sketch and description, (2) Edit HTML/JS from Claude's output, (3) Get API key from Google AI Studio, (4) Test prompts, (5) Add Chrome Downloads API integration.
- **Key tools**: Claude for code generation, Thunder Client for API debugging, Gemini API for recommendations.
- **Key quote**: "I built a browser extension for Chrome in a few hours using Claude — and you can, too!"
- **GitHub repo**: https://github.com/123mbam/3rdextension
- **URL**: https://meryam.substack.com/p/ai-tutorial-i-built-a-browser-extension

### "Building a Chrome Extension from Scratch with AI/ML API, Deepgram Aura, and IndexedDB" — dev.to (Oct 2024)
- **Approach**: Traditional tutorial-style guide for building AI-powered extensions.
- **URL**: https://dev.to/abdibrokhim/building-a-chrome-extension-from-scratch-with-aiml-api-deepgram-aura-and-indexeddb-integration-25hd

### "Build a Chrome Extension Using AI with Cursor" — YouTube Tutorial
- **Approach**: Step-by-step video tutorial using Cursor AI code editor.
- **URL**: https://www.youtube.com/watch?v=vIcDmkK6vMs

### "A Practical Guide to Building AI-Powered Chrome Extensions" — Medium / Slalom Build (May 2025)
- **Approach**: Modern best practices guide for building AI-powered Chrome extensions from scratch.
- **URL**: https://medium.com/slalom-build/a-guide-to-building-ai-powered-chrome-extensions-d866db9a8106

### "How to Build a Chrome Extension with AI: Complete Developer Guide" — Anurag Wagh (Mar 2026)
- **Approach**: Uses Anthropic API with step-by-step coverage of manifest, popup UI, content scripts, and AI integration.
- **URL**: https://www.anuragwagh.me/blog/how-to-build-chrome-extension-with-ai

### "How to Build Transformers Chrome Extensions: Browser AI Tools"
- **Approach**: Uses Transformers.js for in-browser AI text analysis (sentiment, NLP) without servers.
- **URL**: https://markaicode.com/build-transformers-chrome-extensions-browser-ai/
- **Date**: June 2025

---

## 2. GitHub Repositories with AI-Generated Extension Code

### Google Chrome Official Samples — AI Extensions
- **Repo**: https://github.com/GoogleChrome/chrome-extensions-samples
- **Stars**: 17.5k+
- **Key samples**:
  - **Gemini Cloud API extension** (`ai.gemini-in-the-cloud`): Side-panel chat interface using Gemini API. Includes manifest.json, background.js, sidepanel JS bundle.
    - URL: https://github.com/GoogleChrome/chrome-extensions-samples/tree/main/functional-samples/ai.gemini-in-the-cloud
  - **Gemini Nano on-device extension** (`ai.gemini-on-device`): Uses Prompt API with Gemini Nano (client-side, no cloud needed).
    - URL: https://github.com/GoogleChrome/chrome-extensions-samples/tree/main/functional-samples/ai.gemini-on-device
  - **Client-side summarization** (`ai.gemini-on-device-summarization`): Summarizer API for current tab content.
    - URL: https://github.com/GoogleChrome/chrome-extensions-samples/tree/main/functional-samples/ai.gemini-on-device-summarization

### 3rdextension — AI-Built Extension (by Meryam Bukhari)
- **Repo**: https://github.com/123mbam/3rdextension
- **Description**: Reading assistant extension built entirely via Claude collaboration. Features notes persistence, download, and Gemini-based recommendations.

---

## 3. Case Studies and Blog Posts

### Chrome for Developers — Official AI Extensions Portal
- **URL**: https://developer.chrome.com/docs/extensions/ai
- **Key content**: Official documentation from Google on building AI-powered Chrome extensions, covering client-side AI (Gemini Nano on-device) and cloud AI (Gemini API). Lists built-in AI APIs: Prompt API, Writer API, Rewriter API, Translator API, Language Detector API, Summarizer API, Proofreader API.
- **Key quote**: "You can build AI-powered extensions that summarize text, help with translation, generate content, assist with coding, provide recommendations, personalize user interfaces, and so much more."
- **Case study referenced**: Google Creative Lab team used AI + extensions to build an interactive creative coding experience: https://developers.googleblog.com/how-its-made-exploring-ai-x-learning-through-shiffbot-an-ai-experiment-powered-by-the-gemini-api/

### "Building a Chrome Extension with AI — No Coding Experience Required" — Prompt Warrior
- Describes building a "Tweet Idea Remixer" extension using only AI prompting. Published to Chrome Web Store.
- **Key workflow**: Planning with AI → iterative coding in Cursor (4 layers: core → main feature → supporting → UI) → store publishing with AI-generated descriptions, privacy policy, and screenshots.

---

## 4. Requirements Document as Input for AI Agent

### The Prompt Warrior Approach (Requirements → AI → Extension)
- The tutorial explicitly demonstrates using a plain-language requirements prompt as the starting point for building an extension.
- **Prompt template used**:
  ```
  "I want to build a [Chrome extension that lets me select a tweet, click the Chrome extension,
  and it will then generate 10 ideas similar to that tweet...]. Help me think about the essential
  MVP features for this extension to start with. Keep it really simple. Help me with any technical
  consideration I should know about. Keep in mind that I do not have any programming experience."
  ```
- The AI then produces: MVP feature list, technical architecture overview, file structure (manifest.json, popup.html, content.js, background.js), and data flow.
- **Conclusion**: The requirements/prompt acts as a "spec document" that the AI uses to scaffold the entire project.

### Meryam Bukhari's Approach (Sketch + Description → Claude → Extension)
- Used a hand-drawn sketch plus a natural language description as the "requirements document" for Claude.
- **First prompt**: Used Google's task/persona/format/context framework to describe the extension.
- Claude generated the initial HTML and JS code directly from this prompt-based spec.

---

## 5. YouTube Videos and Online Courses

### YouTube Videos
1. **"Build a Chrome Extension Using AI with Cursor | Step-by-Step Tutorial"**
   - URL: https://www.youtube.com/watch?v=vIcDmkK6vMs
   - Focus: Using Cursor AI code editor

2. **Prompt Warrior YouTube Channel** — https://www.youtube.com/@promptwarrior
   - Multiple videos on building software (including extensions) with AI

3. Google's prompting framework video referenced by Meryam Bukhari:
   - URL: https://www.youtube.com/watch?v=lp-Ft3Ex5_k

### Online Courses / Communities
1. **Prompt Warrior Community** (Skool) — https://www.skool.com/promptwarrior
   - Paid community with courses, templates, and live Q&A sessions on building software with AI, including Chrome extensions.

2. **Chrome for Developers — Extensions and AI** (Free official docs)
   - URL: https://developer.chrome.com/docs/extensions/ai
   - Includes sample code, API references, and best practices.

3. **Google AI Studio** (Free API access)
   - URL: https://aistudio.google.com/
   - Free tier for prototyping Gemini API integrations.

---

## Summary of Key Patterns

| Pattern | Tools Used | Approach |
|---------|-----------|----------|
| Chatbot-only | Claude/ChatGPT + VS Code | Prompt → code → manual refinement |
| AI Code Editor | Cursor + Claude/GPT | Iterative in-editor prompting and debugging |
| Official SDK | Gemini API + Chrome Extensions API | Structured, documented integration |
| No-code AI | Cursor + v0.dev | Visual design via AI, code generation, store submission |

### Recurring Best Practices
1. Start with a plain-language requirements prompt/spec
2. Build the simplest MVP first, then layer on complexity
3. Use AI not just for code generation but also for planning, debugging, and store listing content
4. Keep API keys out of the code — ask users to provide their own
5. Chrome Web Store review typically takes a few days; permission justifications can be AI-drafted
