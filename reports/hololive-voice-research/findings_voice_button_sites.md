# Hololive Voice Button Sites - Research Findings

## Overview

Voice button (soundboard) sites for Hololive VTubers are fan-made websites that collect and organize voice clips from stream archives. Users click buttons to play short audio clips. These sites are typically built as static SPAs (Vue.js, plain HTML/JS) and hosted on GitHub Pages or similar free hosting.

---

## 1. Individual Member Voice Button Sites

### Mio Button (Ookami Mio)
- **URL:** https://ookamimio.org/
- **Description:** Dedicated soundboard for Ookami Mio (Hololive JP Gen 3). Categorized voice clips.
- **Mechanics:** Click to play. Fan-made, not affiliated with Cover Corp.

### Luna Button (Himemori Luna)
- **URL:** https://nanora.moe/
- **Description:** Voice button board for Himemori Luna (Hololive JP Gen 4). Built with Vue.js + jQuery + Bootstrap 3.
- **Source:** https://github.com/monoai/luna-button (MIT license)
- **Members covered:** Himemori Luna only.
- **Mechanics:** Click buttons to play MP3 clips. Voice files follow naming pattern `CATEGORY_VOICENAME.mp3`. Volume-normalized to 80. Strong cache strategy; new voice files must have new filenames.

### Kanata Button (Amane Kanata)
- **URL:** https://vbup-osc.github.io/kanata-button/
- **Description:** Full-featured voice button site for Amane Kanata (Hololive JP Gen 4). Includes categories for "Tenshi", "Otome", "Mimicry", "Chinese", "Special", "Tenshi Mode", "Wholesome", and more.
- **Members covered:** Amane Kanata (includes "Tengoku Housoubu" - Heaven Academy Broadcasting Club theme).
- **Mechanics:** Click to play. Organized into sub-categories (萌, 模仿秀, 说中文, 特殊, 天哥, etc.). Has "About" page with STAFF credits.

### Miko Button (Sakura Miko)
- **URL:** https://harutoblog.com/voiceCollection/hololive/sakura-miko/index.html
- **Description:** Voice collection site for Sakura Miko (Hololive JP Gen 0/JP). Organized into categories: New, Greeting, Holomem, Reaction, Funny, Comfort (ASMR).
- **Members covered:** Sakura Miko (also references other Hololive members like Pekora in cross-clips).
- **Mechanics:** Click to play. Cites Hololive Secondary Creation License. Contact via Twitter (@hongo_haruto).

### IRySoundboard (IRyS)
- **URL:** https://irysoundboard.com/
- **Description:** Soundboard dedicated to IRyS (Hololive EN Project: Hope).
- **Members covered:** IRyS only.
- **Mechanics:** Click to play sound buttons.

### HololiveSoundboard (Matsuri & Ayame - GitHub Project)
- **URL:** https://github.com/Ky1286/HololiveSoundboard
- **Description:** Open-source soundboard project initially covering Natsuiro Matsuri and Nakiri Ayame (later adding Shirakami Fubuki).
- **Members covered:** Natsuiro Matsuri, Nakiri Ayame, Shirakami Fubuki.
- **Mechanics:** Click-to-play soundboard built as a static HTML/CSS/JS page. Not deployed as a live site (GitHub repo only).

---

## 2. Multi-Member / Aggregator Soundboard Sites

### Myinstants - Hololive Soundboard
- **URL:** https://www.myinstants.com/en/search/?name=Hololive
- **Description:** Large general-purpose instant sound button platform with a Hololive tag. User-submitted clips.
- **Members covered:** Gawr Gura, Usada Pekora, Houshou Marine, Uruha Rushia, Shirakami Fubuki, Inugami Korone, Minato Aqua, Sakura Miko, Kiryu Coco, Watson Amelia, Natsuiro Matsuri, Nakiri Ayame, Suisei, Tsunomaki Watame, and more.
- **Mechanics:** Click to play. Users can upload their own sounds. Web app with installable mobile version. Includes share functionality.

### 101Soundboards - Hololive Soundboard
- **URL:** https://www.101soundboards.com/boards/148651-hololive-soundboard
- **Description:** Dedicated Hololive soundboard page on a large soundboard directory. Also offers TTS (text-to-speech) for specific members.
- **Members covered:** Includes Vestia Zeta (Hololive ID), Houshou Marine, and others.
- **Mechanics:** Click to play MP3 clips. Download available (MP3 format). TTS feature to generate custom speech in member voices.

