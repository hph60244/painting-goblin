# Hololive 粉絲剪輯語音/SE 下載點 — 綜合研究報告

**日期:** 2026-05-24

---

## 一、Voice Button 網站（在線播放型）

這類網站以按鈕形式排列語音，點擊即可播放 Hololive 成員的剪輯語音。

### 單一成員專用站

| 成員 | 網站 | 說明 |
|------|------|------|
| 大神ミオ | https://ookamimio.org/ | 專屬聲音按鈕板 |
| 姫森ルーナ | https://nanora.moe/ | Vue.js 構建，開源 (MIT) |
| 天音かなた | https://vbup-osc.github.io/kanata-button/ | 多分類完整按鈕站 |
| さくらみこ | https://harutoblog.com/voiceCollection/hololive/sakura-miko/index.html | 分類包含新語音、問候、反應等 |
| IRyS | https://irysoundboard.com/ | EN 組專屬 |

### 多成員聚合站（支援下載）

| 網站 | URL | 特色 |
|------|-----|------|
| Myinstants | https://www.myinstants.com/en/search/?name=Hololive | 使用者上傳，播放+MP3 下載 |
| 101Soundboards | https://www.101soundboards.com/boards/148651-hololive-soundboard | 支援 TTS，MP3 下載 |
| Voicy | https://www.voicy.network/search/hololive-sound-effects | 58+ 音效，MP3 下載，Discord/TG Bot 整合 |
| SoundInstants | https://soundinstants.com/search/Hololive | MP3 下載，可用於影片製作 |

### 目錄聚合站

| 網站 | URL | 說明 |
|------|-----|------|
| VBUP Collection | https://vbup-osc.github.io/vtuber-voice-button-collection/ | 所有 Vtuber 聲音按鈕的索引目錄 |

---

## 二、完整語音包/音檔下載站

### Nyaa.si（Torrent）
- **URL:** https://nyaa.si/?f=0&c=2_0&q=hololive+voice
- **內容:** 官方語音包（季節、生日、ASMR、系統語音等）的粉絲分流
- **格式:** FLAC（無損）/ MP3
- **大小:** 數 MiB ~ 76+ GiB 大合集
- **範圍:** Hololive JP, EN, ID 全部成員
- **需要:** BitTorrent 客戶端

### Ragtag Archive（串流備份）
- **URL:** https://archive.ragtag.moe/about
- **內容:** Hololive 公開直播完整錄影備份
- **品質:** YouTube 最高畫質（含音軌）
- **開源:** 可自架實例

### Internet Archive
- **URL:** https://archive.org/details/hololive-unarchived
- **內容:** 未存檔/會員限定的直播重傳
- **格式:** 各種格式（上傳者決定）

### Piapro（官方伴奏）
- **URL:** https://piapro.jp/hololive
- **內容:** 317+ 首 Hololive 原創曲官方伴奏/卡拉 OK 版
- **授權:** 官方帳號，可在二創準則下使用

---

## 三、工具與開源專案

### 聲音按鈕建站模板

| 專案 | URL | 星數 | 說明 |
|------|-----|------|------|
| material-vtuber-button | https://github.com/lonelyion/material-vtuber-button | 79 | Vue+NuxtJS+Vuetify 模板，易部署 |
| sound-buttons | https://github.com/sound-buttons/sound-buttons | 13 | 完整平台含 YouTube 剪輯提交功能 |
| luna-button | https://github.com/monoai/luna-button | 10 | MIT 開源，Himemori Luna 專用 |

### vbup-osc 組織（Hololive 聲音按鈕系列）
- **GitHub:** https://github.com/vbup-osc
- 包含 Subaru、Ayame、Miko、Mio 等成員按鈕
- 均採用 Vue.js 構建

### AI 語音工具

| 工具 | URL | 功能 |
|------|-----|------|
| Hololive RVC Models | https://huggingface.co/spaces/megaaziib/hololive-rvc-models-v2 | AI 聲音轉換（上傳音檔 → 轉為 Hololive 成員聲線） |
| hololive-style-bert-vits2 | https://replicate.com/zsxkib/hololive-style-bert-vits2 | AI 文字轉語音（Hololive 風格 TTS） |
| VoiceDub.ai | https://voicedub.ai/create/hololive-model-collection | AI 翻唱/聲音轉換 |

### 官方音效包
- **hololive Noises!:** https://shop.hololivepro.com/en/products/hololive_noises
- 系統音效、通知音、鬧鐘音，供個人使用

### Minecraft 音效包
- **Hololive JP Sounds Pack:** https://www.curseforge.com/minecraft/texture-packs/hololive-jp-sounds-pack
- 150+ 個 Hololive JP 聲音，6,400+ 下載

### 其他相關工具
- **Holodex:** https://holodex.net — 多視窗直播入口/剪輯搜尋
- **HLClips:** https://hlclips.com — 2 萬+ 英文字幕剪輯存檔
- **Hololive 非公式 Wiki:** https://seesaawiki.jp/hololivetv/ — 語音包目錄（日文）

---

## 四、重點總結

### 如果你想要...
- **即點即聽語音按鈕:** 使用 VBUP Collection 目錄找到喜愛成員的專屬站
- **下載完整官方語音包（無損）:** Nyaa.si 搜尋 "hololive voice"（需 BT 客戶端）
- **短語音/SE 素材:** Myinstants、101Soundboards、Voicy 可直接下載 MP3
- **直播備份音檔:** Ragtag Archive 或 Internet Archive
- **官方伴奏音樂:** Piapro（hololive 官方帳號）
- **AI 語音合成/轉換:** Hugging Face RVC Models 或 Replicate BERT-VITS2
- **自己建按鈕站:** material-vtuber-button 開源模板（最快上手）
- **Hololive 相關開源專案探索:** GitHub 上 vbup-osc 組織

### 注意事項
- 大多數粉絲站引用 Hololive 二創準則（https://www.hololive.tv/terms）
- 非官方站點上的語音素材版權歸 Cover Corp 所有
- Nyaa.si 上的語音包為官方付費內容的粉絲分流，使用時請注意當地法規
