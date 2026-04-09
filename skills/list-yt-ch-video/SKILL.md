---
name: list-yt-ch-video
description: Tool for listing all videos from a YouTube channel with video id, name, and duration. Use when asked to query video data from a YouTube channel, generate CSV reports, or analyze channel content.
---

# List YouTube Channel Videos

This skill provides a Python CLI tool to fetch all videos from a YouTube channel and export them as a CSV file.

## When to Use This Skill

- User asks to list all videos from a YouTube channel
- User needs a CSV report of channel videos with metadata
- User wants to analyze channel content, video durations, or titles
- User needs to get video IDs for further processing (e.g., downloading)

## Prerequisites

- Python 3.7+
- yt-dlp library (installed via requirements.txt in tool directory)

## Tool Location

The tool is located at `$PAINTING_GOBLIN_DIR/tools/list-yt-ch-video/list-yt-ch-video.py`.

## Usage

```bash
python $PAINTING_GOBLIN_DIR/tools/list-yt-ch-video/list-yt-ch-video.py <CHANNEL_ID> <OUTPUT_DIR>
```

### Arguments

- `CHANNEL_ID`: YouTube channel identifier. Can be:
  - Handle starting with `@` (e.g., `@TsunomakiWatame`)
  - Channel ID starting with `UC` (e.g., `UCqm3BQLlJfvkTsX_hvm0UmA`)
  - Custom handle without `@` (e.g., `TsunomakiWatame`)
  - Full YouTube channel/videos URL (e.g., `https://www.youtube.com/@TsunomakiWatame/videos`)
- `OUTPUT_DIR`: Directory where CSV file will be saved. The tool creates the directory if it doesn't exist.

### Output

- A CSV file named `<CHANNEL_ID>.csv` (with invalid characters replaced by underscores) in the output directory.
- Columns: `video id`, `video name`, `video duration` (seconds).

## Examples

```bash
# Using channel handle
python tools/list-yt-ch-video/list-yt-ch-video.py "@TsunomakiWatame" ./output

# Using channel ID
python tools/list-yt-ch-video/list-yt-ch-video.py "UCqm3BQLlJfvkTsX_hvm0UmA" ./reports

# Using custom handle (no @)
python tools/list-yt-ch-video/list-yt-ch-video.py "TsunomakiWatame" ./data
```

## Troubleshooting

- **No videos found**: Ensure the channel identifier is correct and the channel has public videos.
- **Network errors**: Check internet connectivity and YouTube access.
- **Permission errors**: Ensure output directory is writable.
- **Missing yt-dlp**: Install with `pip install -r tools/list-yt-ch-video/requirements.txt`.

## Implementation Details

The tool uses `yt-dlp` with `extract_flat` mode to efficiently retrieve video metadata without downloading. It fetches the channel's `/videos` playlist, which includes all uploaded videos.

## Related Skills

- `dl-yt-video`: Download individual YouTube videos.
- `build-python-cli-tool`: Create new Python CLI tools.