### Voicy - Hololive Sounds
- **URL:** https://www.voicy.network/search/hololive-sound-effects
- **Description:** Sound effect platform with ~58 Hololive-specific sounds. User-submitted content.
- **Members covered:** Gawr Gura, Usada Pekora, Sakura Miko, Houshou Marine, Inugami Korone, Uruha Rusha, Shirakami Fubuki, Ouro Kronii, and others.
- **Mechanics:** Click to play. Download as MP3. Supports integration with Discord bot, Telegram bot, Slack bot. Also offers soundboard maker tool.

### SoundInstants - Hololive Search
- **URL:** https://soundinstants.com/search/Hololive
- **Description:** General soundboard library with Hololive-tagged content.
- **Members covered:** Various Hololive members.
- **Mechanics:** Click to play. MP3 download available.

### SoundButtonsLab
- **URL:** https://soundbuttonslab.com/
- **Description:** General meme soundboard site. Has Hololive content via search.
- **Members covered:** Various (search-based).
- **Mechanics:** Click to play. Unblocked soundboard.

---

## 3. Directory / Collection Sites

### VBUP - VTuber Voice Button Collection
- **URL:** https://vbup-osc.github.io/vtuber-voice-button-collection/
- **Description:** A curated directory/collection of VTuber voice button sites. Organized by agency: Hololive, Nijisanji, ViViD, and Others. Maintained by the Voice Button United Project (VBUP-OSC).
- **Members covered:** Spans the entire Hololive roster (JP, EN, ID, DEV_IS) plus other agencies.
- **Mechanics:** Link directory only - aggregates URLs to individual voice button sites. Not a player itself. Claims no responsibility for linked content. Open-source on GitHub.

---

## 4. Common Patterns & Technical Details

### How They Work
1. **Click to play:** All sites use a simple button grid. Clicking/tapping a button plays an MP3 audio clip inline via HTML5 Audio or a JS library.
2. **No download (most):** Most individual member sites do not offer download - they are purely playback.
3. **Aggregator sites:** Myinstants, 101Soundboards, and Voicy typically allow both playback and MP3 download.
4. **Hosting:** Individual button sites commonly use GitHub Pages, free web hosting, or personal domains.
5. **Tech stacks:** Vue.js (luna-button), plain HTML/CSS/JS (HololiveSoundboard), or custom JS frameworks.

### Categorization
- Most sites organize clips by: Greetings, Reactions, Funny moments, Member interactions, ASMR/comfort, Meme clips, Special events.
- Some sites include TTS functionality (101Soundboards) where users can type text and hear it in a member's voice (AI-generated).

### Legal / Licensing
- Most sites cite the Hololive Secondary Creation License (https://www.hololive.tv/terms).
- Sites are explicitly marked as fan-made and not affiliated with Cover Corp.
- Contact info (Twitter, email) is typically provided for copyright removal requests.

### Notable GitHub Projects (Open Source)
1. **luna-button** (https://github.com/monoai/luna-button) - Vue.js, Himemori Luna. Based on the earlier "Aqua button" project. MIT license.
2. **HololiveSoundboard** (https://github.com/Ky1286/HololiveSoundboard) - HTML/CSS/JS, Matsuri/Ayame/Fubuki.
3. **kanata-button** (https://github.com/vbup-osc/kanata-button) - Part of VBUP-OSC. Amane Kanata.
4. **VBUP Collection** (https://github.com/vbup-osc/vtuber-voice-button-collection) - Directory of all VTuber voice button sites.

---

## 5. Key Sites Summary Table

| Site | Type | Members | Playback | Download | Open Source |
|------|------|---------|----------|----------|-------------|
| ookamimio.org | Single-member | Ookami Mio | Click | No | Unknown |
| nanora.moe | Single-member | Himemori Luna | Click | No | Yes (MIT) |
| vbup-osc.github.io/kanata-button | Single-member | Amane Kanata | Click | No | Yes (VBUP) |
| harutoblog.com/.../sakura-miko | Single-member | Sakura Miko | Click | No | No |
| irysoundboard.com | Single-member | IRyS | Click | No | Unknown |
| myinstants.com | Multi-member (aggregator) | Many Hololive | Click | No (web only) | No |
| 101soundboards.com | Multi-member (aggregator) | Many Hololive | Click + TTS | Yes (MP3) | No |
| voicy.network | Multi-member (aggregator) | ~58 sounds | Click | Yes (MP3) | No |
| vbup-osc.github.io/collection | Directory | All Hololive | Link only | N/A | Yes |
