---
name: dl_yt_video
description: Download YouTube videos by video ID with highest quality MP4 format. Use this skill when users need to download YouTube videos programmatically or via command line.
---

# YouTube Video Download Skill

This skill enables downloading YouTube videos using the `dl-yt-video.py` command-line tool. The tool downloads the highest quality MP4 version available.

## Quick Start

Download a YouTube video by its video ID:

```bash
python $PAINTING_GOBLIN_DIR/tools/dl-yt-video.py <VIDEO_ID> <OUTPUT_DIR>
```

Example:
```bash
python $PAINTING_GOBLIN_DIR/tools/dl-yt-video.py jNQXAC9IVRw ./videos
```

## Tool Usage

### Command Syntax
```bash
python dl-yt-video.py VIDEO_ID OUTPUT_DIR
```

### Arguments
- **VIDEO_ID**: The YouTube video ID (the `v` parameter in YouTube URLs)
- **OUTPUT_DIR**: Directory where the downloaded video will be saved

### Behavior
1. The tool downloads the best available MP4 format (single file with audio and video).
2. If no MP4 format exists, downloads the best available format (any extension).
3. Output filename is automatically derived from the video title.
4. The output directory is created if it does not exist.

### Examples

**Download a video to current directory:**
```bash
python dl-yt-video.py dQw4w9WgXcQ .
```

**Download a video to a specific folder:**
```bash
python dl-yt-video.py M7lc1UVf-VE /path/to/downloads
```

## How It Works

The tool uses `yt-dlp` internally with the following parameters:
- Format selection: `best[ext=mp4]/best` (prefers MP4, falls back to any format)
- Output template: `%(title)s.%(ext)s`
- No merging required (selects progressive streams when possible)

### Dependencies
- `yt-dlp` (installed via pip)
- Python 3.6+

### Installation
The tool is ready to use if `yt-dlp` is installed. To install missing dependencies:

```bash
pip install yt-dlp
```

## Troubleshooting

### Common Issues

**Error: "yt-dlp not found"**
- Install yt-dlp: `pip install yt-dlp`

**Error: "HTTP Error 403: Forbidden"**
- YouTube may have rate‑limited the IP; wait and retry later
- Consider using `--cookies` option (not yet implemented in this tool)

**Error: "Video unavailable"**
- The video may be private, deleted, or region‑restricted
- Verify the video ID is correct and the video is publicly accessible

**Warning: "No supported JavaScript runtime could be found"**
- YouTube's extraction may be limited; install a JS runtime (deno, node) for full format support
- This warning does not prevent download but may limit available formats

**Multiple files downloaded instead of a single MP4**
- The selected format might be video‑only or audio‑only; the tool currently does not merge streams
- Install `ffmpeg` and adjust the format string to `bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best` with `--merge-output-format mp4` if merging is required

### Debug Mode
To see detailed yt-dlp output, add `--verbose` flag (not currently implemented). You can modify the script to print stderr.

## Integration with Painting‑Goblin

This tool can be used as part of automated task processing. Example task file:

```markdown
Download YouTube video with ID jNQXAC9IVRw to ./downloads

- Usage: `python dl-yt-video.py jNQXAC9IVRw ./downloads`
- Expected output: `./downloads/Me at the zoo.mp4`
```

Place such a task in `$PAINTING_GOBLIN_DIR/tasks/todo/` for automatic processing.

## Advanced Customization

You can edit the format string in `$PAINTING_GOBLIN_DIR/tools/dl-yt-video.py` to change download behavior:

- **Higher quality (requires ffmpeg)**:
  ```python
  '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
  '--merge-output-format', 'mp4',
  ```

- **Audio‑only**:
  ```python
  '-f', 'bestaudio[ext=m4a]/bestaudio',
  ```

- **Specific resolution**:
  ```python
  '-f', 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]',
  ```

Remember to install `ffmpeg` for merging video and audio streams.

## Support

If the tool fails unexpectedly, check the following:
1. Internet connectivity
2. YouTube API changes (yt‑dlp is generally up‑to‑date)
3. Disk space and write permissions in the output directory
4. Python environment and yt‑dlp version

Report issues to the repository maintainer.
