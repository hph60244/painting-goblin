# Hololive Voice / Sound Effect Tools & Collections — Research Findings

**Date:** 2026-05-24
**Scope:** GitHub, BOOTH, fan projects, official products, and open-source VTuber voice button projects.

---

## 1. "Holo-OTTO" / Voice Synthesis Tools

No project named "holo-otto" or "hololive otto" was found. The search instead surfaced:

### OTTO (unrelated — audio hardware)
- **URL:** https://github.com/bitfieldaudio/OTTO
- **Description:** An open-source digital hardware synth, groovebox, and FX processor. *Not Hololive-related.*
- **Verdict:** The name collision is coincidental. Not relevant.

### Hololive RVC Models (AI Voice Conversion)
- **URL:** https://huggingface.co/spaces/megaaziib/hololive-rvc-models-v2
- **Description:** A Hugging Face Space that provides RVC (Retrieval-based Voice Conversion) models for many Hololive members. Users can upload audio, use a YouTube link, or generate TTS, then apply voice conversion.
- **Members covered:** Multiple Hololive generations (exact list varies by model version).

### VoiceDub.ai — Hololive Model Collection
- **URL:** https://voicedub.ai/create/hololive-model-collection
- **Description:** AI-powered voice conversion service that supports a Hololive model collection for making AI covers. Insert a song link or record vocals, and the tool transforms the voice.

### hololive-style-bert-vits2
- **URL:** https://replicate.com/zsxkib/hololive-style-bert-vits2
- **Description:** Open-source text-to-speech model fine-tuned on Hololive voices, accessible via Replicate API. Uses BERT-VITS2 architecture.

---

## 2. Hololive Sound Effect Collections on BOOTH

### hololive production official BOOTH shop
- **URL:** https://hololive.booth.pm
- **Status:** The official shop has ceased handling new products. Existing listings were mostly retired as of August 2024.
- **Details:** Previously sold voice packs, digital goods, and merchandise. Now effectively inactive for new purchases.

### Official Shop — hololive Noises! Voice Pack
- **URL:** https://shop.hololivepro.com/en/products/hololive_noises
- **Description:** Official voice pack containing system sounds, notification sounds, and alarm sounds from Hololive talents. Licensed for personal use.
- **Members covered:** Wide range across Hololive JP, ID, EN branches.

---

## 3. Hololive Voice Packs on GitHub & Other Platforms

### vbup-osc / vtuber-voice-button-collection
- **URL:** https://github.com/vbup-osc/vtuber-voice-button-collection
- **Stars:** 13
- **Description:** A collection of VTuber voice buttons hosted as a static HTML page. Serves as an index/aggregator for individual member voice buttons.
- **License:** GPL-3.0
- **Members covered:** Aggregate of many Hololive members.

### monoai / luna-button
- **URL:** https://github.com/monoai/luna-button
- **Stars:** 10
- **Description:** Voice button board dedicated to Himemori Luna (Hololive 4th Gen). Built with Vue + jQuery + Bootstrap 3. Live at https://nanora.moe
- **License:** MIT (program), audio per Hololive secondary creation guidelines.
- **Members covered:** Himemori Luna.

### YukihanaLamy / lamy-button
- **URL:** https://github.com/YukihanaLamy/lamy-button
- **Stars:** 1
- **Description:** Voice button for Yukihana Lamy (Hololive 5th Gen). Built with Vue. Live at https://lamy.moe
- **Members covered:** Yukihana Lamy.

### vtb-top / Hololive-JP-Sounds-Pack (Minecraft)
- **URL:** https://www.curseforge.com/minecraft/texture-packs/hololive-jp-sounds-pack
- **Description:** Minecraft resource pack that adds 150+ Hololive JP sounds captured from streams and songs. Over 6.4K+ downloads.
- **Members covered:** Hololive JP members.

### VTuber Lossless Voice Packs (Nyaa)
- **URL:** https://nyaa.land/view/1838239
- **Description:** Large lossless voice pack collection (76.1 GiB) covering Hololive, Neo-Porte, Nijisanji, and other VTuber groups. Uploaded June 2024. **Note:** Copyright status is unclear.

---

## 4. Sound Effect Packs for Game Development

### Official: hololive Noises! (shop.hololivepro.com)
- **URL:** https://shop.hololivepro.com/en/products/hololive_noises
- **Description:** The only official Hololive sound effect pack. System/notification sounds usable for personal projects. Not licensed for commercial game development without review of terms.

