---
name: video-to-text
description: Extract speech text from video files using Whisper speech recognition. Use when asked to transcribe video, extract subtitles, convert video to text, or generate transcript from video. Supports multiple languages and model sizes.
---

# Video to Text Skill

This skill provides a tool for extracting speech text from video files using OpenAI's Whisper model.

## When to Use This Skill

- User asks to "extract text from video", "transcribe video", "video to text"
- User wants to generate subtitles or transcripts from video content
- User needs to convert speech in video to written text
- User wants to analyze spoken content in videos

## Prerequisites

- Python 3.8+ with pip
- FFmpeg installed and available in PATH (required for audio extraction)
- OpenAI Whisper package (installed automatically via requirements.txt)

## Tool Location

The Python script is located at `$AGENT_CWD/tools/video-to-text/video-to-text.py`.

## Usage

### Basic Command

```bash
python tools/video-to-text/video-to-text.py <VIDEO_PATH> <OUTPUT_DIR>
```

### Arguments

- `VIDEO_PATH`: Path to the input video file
- `OUTPUT_DIR`: Directory where the text file will be saved (created if doesn't exist)

### Optional Arguments

- `--model`: Whisper model size (`tiny`, `base`, `small`, `medium`, `large`). Default: `base`
- `--language`: Language code (e.g., `en`, `ja`). If not specified, Whisper auto-detects.
- `--task`: `transcribe` (default) or `translate` (translate to English)

### Examples

1. Extract text from a video with default settings:
   ```bash
   python tools/video-to-text/video-to-text.py "input.mp4" "output/"
   ```

2. Use a larger model for better accuracy:
   ```bash
   python tools/video-to-text/video-to-text.py "input.mp4" "output/" --model large
   ```

3. Specify language (Japanese):
   ```bash
   python tools/video-to-text/video-to-text.py "input.mp4" "output/" --language ja
   ```

4. Translate non-English speech to English:
   ```bash
   python tools/video-to-text/video-to-text.py "input.mp4" "output/" --task translate
   ```

## Output

The tool creates a text file in the output directory with the same name as the input video (e.g., `input.txt`). The file contains the transcribed text in UTF-8 encoding.

## Troubleshooting

### FFmpeg not found
- Ensure FFmpeg is installed and accessible in PATH
- On Windows, download from https://ffmpeg.org/download.html

### Whisper model download fails
- Check internet connection
- The tool downloads models on first use (cached locally)

### No speech detected
- The video may not contain clear speech
- Try using a larger model (`--model large`)
- Ensure audio track is present

### Performance issues
- Smaller models (`tiny`, `base`) are faster but less accurate
- Larger models require more memory and time
- Consider using GPU for faster processing (requires CUDA)

## Dependencies

See `$AGENT_CWD/tools/video-to-text/requirements.txt` for Python dependencies.
