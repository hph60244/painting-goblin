# Research: Open-Source RSS Reader Projects

## Overview

A comprehensive survey of notable open-source RSS reader projects across multiple tech stacks, including architecture patterns, data models, and UI approaches. Research conducted May 2026.

---

## Notable Open-Source RSS Readers (by Language/Stack)

### 1. Go

#### Miniflux
- **Stars**: ~9.1k
- **URL**: https://github.com/miniflux/v2
- **Description**: Minimalist and opinionated feed reader. Single binary, no dependencies, very lightweight.
- **Backend**: Go (Golang)
- **Frontend**: Vanilla JavaScript (no framework), bundled into binary via Go `embed`
- **Database**: PostgreSQL only
- **License**: Apache 2.0
- **Key Features**:
  - Atom 0.3/1.0, RSS 1.0/2.0, JSON Feed 1.0/1.1
  - OPML import/export
  - Full-text search (Postgres-powered)
  - Readability parser for content extraction
  - Fever & Google Reader API compatibility
  - 25+ third-party integrations
  - WebAuthn, OAuth2, OpenID Connect auth
  - Background feed scheduler, respects HTTP caching headers
  - Docker, ARM/RISC-V support
- **Architecture**: Clean Go monolith; `internal/` packages for storage, feed parsing, reader, API; no ORM; scheduler-based background polling.

---

### 2. TypeScript / JavaScript (Node.js & Desktop)

#### Folo (formerly Follow)
- **Stars**: ~38.2k
- **URL**: https://github.com/RSSNext/Folo
- **Description**: AI-powered RSS reader. Desktop app + mobile apps + web. Very active, modern.
- **Backend**: TypeScript (Node.js, Hono framework)
- **Frontend**: TypeScript (React/Next.js-style), with desktop (Electron-like), iOS (Swift), Android (Kotlin)
- **Database**: PostgreSQL (via Drizzle ORM)
- **License**: AGPL-3.0
- **Key Features**:
  - AI-powered translation, summarization
  - Social lists & collections (community-driven discovery)
  - Multi-platform: Web, macOS, Windows, Linux, iOS, Android
  - Dynamic content support (video, audio, images)
  - RSSHub integration
  - Monorepo (pnpm workspaces, Turbo)
- **Architecture**: Monorepo with `apps/` (desktop, mobile) and `packages/` (shared libs). API layer in `api/`, plugins system in `plugins/`.

#### Alduin
- **Stars**: ~306
- **URL**: https://github.com/AlduinApp/alduin
- **Description**: Desktop RSS/Atom/JSON feed reader built with Electron.
- **Language**: TypeScript
- **Frontend**: React (desktop via Electron)
- **Key Features**: Cross-platform desktop app, supports RSS/Atom/JSON feeds.

#### Refedd
- **Stars**: ~178
- **URL**: https://github.com/michaelkremenetsky/Refeed
- **Description**: Open-source RSS reader.
- **Language**: TypeScript

#### Dino RSS (Electron)
- **Stars**: ~295
- **URL**: https://github.com/richshaw2015/dino-rss-electron
- **Description**: Simple, efficient open-source RSS reader service.
- **Language**: Svelte + Electron

---

### 3. PHP

#### FreshRSS
- **Stars**: ~14.9k
- **URL**: https://github.com/FreshRSS/FreshRSS
- **Description**: Self-hosted RSS feed aggregator. Lightweight, powerful, multi-user.
- **Backend**: PHP 8.1+
- **Frontend**: HTML/CSS/vanilla JS, responsive design
- **Database**: PostgreSQL 10+, SQLite, or MySQL 8.0+ / MariaDB 10.6+
- **License**: AGPL-3.0
- **Key Features**:
  - Multi-user with anonymous reading mode
  - WebSub (instant push notifications)
  - XPath-based web scraping for sites without RSS
  - Google Reader API & Fever API compatibility
  - 20+ language translations
  - Extensions system
  - Docker support
  - OPML import/export
  - CLI interface
- **Architecture**: PHP MVC (MINZ framework), `app/` for controllers/models, `lib/` for libraries (SimplePie for parsing), `extensions/` for plugins.

#### Tiny Tiny RSS (tt-rss)
- **Stars**: ~713
- **URL**: https://github.com/tt-rss/tt-rss
- **Description**: Web-based news feed reader and aggregator. Mature project with long history.
- **Language**: PHP
- **Database**: PostgreSQL
- **License**: GPL-2.0

---

### 4. Ruby

