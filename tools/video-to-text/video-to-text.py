#!/usr/bin/env python3
"""
Video Speech Text Extractor
Extracts speech text from video with timestamps.
"""

import argparse
import os
import sys
import subprocess
import whisper
import tempfile
from pathlib import Path

def get_short_path(path: str) -> str:
    """
    Convert a path to its short (8.3) form on Windows to avoid encoding issues.
    Returns the original path on non-Windows or if conversion fails.
    """
    if os.name != 'nt':
        return path

    try:
        import ctypes
        from ctypes import wintypes

        GetShortPathNameW = ctypes.windll.kernel32.GetShortPathNameW
        GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
        GetShortPathNameW.restype = wintypes.DWORD

        # Convert to absolute path first
        abs_path = os.path.abspath(path)

        # Buffer for short path
        buffer = ctypes.create_unicode_buffer(260)  # MAX_PATH
        result = GetShortPathNameW(abs_path, buffer, len(buffer))

        if result == 0 or result > len(buffer):
            return abs_path
        return buffer.value
    except:
        return path

def safe_print(text: str, file=sys.stdout):
    """Print text safely, handling encoding errors."""
    try:
        print(text, file=file)
    except UnicodeEncodeError:
        encoding = file.encoding if hasattr(file, 'encoding') else (sys.stdout.encoding or 'utf-8')
        encoded = text.encode(encoding, errors='replace').decode(encoding)
        print(encoded, file=file)

def check_ffmpeg():
    """Check if ffmpeg is available in PATH."""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, timeout=5)
        return True
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False

def extract_audio(video_path: str, audio_path: str):
    """Extract audio from video using ffmpeg."""
    # Check ffmpeg availability
    if not check_ffmpeg():
        safe_print("Error: ffmpeg not found in PATH. Please install ffmpeg and ensure it's available.", file=sys.stderr)
        sys.exit(1)

    safe_print(f"Extracting audio from {video_path}...")
    try:
        # Use ffmpeg to extract audio as mono WAV at 16kHz (whisper prefers 16kHz)
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-ac', '1',          # mono
            '-ar', '16000',      # sample rate 16kHz
            '-vn',               # no video
            '-f', 'wav',
            '-y',                # overwrite output
            audio_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=300)
        if result.returncode != 0:
            safe_print(f"ffmpeg error: {result.stderr}", file=sys.stderr)
            sys.exit(1)
    except subprocess.TimeoutExpired:
        safe_print("ffmpeg timed out after 5 minutes", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        safe_print(f"Error extracting audio: {e}", file=sys.stderr)
        sys.exit(1)

def transcribe_with_timestamps(audio_path: str):
    """Transcribe audio using whisper and return segments with timestamps."""
    safe_print("Loading whisper model...")
    try:
        model = whisper.load_model("base")  # small model for speed, can be changed
    except Exception as e:
        safe_print(f"Error loading whisper model: {e}", file=sys.stderr)
        sys.exit(1)

    safe_print("Transcribing audio...")
    try:
        result = model.transcribe(audio_path, verbose=False)
    except Exception as e:
        safe_print(f"Error transcribing audio: {e}", file=sys.stderr)
        sys.exit(1)

    return result.get("segments", [])

def format_timestamp(seconds: float) -> str:
    """Format seconds to HH:mm:ss."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def write_output(segments, output_path: str):
    """Write segments to output file with timestamps."""
    safe_print(f"Writing transcript to {output_path}...")
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            for seg in segments:
                start = format_timestamp(seg['start'])
                text = seg['text'].strip()
                f.write(f"[{start}] {text}\n")
    except Exception as e:
        safe_print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)

def extract_speech_text(video_path: str, output_dir: str):
    """
    Extract speech text from video and save to output directory.
    """
    # Convert to absolute path to avoid encoding issues
    video_path = os.path.abspath(video_path)
    # Convert to short path on Windows to handle Unicode characters
    video_path = get_short_path(video_path)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Generate output filename based on video filename
    video_name = Path(video_path).stem
    output_filename = f"{video_name}.txt"
    output_path = os.path.join(output_dir, output_filename)

    # Create temporary audio file
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        audio_path = tmp.name

    try:
        # Extract audio
        extract_audio(video_path, audio_path)

        # Transcribe
        segments = transcribe_with_timestamps(audio_path)

        if not segments:
            safe_print("No speech segments found.", file=sys.stderr)
            # Create empty output file
            open(output_path, 'w').close()
        else:
            # Write output
            write_output(segments, output_path)
            safe_print(f"Transcript saved to {output_path}")

    finally:
        # Clean up temporary audio file
        try:
            os.unlink(audio_path)
        except:
            pass

def main():
    parser = argparse.ArgumentParser(
        description='Extract speech text from video with timestamps.'
    )
    parser.add_argument(
        'video_path',
        help='Path to the input video file'
    )
    parser.add_argument(
        'output_dir',
        help='Output directory for the transcript text file'
    )
    args = parser.parse_args()

    extract_speech_text(args.video_path, args.output_dir)

if __name__ == '__main__':
    main()
