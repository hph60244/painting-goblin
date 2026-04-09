#!/usr/bin/env python3
"""
YouTube Video Downloader
Downloads the best quality video and audio from YouTube.
"""

import argparse
import os
import re
import sys
import yt_dlp

def safe_print(text: str, file=sys.stdout):
    """Print text safely, handling encoding errors."""
    try:
        print(text, file=file)
    except UnicodeEncodeError:
        # Replace non-encodable characters with '?'
        encoding = file.encoding if hasattr(file, 'encoding') else (sys.stdout.encoding or 'utf-8')
        encoded = text.encode(encoding, errors='replace').decode(encoding)
        print(encoded, file=file)

def sanitize_filename(filename: str) -> str:
    """
    Remove or replace characters that are invalid in filenames.
    """
    # Replace characters that are problematic in file systems
    # Windows: \ / : * ? " < > |
    # Unix: / and null
    # We'll also replace control characters and trim spaces
    filename = re.sub(r'[\\/*?:"<>|]', '_', filename)
    filename = re.sub(r'[\x00-\x1f\x7f]', '', filename)
    filename = filename.strip()
    # Limit length to avoid path length issues
    if len(filename) > 200:
        # Keep first 100 and last 50 chars with ellipsis
        filename = filename[:100] + '...' + filename[-50:]
    return filename

def download_video(video_id: str, output_dir: str):
    """
    Download YouTube video with given ID to output directory.
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    video_url = f'https://www.youtube.com/watch?v={video_id}'

    try:
        # First extract info to get video title
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:  # type: ignore
            info = ydl.extract_info(video_url, download=False)
            title = info.get('title')
            if not title:
                title = video_id
            sanitized_title = sanitize_filename(title)

        # yt-dlp options for download
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(output_dir, f'{sanitized_title}.%(ext)s'),
            'merge_output_format': 'mp4',
            'quiet': False,
            'no_warnings': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type: ignore
            safe_print(f'Downloading: {title}')
            safe_print(f'Video ID: {video_id}')
            ydl.download([video_url])
            safe_print('Download completed successfully.')
    except yt_dlp.DownloadError as e:  # type: ignore
        safe_print(f'Download error: {e}', file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        safe_print(f'Unexpected error: {e}', file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Download YouTube video with best quality video and audio.'
    )
    parser.add_argument(
        'video_id',
        help='YouTube video ID (e.g., d3UTywBDSW4)'
    )
    parser.add_argument(
        'output_dir',
        help='Output directory for downloaded video'
    )
    args = parser.parse_args()

    download_video(args.video_id, args.output_dir)

if __name__ == '__main__':
    main()
