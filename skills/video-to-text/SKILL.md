---
name: video-to-text
description: Tool for extracting speech text from video with timestamps. Use when asked to transcribe video, extract subtitles, generate transcript from video, or convert video speech to text.
---

# Video to Text

Extracts speech text from video files using OpenAI Whisper and outputs a transcript with timestamps.

## When to Use This Skill

- You need to extract spoken words from a video file
- You want a timestamped transcript for subtitles or analysis
- You need to convert video speech to text for further processing
- You have a video file and want to generate a text transcript

## Prerequisites

- Python 3.8+
- ffmpeg installed and available in PATH
- Internet connection (for downloading Whisper models on first run)

## Usage

The tool is located at `tools/video-to-text/video-to-text.py`.

### Command Line Arguments

```bash
python video-to-text.py <VIDEO_PATH> <OUTPUT_DIR>
```

- `VIDEO_PATH`: Path to the input video file (supports most formats)
- `OUTPUT_DIR`: Directory where the transcript text file will be saved

### Example

```bash
python tools/video-to-text/video-to-text.py "path/to/video.mp4" "output/folder"
```

The output file will be named after the video file (e.g., `video.txt`) and placed in the output directory.

## Features

- Automatically creates output directory if it doesn't exist
- Extracts audio from video using ffmpeg (mono, 16kHz WAV)
- Transcribes using OpenAI Whisper (base model by default)
- Outputs timestamps in `HH:mm:ss` format
- Handles various video formats supported by ffmpeg
- Clean error messages and progress indicators

## Output Format

Each line in the output text file has the format:

```
[HH:mm:ss] Transcribed text here
```

Example:
```
[00:00:00] Hello world
[00:00:02] This is a test
```

## Troubleshooting

### Unicode Path Issues on Windows

If the video file path contains non-ASCII characters (e.g., Japanese, Chinese), you may encounter encoding issues on Windows command prompt. Consider:

1. Renaming the file to use ASCII characters
2. Using short paths (8.3 format)
3. Running from PowerShell or WSL

### ffmpeg Not Found

Ensure ffmpeg is installed and available in your PATH. You can test with:

```bash
ffmpeg -version
```

### Whisper Model Download Failures

The first run downloads the Whisper model (base, ~150MB). Ensure you have internet connectivity and sufficient disk space.

### Performance

Transcription speed depends on video length and CPU. For long videos, consider using a smaller model (edit script to use "tiny" or "small").

## Customization

You can modify the script to use different Whisper models by changing the line:

```python
model = whisper.load_model("base")  # Change to "tiny", "small", "medium", "large"
```

## References

- [OpenAI Whisper](https://github.com/openai/whisper)
- [FFmpeg](https://ffmpeg.org/)
- [MoviePy](https://zulko.github.io/moviepy/)
