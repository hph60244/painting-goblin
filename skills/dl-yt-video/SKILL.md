---
name: dl-yt-video
description: Download YouTube videos with best quality video and audio using the dl-yt-video tool. Use when asked to download YouTube video, fetch video by ID, save video as mp4, or get high quality video from YouTube.
---

# dl-yt-video Skill

This skill enables downloading YouTube videos with best quality video and audio using the `dl-yt-video` Python CLI tool.

## When to Use This Skill

- User requests downloading a YouTube video
- User provides a YouTube video ID or URL
- User wants to save video in MP4 format with best quality
- User needs to download a video to a specific directory
- User wants to automatically create output directory if missing

## Prerequisites

- Python 3.7+ installed
- `yt-dlp` installed (automatically via `requirements.txt`)
- `ffmpeg` installed (for merging video and audio streams)
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

- `VIDEO_ID`: The YouTube video ID (e.g., `d3UTywBDSW4`) from the video URL `https://www.youtube.com/watch?v=VIDEO_ID`
- `OUTPUT_DIR`: Directory where the downloaded video will be saved

### Example

To download the video with ID `d3UTywBDSW4` and save it to `~/videos`:

```bash
python $PAINTING_GOBLIN_DIR/tools/dl-yt-video/dl-yt-video.py d3UTywBDSW4 ~/videos
```

## Features

- Downloads best quality video and audio streams available
- Automatically merges streams into MP4 format
- Creates output directory if it doesn't exist
- Output filename is based on video title (sanitized for filesystem)
- Handles Unicode characters in video titles (encoding safe)
- Graceful error handling (invalid video ID, network issues, etc.)

## Troubleshooting

- **yt-dlp not found**: Install with `pip install yt-dlp`
- **ffmpeg not found**: Install ffmpeg from https://ffmpeg.org/ (required for merging)
- **Output directory cannot be created**: Check permissions
- **Video not found**: Verify the video ID is correct and the video is publicly accessible
- **Encoding errors**: The tool uses safe printing to avoid Unicode encoding issues on Windows
- **JavaScript runtime warning**: yt-dlp may warn about missing JavaScript runtime; the tool will still work but some formats may be missing. Install Node.js or Deno to suppress warning.

## Notes

- Downloaded videos are saved as `<sanitized title>.mp4` in the output directory.
- The tool uses `bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best` format selection.
- If the video title contains characters invalid for filesystems, they are replaced with underscores.
- The tool first extracts video metadata to get the title, then downloads with sanitized filename.
- For testing, video ID `d3UTywBDSW4` can be used (a public YouTube video).
