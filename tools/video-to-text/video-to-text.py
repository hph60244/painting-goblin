#!/usr/bin/env python3
"""
Video Speech-to-Text Extractor
Extracts speech text from video files using OpenAI's Whisper.
"""

import argparse
import os
import sys
import warnings
import shutil
from pathlib import Path

def safe_print(text: str, file=sys.stdout):
    """Print text safely, handling encoding errors."""
    try:
        print(text, file=file)
    except UnicodeEncodeError:
        encoding = file.encoding if hasattr(file, 'encoding') else (sys.stdout.encoding or 'utf-8')
        encoded = text.encode(encoding, errors='replace').decode(encoding)
        print(encoded, file=file)

def main():
    parser = argparse.ArgumentParser(
        description='Extract speech text from video file using Whisper.'
    )
    parser.add_argument(
        'video_path',
        help='Path to the input video file'
    )
    parser.add_argument(
        'output_dir',
        help='Output directory for the extracted text file'
    )
    parser.add_argument(
        '--model',
        default='base',
        choices=['tiny', 'base', 'small', 'medium', 'large'],
        help='Whisper model size (default: base)'
    )
    parser.add_argument(
        '--language',
        default=None,
        help='Language code (e.g., en, ja). If not specified, Whisper will auto‑detect.'
    )
    parser.add_argument(
        '--task',
        default='transcribe',
        choices=['transcribe', 'translate'],
        help='Task: transcribe (default) or translate to English'
    )
    args = parser.parse_args()

    video_path = Path(args.video_path)
    output_dir = Path(args.output_dir)

    if not video_path.is_file():
        safe_print(f'Error: video file not found: {video_path}', file=sys.stderr)
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f'{video_path.stem}.txt'

    safe_print(f'Loading Whisper model "{args.model}"...')
    try:
        import whisper
    except ImportError:
        safe_print('Error: whisper module not installed.', file=sys.stderr)
        safe_print('Please install it: pip install openai-whisper', file=sys.stderr)
        sys.exit(1)

    try:
        model = whisper.load_model(args.model)
    except Exception as e:
        safe_print(f'Error loading Whisper model: {e}', file=sys.stderr)
        sys.exit(1)

    if not shutil.which('ffmpeg'):
        safe_print('Error: ffmpeg not found in PATH.', file=sys.stderr)
        safe_print('Please install ffmpeg and ensure it is accessible.', file=sys.stderr)
        sys.exit(1)

    safe_print(f'Loading audio from "{video_path.name}"...')
    try:
        audio = whisper.load_audio(str(video_path))
    except Exception as e:
        safe_print(f'Error loading audio: {e}', file=sys.stderr)
        safe_print('Ensure ffmpeg is installed and accessible.', file=sys.stderr)
        sys.exit(1)

    safe_print('Transcribing...')
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        result = model.transcribe(
            audio,
            language=args.language,
            task=args.task,
            fp16=False  # disable FP16 to avoid GPU‑related issues on CPU
        )

    text = result.get('text', '').strip()
    if not text:
        safe_print('Warning: No speech detected.', file=sys.stderr)

    try:
        output_file.write_text(text, encoding='utf-8')
        safe_print(f'Text saved to: {output_file}')
    except Exception as e:
        safe_print(f'Error writing output file: {e}', file=sys.stderr)
        sys.exit(1)

    safe_print('Done.')

if __name__ == '__main__':
    main()
