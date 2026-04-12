# Painting Goblin - Research Findings

## Definition

"Painting Goblin" refers to two distinct but related concepts:

1. **Internet Meme/Folklore**: A popular concept within *The Sims* gaming community where players create a Sim (usually with green skin) confined to a basement or isolated room, whose sole purpose is to paint constantly and generate income for the household. This practice became known as the "Painting Goblin" folklore.

2. **Software Projects**:
   - **The Painting Goblin Game**: A game developed in Processing (2016) that implements utility-based AI, inspired by the Sims meme.
   - **painting-goblin Task Processing System**: A Python-based file-system task queue processor (2026) that uses publisher-subscriber pattern and OpenCode AI to execute tasks.

## Purpose

### Meme Purpose
- Provides an automated income source within *The Sims* games
- Explores game mechanics and player creativity in exploiting simulation systems
- Serves as a humorous commentary on labor exploitation and optimization in gaming

### Game Project Purpose (gozu66)
- Technical exercise in utility-based game AI
- Educational project to explore decision-making systems for semi-autonomous agents
- Implements the narrative concept of managing a goblin's environment to maximize painting output

### Task Processing System Purpose (fnaith)
- Automate task execution using AI agents (OpenCode)
- Provide a robust, file-based task queue system with monitoring and scheduling
- Enable research and development of AI skills through scheduled tasks

## Nature

### Meme Nature
- Community-generated folklore, spread via forums (4chan, Reddit), social media, and gaming communities
- Emergent gameplay strategy that became a shared cultural reference
- Often accompanied by screenshots and stories of players' "painting goblins"

### Game Nature
- **Language**: Processing (Java-based)
- **Architecture**: Object-oriented, with three main components: AI Goblin, interface, game manager
- **Gameplay**: Player controls environment to meet goblin's needs, sell paintings, reinvest earnings
- **Status**: Appears to be a completed academic/technical exercise (last commit May 2016)

### Task Processing System Nature
- **Language**: Python 3.14+
- **Architecture**: Publisher-Subscriber pattern with file system as message queue
- **Components**: Executor (task runner), Scheduler (cron-based task creation), Monitor (timeout handling)
- **Integration**: Uses OpenCode AI CLI for task execution
- **Status**: Active development (first commit April 2026)

## Creator

### Meme Creator
- Origin unclear, attributed to anonymous *The Sims* player community
- Popularized through 4chan and Reddit posts circa 2014-2015
- Early references include Imgur post "Painting Goblin - sims post" (image ID: NrJku9x)

### Game Creator
- **GitHub User**: gozu66 (Richie)
- **Repository**: https://github.com/gozu66/ThePaintingGoblin
- **Description**: "A game made in Processing"

### Task Processing System Creator
- **GitHub User**: fnaith
- **Repository**: https://github.com/fnaith/painting-goblin
- **Description**: "任務處理系統 - 基於檔案系統的任務佇列處理器" (Task processing system - file system-based task queue processor)

## Creation Date

### Meme
- Emerged circa 2014-2015 based on earliest online references
- Known Reddit post from 2014 (r/thesims/comments/1zela3/)
- Imgur post likely from similar timeframe

### Game Project
- **First Commit**: March 20, 2016 (23f9dd4)
- **Last Commit**: May 5, 2016 (f93e860)
- **Active Development Period**: March-May 2016

### Task Processing System
- **First Commit**: April 5, 2026 (66f9f6a)
- **Active Development**: Ongoing as of April 2026

## Primary Function

### Meme Function
- To provide humorous optimization strategy for *The Sims* gameplay
- To create shared cultural reference within gaming community
- To explore ethical boundaries in simulation games

### Game Function
- Implement utility-based AI for autonomous agent decision-making
- Provide interactive simulation where player manages environment to influence goblin behavior
- Generate paintings as output based on environmental factors

### Task Processing System Function
- **Task Queue Management**: Monitor directories (todo, doing, done, failed) and move tasks through workflow
- **Task Execution**: Use OpenCode AI to execute markdown-formatted tasks
- **Scheduling**: Cron-based task generation from template files
- **Monitoring**: Timeout handling, logging, and cleanup of stale tasks
- **Skill Development**: Framework for developing AI skills (research, app building, etc.)

## Key Facts

### Meme Facts
- Reference to "The Sims folklore of a Painting Goblin" appears in game design document
- Players often describe feeling guilt for exploiting their painting goblins
- The concept has been featured in articles from The Cut, Pedestrian.tv, and gaming blogs
- Some players create elaborate backstories and living conditions for their goblins

### Game Facts
- Uses Processing IDE and language
- Design document outlines three-part architecture
- Includes image reference to original meme (Imgur URL)
- License: MIT
- 41 commits total

### Task Processing System Facts
- Supports parameterized tasks through config.ini
- Implements file locking to prevent concurrent processing
- Includes automatic cleanup of logs and temporary files
- Configurable via config.ini with directory paths, timing, and OpenCode executable
- Integrates with pre-commit hooks for code quality

## Relevant Quotes

### From Game README
> "The game concept is based off the popular '*The Sims*' folklore of a **Painting Goblin**."

> "The Painting Goblin will be a game created in the Processing environment and language. It will be a short game and a technical exercise in utility based game AI."

### From Task System README
> "painting-goblin 是一個基於檔案系統的任務處理系統，使用 Publisher-Subscriber 模式來管理任務佇列。系統會監控任務目錄，自動將任務從待處理狀態移動到處理中狀態，並執行任務處理。"

### From Online Articles
> "A few years ago, a 4Chan post by an anon poster went low-key viral when they revealed they'd started every sims family with a 'painting goblin', a green skinned man confined to the basement..." - Pedestrian.tv

> "With my decadent opulence gone, I concentrated my wishes into my Sims. They were happy, and the painting goblin let them live free of the financial woes..." - The Cut

## Source URLs

### Meme Sources
- https://imgur.com/gallery/NrJku9x (Original meme image)
- https://www.reddit.com/r/thesims/comments/1zela3/painting_goblin_xpost_from_r4chan/
- https://knowyourmeme.com/photos/1002565-the-sims
- https://www.thecut.com/article/i-think-about-my-painting-goblin-in-the-sims-a-lot.html
- https://www.pedestrian.tv/tech-gaming/take-inspo-from-some-of-the-weirdest-shit-people-have-done-in-the-sims/

### Game Project Sources
- https://github.com/gozu66/ThePaintingGoblin
- https://raw.githubusercontent.com/gozu66/ThePaintingGoblin/master/README.md
- https://api.github.com/repos/gozu66/ThePaintingGoblin/commits (API for commit dates)

### Task Processing System Sources
- https://github.com/fnaith/painting-goblin
- README.md and config.ini from local repository
- Git commit history: `git log --reverse --oneline`

## Conclusion

The Painting Goblin concept has evolved from a simple *The Sims* optimization strategy into both a game development project and a sophisticated task processing system. While sharing the same name and inspiration, each manifestation serves distinct purposes: cultural meme, AI game experiment, and AI task automation framework. This demonstrates how internet culture can inspire technical projects across different domains.
