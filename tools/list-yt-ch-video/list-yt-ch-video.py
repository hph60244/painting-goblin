#!/usr/bin/env python3
"""
List all videos from a YouTube channel and optionally download them.
Usage: python list-yt-ch-video.py <CHANNEL_ID> <OUTPUT_DIR>
"""

import sys
import os
import subprocess
import argparse
import json
import csv
from pathlib import Path
from typing import Optional

def get_channel_url(channel_id: str) -> str:
    """Convert channel ID to YouTube URL."""
    # If channel_id starts with '@', it's a handle
    # If it starts with 'UC', it's a channel ID
    # yt-dlp can handle both formats directly
    return f"https://www.youtube.com/{channel_id}/videos"

def fetch_video_list(channel_id: str, limit: Optional[int] = None):
    """Use yt-dlp to fetch video metadata as JSON."""
    url = get_channel_url(channel_id)
    cmd = [
        'yt-dlp',
        '--flat-playlist',
        '-j',
        '--no-warnings',
    ]
    if limit is not None:
        cmd.extend(['--playlist-end', str(limit)])
    cmd.append(url)
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        videos = []
        for line in lines:
            if not line:
                continue
            try:
                data = json.loads(line)
                video_id = data.get('id')
                title = data.get('title')
                duration = data.get('duration')
                if video_id and title and duration is not None:
                    videos.append({
                        'id': video_id,
                        'title': title,
                        'duration': duration
                    })
            except json.JSONDecodeError:
                print(f"Warning: Failed to parse JSON line: {line[:100]}", file=sys.stderr)
        return videos
    except subprocess.CalledProcessError as e:
        print(f"Failed to fetch video list: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: yt-dlp not found. Please install yt-dlp (pip install yt-dlp)", file=sys.stderr)
        sys.exit(1)

def write_csv(videos, output_path: Path):
    """Write video list to CSV file."""
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['video id', 'video name', 'video duration'])
        writer.writeheader()
        for v in videos:
            writer.writerow({
                'video id': v['id'],
                'video name': v['title'],
                'video duration': v['duration']
            })

def download_video(video_id: str, output_dir: Path):
    """Download a single video with best quality video and audio."""
    cmd = [
        'yt-dlp',
        f'https://www.youtube.com/watch?v={video_id}',
        '--format', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        '--merge-output-format', 'mp4',
        '--output', str(output_dir / '%(title)s.%(ext)s'),
        '--restrict-filenames',
        '--no-playlist',
        '--no-warnings',
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Downloaded video {video_id}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to download video {video_id}: {e.stderr}", file=sys.stderr)
        # Continue with other videos

def main():
    parser = argparse.ArgumentParser(description='List all videos from a YouTube channel and download them.')
    parser.add_argument('channel_id', help='YouTube channel ID or handle (e.g., @TsunomakiWatame or UC...)')
    parser.add_argument('output_dir', help='Directory where CSV and videos will be saved')
    parser.add_argument('--limit', type=int, help='Limit number of videos to fetch')
    parser.add_argument('--no-download', action='store_true', help='Skip downloading videos')
    args = parser.parse_args()

    channel_id = args.channel_id
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Fetch video list
    print(f"Fetching video list for channel {channel_id}...")
    videos = fetch_video_list(channel_id, args.limit)
    print(f"Found {len(videos)} videos.")

    # Write CSV
    csv_path = output_dir / f"{channel_id.replace('/', '_')}.csv"
    write_csv(videos, csv_path)
    print(f"Video list written to {csv_path}")

    # Download videos if requested
    if not args.no_download:
        print("Downloading videos...")
        for video in videos:
            download_video(video['id'], output_dir)
        print("Download completed.")
    else:
        print("Skipping download (--no-download flag).")

if __name__ == '__main__':
    main()
