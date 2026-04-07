---
name: dl-yt-video
description: Download YouTube videos using the dl-yt-video tool. Use when asked to download YouTube videos, fetch video by ID, or save YouTube content as MP4.
---

# dl-yt-video Skill

This skill enables downloading YouTube videos as MP4 files using the `dl-yt-video` Python CLI tool.

## When to Use This Skill

- User requests downloading a YouTube video
- User provides a YouTube video ID or URL
- User wants to save a video locally as MP4
- User needs the highest quality video and audio merged

## Prerequisites

- Python 3.7+ installed
- `yt-dlp` installed (automatically via `requirements.txt`)
- The `dl-yt-video` tool located at `$PAINTING_GOBLIN_DIR/tools/dl-yt-video/`

## Installation

If the tool is not yet installed, run:

```bash
cd $PAINTING_GOBLIN_DIR/tools/dl-yt-video
pip install -r requirements.txt
```

## Usage

### Basic Command

```bash
python $PAINTING_GOBLIN_DIR/tools/dl-yt-video/dl-yt-video.py <VIDEO_ID> <OUTPUT_DIR>
```

### Arguments

- `VIDEO_ID`: The YouTube video ID (the string after `v=` in the URL)
- `OUTPUT_DIR`: Directory where the downloaded MP4 file will be saved

### Example

To download the video with ID `d3UTywBDSW4` to the `~/Downloads` folder:

```bash
python $PAINTING_GOBLIN_DIR/tools/dl-yt-video/dl-yt-video.py d3UTywBDSW4 ~/Downloads
```

## Features

- Downloads the best available video and audio streams
- Merges them into a single MP4 file
- Sanitizes filenames (removes special characters)
- Provides progress feedback via yt-dlp
- Gracefully handles errors (invalid ID, network issues, etc.)

## Troubleshooting

- **yt-dlp not found**: Install with `pip install yt-dlp`
- **Output directory does not exist**: Ensure the directory exists before running
- **Video unavailable**: Check the video ID and your network connection
- **Permission errors**: Ensure write access to the output directory

## Notes

- The tool uses `--restrict-filenames` to avoid filesystem issues with special characters.
- The output filename is derived from the video title.
- The tool downloads only the single video, not playlists.
