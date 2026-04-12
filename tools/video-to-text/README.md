# Video to Text Tool

Extracts speech text from video files with timestamps using OpenAI Whisper.

## Installation

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Ensure `ffmpeg` is installed and available in your PATH.

## Usage

```bash
python video-to-text.py <VIDEO_PATH> <OUTPUT_DIR>
```

Example:

```bash
python video-to-text.py "my_video.mp4" "./transcripts"
```

The output file will be named after the video file (e.g., `my_video.txt`) and placed in the output directory.

## Output Format

Each line contains a timestamp in `HH:mm:ss` format followed by the transcribed text:

```
[00:00:00] Hello world
[00:00:02] This is a test
```

## Features

- Automatically creates output directory if missing
- Handles Unicode file paths (via short path conversion on Windows)
- Uses Whisper base model for transcription
- Extracts audio using ffmpeg (mono, 16kHz WAV)
- Graceful error handling and progress feedback

## Requirements

- Python 3.8+
- ffmpeg
- Internet connection (for downloading Whisper model on first run)

## License

Part of the Painting Goblin project.