#### Stringer
- **Stars**: ~4.1k
- **URL**: https://github.com/stringer-rss/stringer
- **Description**: Self-hosted, anti-social RSS reader. No social features, no recommendations.
- **Backend**: Ruby on Rails
- **Frontend**: Backbone.js, Twitter Bootstrap
- **Database**: PostgreSQL
- **License**: MIT
- **Key Features**:
  - Keyboard shortcuts
  - Fever API compatibility (for mobile clients)
  - Heroku one-click deploy
  - No external dependencies, no machine learning
  - Multiple language translations
- **Architecture**: Rails MVC, uses Feedjira and Feedbag for feed parsing, GoodJob for background job processing.

---

### 5. C++ / Rust

#### Newsboat
- **Stars**: ~3.8k
- **URL**: https://github.com/newsboat/newsboat
- **Description**: RSS/Atom feed reader for text terminals. Actively maintained fork of Newsbeuter.
- **Language**: C++17 + Rust
- **Frontend**: TUI (text terminal UI via STFL library)
- **Database**: SQLite3
- **License**: MIT
- **Key Features**:
  - Powerful built-in HTML renderer (no browser needed)
  - Article filtering by title, author, content
  - Query feeds (meta-feeds by arbitrary criteria)
  - Macro system (custom key sequences)
  - Podcast support
  - Integrations with The Old Reader, NewsBlur, FeedHQ
  - Bookmarking scripts
- **Architecture**: C++ core with Rust components. STFL for TUI, libcurl for HTTP, SQLite3 for storage, libxml2 for XML parsing.

---

### 6. Swift (macOS / iOS)

#### NetNewsWire
- **Stars**: ~10k
- **URL**: https://github.com/Ranchero-Software/NetNewsWire
- **Description**: Free and open-source feed reader for macOS and iOS.
- **Language**: Swift
- **Platform**: macOS, iOS (native Apple platforms)
- **Database**: (local storage)
- **License**: MIT
- **Key Features**:
  - RSS, Atom, JSON Feed, RSS-in-JSON
  - iCloud sync between devices
  - Feedly sync support
  - Reader view
  - AppleScript support
  - Widgets
- **Architecture**: Swift/SwiftUI for macOS and iOS. Xcode project with shared modules.

---

### 7. Python (Adjacent / Notable)

#### Linkding (Python/Django)
- **Stars**: ~10.5k
- **URL**: https://github.com/sissbruecker/linkding
- **Description**: Self-hosted bookmark manager (has RSS reading capabilities).
- **Language**: Python (Django)
- **Database**: SQLite / PostgreSQL
- **License**: MIT
- **Note**: Not a pure RSS reader but shares many architectural patterns (feed fetching, parsing, storage). Demonstrates Python/Django approach to feed management.

---

## Common Architecture Patterns

### Data Flow
```
[Feed Sources] → [HTTP Fetcher] → [Feed Parser] → [Storage] → [API/UI]
                                ↕
                     [Background Scheduler]
```

