# Chrome Extension Basics (Manifest V3)

**Date:** 2026-05-01
**Source:** Chrome for Developers documentation

---

## 1. Architecture Overview (Manifest V3)

Chrome Extensions are built using standard web technologies: **HTML, CSS, and JavaScript**. They enhance the browsing experience by customizing the UI, observing browser events, and modifying web pages.

> *"You can build extensions using the same web technologies that are used to create web applications: HTML, CSS, and JavaScript."*
> — [Chrome Extensions Get Started](https://developer.chrome.com/docs/extensions/get-started)

The platform enforces a **single-purpose principle**:

> *"When choosing which features to support, make sure your extension fulfills a single purpose that is narrowly defined and easy to understand."*
> — [Chrome Extensions Get Started](https://developer.chrome.com/docs/extensions/get-started)

Key architectural requirements:
- **All logic must be included in the extension package** — no remotely hosted JavaScript code may be downloaded at runtime.
- Extensions have access to both standard [Web APIs](https://developer.mozilla.org/docs/Web/API) and [Chrome Extension APIs](https://developer.chrome.com/docs/extensions/reference).

---

## 2. Key Components

### Manifest (`manifest.json`)
The only required file with a specific filename. Must be in the extension's root directory.

> *"The manifest records important metadata, defines resources, declares permissions, and identifies which files to run in the background and on the page."*
> — [Chrome Extensions Get Started](https://developer.chrome.com/docs/extensions/get-started)

### Service Workers (Background Scripts)
Replaces the persistent background page from MV2. Event-driven, runs only when needed, and cannot access the DOM directly.

> *"A service worker runs in the background and handles browser events, like removing a bookmark, or closing a tab. They don't have access to the DOM, but you can combine it with an offscreen document for this use case."*
> — [About Extension Service Workers](https://developer.chrome.com/docs/extensions/develop/concepts/service-workers)

> *"An extension service worker is loaded when it is needed, and unloaded when it goes dormant."*
> — [About Extension Service Workers](https://developer.chrome.com/docs/extensions/develop/concepts/service-workers)

Extension service workers respond to extension events (navigation, notifications, tab closures) in addition to standard service worker events. They are registered and updated differently from web service workers.

### Content Scripts
Run JavaScript in the context of a web page. Can read/modify the DOM of pages the user visits.

> *"Chrome extensions enhance the browsing experience by customizing the user interface, observing browser events, and modifying the web."*
> — [Chrome Extensions Get Started](https://developer.chrome.com/docs/extensions/get-started)

### Toolbar Action (Popup)
Execute code or show a popup when the user clicks the extension toolbar icon using the Action API.

### Side Panel
Custom UI that displays in the browser's side panel.

### DeclarativeNetRequest
Intercept, block, or modify network requests declaratively (replaces blocking `webRequest` from MV2).

---

## 3. Manifest JSON Structure

### Required Fields (Extensions Platform)
```json
{
  "manifest_version": 3,
  "name": "My Extension",
  "version": "1.0.0"
}
```
- **`manifest_version`** — Integer. Only supported value is `3`.
- **`name`** — String. Max 75 chars. Identifies extension in Chrome Web Store and `chrome://extensions`.
- **`version`** — String. Version number of the extension.

### Required Fields (Chrome Web Store)
- **`description`** — String. Max 132 chars. Describes the extension on the store and management page.
- **`icons`** — One or more icons representing the extension.

### Minimal Manifest Example
```json
{
  "manifest_version": 3,
  "name": "Minimal Manifest",
  "version": "1.0.0",
  "description": "A basic example extension with only required keys",
  "icons": {
    "48": "images/icon-48.png",
    "128": "images/icon-128.png"
  }
}
```
— [Manifest File Format](https://developer.chrome.com/docs/extensions/reference/manifest)

### Common Optional Keys
| Key | Purpose |
|------|---------|
| `background` | Specifies the service worker JS file |
| `content_scripts` | JS/CSS files injected into specified pages |
| `action` | Toolbar icon and popup behavior |
| `permissions` | Enables use of specific Chrome APIs |
| `host_permissions` | URL patterns the extension can interact with |
| `options_page` / `options_ui` | Extension settings page |
| `side_panel` | Side panel HTML file |
| `commands` | Keyboard shortcuts |
| `web_accessible_resources` | Files accessible to web pages/other extensions |
| `content_security_policy` | Restrictions on scripts/styles/resources |
| `declarative_net_request` | Static rules for network request modification |

---

## 4. Messaging Between Components

Two message passing APIs exist:

### One-Time Requests (`runtime.sendMessage` / `tabs.sendMessage`)
Send a single JSON-serializable message to another part of the extension and optionally get a response.

**From content script to service worker:**
```javascript
// content-script.js
(async () => {
  const response = await chrome.runtime.sendMessage({greeting: "hello"});
  console.log(response);
})();
```

**Listening for messages (service worker):**
```javascript
// service-worker.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.greeting === "hello") {
    sendResponse({farewell: "goodbye"});
  }
});
```

> *"When the event listener is called, a `sendResponse` function is passed as the third parameter. This is a function that can be called to provide a response."*
> — [Message Passing](https://developer.chrome.com/docs/extensions/develop/concepts/messaging)

**Response patterns:**
- **Synchronous:** Call `sendResponse()` immediately
- **Async via `return true`:** Return literal `true` to keep channel open
- **Async via Promise (Chrome 146+):** Return a Promise from the listener

### Long-Lived Connections (`runtime.connect` / `tabs.connect`)
Reusable channels for multiple messages:

```javascript
// Open a connection
const port = chrome.runtime.connect({name: "knockknock"});
port.postMessage({joke: "Knock knock"});
port.onMessage.addListener((msg) => { /* handle response */ });

// Listen for connections
chrome.runtime.onConnect.addListener((port) => {
  port.onMessage.addListener((msg) => {
    port.postMessage({question: "Who's there?"});
  });
});
```

**Serialization:** Chrome uses JSON serialization (unlike other browsers which use structured clone). Max message size: **64 MiB**.

### Cross-Extension Messaging
Use `runtime.onMessageExternal` / `runtime.onConnectExternal` to communicate between different extensions. Specify allowed external extensions via `externally_connectable` in manifest.

### Web Page to Extension Messaging
Web pages can send messages to extensions if the extension declares `externally_connectable` match patterns in manifest. Extensions **cannot** send messages *to* web pages.

### Security Considerations
> *"Content scripts are less trustworthy than the extension service worker. Assume that messages from a content script might have been crafted by an attacker and make sure to validate and sanitize all input."*
> — [Message Passing](https://developer.chrome.com/docs/extensions/develop/concepts/messaging)

---

## 5. Manifest V2 vs V3 Key Differences

### 5.1 Background Pages → Service Workers
- **MV2:** Persistent background page (full HTML page, always running, DOM access)
- **MV3:** Event-driven service worker (loaded on demand, no DOM access, dormant when idle)

> *"Extensions in Manifest V2 had a long-lived background page that took up resources, even when an extension wasn't running. In Manifest V3, we have moved the background context to service workers, which run only when needed."*
> — [What is Manifest V3](https://developer.chrome.com/docs/extensions/develop/migrate/what-is-mv3)

### 5.2 No Remotely Hosted Code
- **MV2:** Could execute remotely hosted JavaScript (eval(), remote scripts)
- **MV3:** All JavaScript must be included in the extension package

> *"Manifest V3 removes the ability for an extension to use remotely hosted code, which presents security risks by allowing unreviewed code to be executed in extensions."*
> — [What is Manifest V3](https://developer.chrome.com/docs/extensions/develop/migrate/what-is-mv3)

### 5.3 Network Request Modification
- **MV2:** Blocking `webRequest` API (proxy all traffic, performance/privacy cost)
- **MV3:** `declarativeNetRequest` API (declarative rules, no traffic proxying)

> *"We are deprecating the blocking version of the webRequest API. The new declarativeNetRequest API provides a safer alternative for many use cases."*
> — [What is Manifest V3](https://developer.chrome.com/docs/extensions/develop/migrate/what-is-mv3)

### 5.4 Promise-Based APIs
MV3 adds promise support for Chrome Extension APIs, enabling modern async/await patterns.

### 5.5 New Capabilities in MV3
- Side Panel API
- Offscreen Documents (for DOM access from service workers)
- Improved security model
- Enhanced permissions system (`host_permissions` separated from `permissions`)

---

## Sources

- Chrome Extensions Get Started: https://developer.chrome.com/docs/extensions/get-started
- About Extension Service Workers: https://developer.chrome.com/docs/extensions/develop/concepts/service-workers
- Message Passing: https://developer.chrome.com/docs/extensions/develop/concepts/messaging
- Manifest File Format: https://developer.chrome.com/docs/extensions/reference/manifest
- What is Manifest V3: https://developer.chrome.com/docs/extensions/develop/migrate/what-is-mv3
