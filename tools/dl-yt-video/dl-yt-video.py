#!/usr/bin/env python3
"""
Download YouTube video with best quality video and audio, output as MP4.
Usage: python dl-yt-video.py <VIDEO_ID> <OUTPUT_DIR>
"""

import sys
import os
import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description='Download YouTube video as MP4')
    parser.add_argument('video_id', help='YouTube video ID (e.g., d3UTywBDSW4)')
    parser.add_argument('output_dir', help='Directory where video will be saved')
    args = parser.parse_args()

    video_id = args.video_id
    output_dir = args.output_dir

    # Basic validation of video ID (YouTube IDs are typically 11 characters)
    if len(video_id) != 11:
        print(f"Warning: Video ID '{video_id}' is not the typical length (11 characters).", file=sys.stderr)
        # Continue anyway

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Build yt-dlp command
    # Use best video+audio, merge to mp4, restrict filenames to ASCII for compatibility
    cmd = [
        'yt-dlp',
        f'https://www.youtube.com/watch?v={video_id}',
        '--format', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        '--merge-output-format', 'mp4',
        '--output', os.path.join(output_dir, '%(title)s.%(ext)s'),
        '--restrict-filenames',
        '--no-playlist',
        '--no-warnings',
    ]

    print(f"Downloading video {video_id}...")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        print("Download completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Download failed with error code {e.returncode}", file=sys.stderr)
        if e.stdout:
            print(e.stdout, file=sys.stderr)
        if e.stderr:
            print(e.stderr, file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: yt-dlp not found. Please install yt-dlp (pip install yt-dlp)", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nDownload interrupted by user.", file=sys.stderr)
        sys.exit(130)

if __name__ == '__main__':
    main()
