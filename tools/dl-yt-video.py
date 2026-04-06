#!/usr/bin/env python3
"""
Download YouTube video with highest quality in MP4 format.
"""

import argparse
import os
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Download YouTube video by video ID"
    )
    parser.add_argument(
        "video_id",
        help="YouTube video ID (from URL)"
    )
    parser.add_argument(
        "output_dir",
        help="Directory where downloaded video will be saved"
    )
    args = parser.parse_args()

    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Construct YouTube URL
    url = f"https://www.youtube.com/watch?v={args.video_id}"

    # yt-dlp command arguments
    # -f: format selection: best MP4, fallback to best any format
    # -o: output template, place in output_dir with video title and extension
    output_template = os.path.join(args.output_dir, '%(title)s.%(ext)s')
    cmd = [
        'yt-dlp',
        '-f', 'best[ext=mp4]/best',
        '-o', output_template,
        url
    ]

    print(f"Downloading video: {args.video_id}")
    print(f"Output directory: {args.output_dir}")
    try:
        # Run yt-dlp
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        # Print yt-dlp output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        print("Download completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Download failed with exit code {e.returncode}", file=sys.stderr)
        if e.stdout:
            print(e.stdout, file=sys.stderr)
        if e.stderr:
            print(e.stderr, file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: yt-dlp not found. Please install yt-dlp.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