1. **Polling**: Most readers use a background scheduler (cron-like or internal) to periodically fetch feeds. Miniflux has an internal scheduler; FreshRSS uses cron.
2. **HTTP Fetching**: Respects `If-Modified-Since`, `ETag`, `Last-Modified` headers to avoid redundant downloads.
3. **Parsing**: Libraries like SimplePie (PHP), Feedjira (Ruby), and custom Go parsers handle RSS/Atom/JSON feed formats.
4. **Content Extraction**: Many readers include Readability-like algorithms (e.g., Miniflux's local Readability parser) to extract article bodies.
5. **Storage**: SQL databases (PostgreSQL, SQLite, MySQL) are the norm. Relationships are stored via foreign keys.

### Common Backend Components

| Component | Description |
|-----------|-------------|
| Feed Fetcher | HTTP client that downloads feed XML/JSON |
| Feed Parser | Converts raw feed data to structured objects |
| Content Extractor | Readability/mozilla parser for article body |
| Storage Layer | Database models & queries |
| Scheduler | Cron-like feed refresh mechanism |
| API Layer | REST API (REST, Fever API, Google Reader API) |
| Auth Layer | User authentication & session management |
| UI Renderer | HTML templates or client-side rendering |

---

## Typical Data Models

### Feed
```
Feed {
  id: UUID/integer (PK)
  url: string (unique)
  title: string
  site_url: string
  description: text
  icon_url: string (favicon)
  category_id: FK → Category
  last_fetched_at: datetime
  error_count: integer
  created_at: datetime
  updated_at: datetime
}
```

### Entry (Article)
```
Entry {
  id: UUID/integer (PK)
  feed_id: FK → Feed
  guid: string (unique per feed, from feed XML)
  url: string (link to original article)
  title: string
  content: text (full article)
  summary: text (short description/excerpt)
  author: string
  published_at: datetime
  updated_at: datetime
  is_read: boolean (default: false)
  is_starred: boolean (default: false)
  categories: M2M → Category
}
```

### Category
```
Category {
  id: UUID/integer (PK)
  user_id: FK → User
  title: string
  created_at: datetime
}
```

### Subscription (User-Feed relationship)
```
Subscription {
  id: UUID/integer (PK)
  user_id: FK → User
  feed_id: FK → Feed
  category_id: FK → Category (nullable)
  title: string (custom override)
  created_at: datetime
}
```

### User
```
User {
  id: UUID/integer (PK)
  username: string (unique)
  password_hash: string
  email: string
  theme: string
  created_at: datetime
}
```

### Enclosure (attachments)
```
Enclosure {
  id: UUID/integer (PK)
  entry_id: FK → Entry
  url: string
  type: string (MIME type)
  length: integer (bytes)
  duration: integer (for podcasts)
}
```

### Common Variations
- Some implementations (FreshRSS, Miniflux) merge Category into a tags/labels system.
- Some use `user_id` directly on Categories instead of M2M through Entries.
- `guid` uniqueness is typically enforced per-feed, not globally.

---

## Frontend Approaches

| Type | Examples | Tech Used |
|------|----------|-----------|
| **Web App (SPA/MPA)** | FreshRSS, Miniflux, tt-rss | Vanilla JS, HTML templates (PHP/Go), responsive CSS |
| **Desktop App (Electron)** | Alduin, Dino RSS, Folo Desktop | Electron, React, Svelte, TypeScript |
| **CLI / TUI** | Newsboat, Newsbeuter | STFL, ncurses, C++/Rust |
| **Native Mobile** | NetNewsWire (iOS), Folo (iOS/Android) | Swift, Kotlin |
| **PWA** | Miniflux, FreshRSS | Service Workers, manifest.json |
| **Desktop Native** | NetNewsWire (macOS) | Swift, AppKit/SwiftUI |

### Common UI patterns:
- **Three-panel layout**: Feeds list (left) → Entries list (center) → Article content (right)
- **Keyboard shortcuts**: Nearly all readers implement `j`/`k` navigation, `m` to toggle read, `s` to star
- **Dark/light themes**: Most support both
- **Responsive design**: Essential for mobile web readers

---

## API Standards

Two dominant API standards are widely replicated:

### Google Reader API
- Used by: Miniflux, FreshRSS, Stringer (partial)
- Endpoints for: subscription listing, tag listing, entry listing, marking read/starred
- Well-documented and supported by many mobile clients

### Fever API
- Used by: Miniflux, FreshRSS, Stringer
- Simpler than Google Reader API but fewer features
- Popular with older iOS clients (Reeder, Unread)

---

## Key Takeaways for Building an RSS Reader

1. **Start with the parser**: Choose a good feed parsing library (feedparser in Python, gofeed in Go, SimplePie in PHP).
2. **Respect HTTP caching**: Always implement `If-Modified-Since` / `ETag` to be a good citizen.
3. **Background scheduling is essential**: Feeds must update asynchronously; use a job queue or scheduler.
4. **Content extraction is hard**: Mozilla's Readability is the gold standard for extracting article text.
5. **API compatibility matters**: Supporting Fever or Google Reader API means instant access to existing mobile clients.
6. **SQL databases work well**: PostgreSQL is overwhelmingly the most common choice among serious readers.
7. **Three-panel layout is standard**: Users expect the feed/entry/article structure.
8. **OPML import/export is table stakes**: Every major reader supports it for onboarding/offboarding.
9. **Multi-user vs single-user**: Decide early; it affects the entire data model design.
10. **Privacy features increasingly matter**: Tracking pixel removal, URL sanitization, CSP headers.

---

## Source URLs

| Project | URL |
|---------|-----|
| Miniflux | https://github.com/miniflux/v2 |
| Folo | https://github.com/RSSNext/Folo |
| FreshRSS | https://github.com/FreshRSS/FreshRSS |
| Tiny Tiny RSS | https://github.com/tt-rss/tt-rss |
| Stringer | https://github.com/stringer-rss/stringer |
| Newsboat | https://github.com/newsboat/newsboat |
| NetNewsWire | https://github.com/Ranchero-Software/NetNewsWire |
| Alduin | https://github.com/AlduinApp/alduin |
| Dino RSS | https://github.com/richshaw2015/dino-rss-electron |
| Refedd | https://github.com/michaelkremenetsky/Refeed |
| Linkding | https://github.com/sissbruecker/linkding |
| GitHub Search (RSS Readers) | https://github.com/search?q=open+source+rss+reader&type=repositories&s=stars&o=desc |