### Community SFX Sources (not official packs):
- **Myinstants** — https://www.myinstants.com/en/search/?name=Hololive (individual sound buttons)
- **101Soundboards** — https://www.101soundboards.com/boards/148651-hololive-soundboard (ringtones/SFX downloads)
- **Voicy** — https://www.voicy.network/search/hololive-sound-effects (58 unique Hololive sounds, mp3 download)
- **SoundInstants** — https://soundinstants.com/search/Hololive
- **SoundButtons** — https://soundbuttons.net/hololive

**Note:** These community sites host fan-uploaded clips. They are not official packs and copyright status varies. Not recommended for commercial game development without permission.

---

## 5. VTuber Voice Button GitHub Projects (Open Source)

### material-vtuber-button (Template — Most Popular)
- **URL:** https://github.com/lonelyion/material-vtuber-button
- **Stars:** 79
- **Description:** A template for quickly creating a Material Design-style VTuber voice button website. Built with Vue + NuxtJS + Vuetify. Supports i18n (multi-language), YAML config, and easy deployment to Vercel/GitHub Pages.
- **License:** MIT
- **Status:** Archived (read-only as of March 2025), but still functional as a template.

### sound-buttons / sound-buttons (Full-Featured)
- **URL:** https://github.com/sound-buttons/sound-buttons
- **Stars:** 13
- **Description:** Complete VTuber voice button website with online audio submission system. Users can clip YouTube audio via a form to generate buttons. Angular2 frontend, Azure Functions backend, Azure Blob Storage for audio files. Data-separated architecture (JSON configs).
- **License:** AGPL-3.0
- **Live site:** https://sound-buttons.click

### vbup-osc org repos (Hololive-specific):
| Repo | Stars | Member | Tech |
|------|-------|--------|------|
| subaru-button | 15 | Oozora Subaru | Vue |
| ayame-button | 15 | Nakiri Ayame | Vue |
| miko-button | 15 | Sakura Miko | Vue |
| mio-button | 12 | Ookami Mio | Vue |

### Other member-specific buttons:
| Repo | Stars | Member | Tech |
|------|-------|--------|------|
| hiiro-button | 71 | Hiiro (not Hololive) | Vue |
| shiori-button | 6 | Shiori Novella (Hololive EN) | JavaScript |
| ciyana-button | 5 | Ciyana (not Hololive) | Vue |
| Kyouka-button | 5 | Kyouka (not Hololive) | Vue |

### Related Tools:
- **Holodex** — https://github.com/HolodexNet/Holodex (multi-platform VTuber content viewer/archiver)
- **LiveTL** — https://github.com/LiveTL/LiveTL (multilingual live translation overlay for VTuber streams)
- **pekofy-bot** — https://github.com/Peko/pekofy-bot (adds "peko" to text, meme bot)
- **holo-schedule** — https://github.com/saza-ku/holo-schedule (Hololive streaming schedule viewer)

---

## Summary

| Category | Best Option | URL |
|----------|-------------|-----|
| **Voice Button Template** | material-vtuber-button (79 stars, easy setup) | https://github.com/lonelyion/material-vtuber-button |
| **Full Voice Button Platform** | sound-buttons (with YouTube clip submission) | https://github.com/sound-buttons/sound-buttons |
| **Official Sound Pack** | hololive Noises! | https://shop.hololivepro.com/en/products/hololive_noises |
| **AI Voice Conversion** | Hololive RVC Models (Hugging Face) | https://huggingface.co/spaces/megaaziib/hololive-rvc-models-v2 |
| **AI TTS** | hololive-style-bert-vits2 (Replicate) | https://replicate.com/zsxkib/hololive-style-bert-vits2 |
| **Minecraft SFX Pack** | Hololive JP Sounds Pack (6.4K+ downloads) | https://www.curseforge.com/minecraft/texture-packs/hololive-jp-sounds-pack |
| **Individual Member Buttons** | vbup-osc org repos (Subaru, Ayame, Miko, Mio) | https://github.com/vbup-osc |
| **Voice Collection Index** | vtuber-voice-button-collection | https://github.com/vbup-osc/vtuber-voice-button-collection |
| **Official BOOTH Shop** | hololive.booth.pm (mostly retired) | https://hololive.booth.pm |
