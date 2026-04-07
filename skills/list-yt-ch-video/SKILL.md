---
name: list-yt-ch-video
description: List all videos from a YouTube channel using the list-yt-ch-video tool. Use when asked to query YouTube channel videos, list video metadata, download channel videos, or export video data to CSV.
---

# list-yt-ch-video Skill

This skill enables listing all videos from a YouTube channel and optionally downloading them using the `list-yt-ch-video` Python CLI tool.

## When to Use This Skill

- User requests listing videos from a YouTube channel
- User provides a YouTube channel ID or handle
- User wants to export video metadata (ID, title, duration) to CSV
- User needs to download all videos from a channel (optional)
- User wants to limit the number of videos fetched

## Prerequisites

- Python 3.7+ installed
- `yt-dlp` installed (automatically via `requirements.txt`)
- The `list-yt-ch-video` tool located at `$PAINTING_GOBLIN_DIR/tools/list-yt-ch-video/`

## Installation

If the tool is not yet installed, run:

```bash
cd $PAINTING_GOBLIN_DIR/tools/list-yt-ch-video
pip install -r requirements.txt
```

## Usage

### Basic Command

```bash
python $PAINTING_GOBLIN_DIR/tools/list-yt-ch-video/list-yt-ch-video.py <CHANNEL_ID> <OUTPUT_DIR>
```

### Arguments

- `CHANNEL_ID`: The YouTube channel ID or handle (e.g., `@TsunomakiWatame` or `UC...`)
- `OUTPUT_DIR`: Directory where the CSV file and downloaded videos will be saved

### Options

- `--limit N`: Limit number of videos to fetch (default: all)
- `--no-download`: Skip downloading videos (only generate CSV)

### Example

To list the first 5 videos from the channel `@TsunomakiWatame` and save CSV to `~/channel_data`:

```bash
python $PAINTING_GOBLIN_DIR/tools/list-yt-ch-video/list-yt-ch-video.py @TsunomakiWatame ~/channel_data --limit 5 --no-download
```

To list all videos and download them:

```bash
python $PAINTING_GOBLIN_DIR/tools/list-yt-ch-video/list-yt-ch-video.py @TsunomakiWatame ~/channel_data
```

## Features

- Fetches video list from channel using yt-dlp
- Exports video ID, title, and duration to CSV (filename = channel ID)
- Optionally downloads each video with best quality video and audio
- Supports channel handles (`@...`) and channel IDs (`UC...`)
- Gracefully handles errors (invalid channel, network issues, etc.)

## Troubleshooting

- **yt-dlp not found**: Install with `pip install yt-dlp`
- **Output directory does not exist**: The tool will create it automatically
- **Channel not found**: Verify the channel ID/handle is correct
- **Permission errors**: Ensure write access to the output directory
- **Download failures**: Check network connectivity and video availability

## Notes

- The CSV file is saved as `<CHANNEL_ID>.csv` in the output directory.
- Downloaded videos are saved as `<video title>.mp4` in the output directory.
- The tool uses `--flat-playlist` to retrieve all videos from the channel.
- Downloaded videos are merged into MP4 format with best video+audio streams.
