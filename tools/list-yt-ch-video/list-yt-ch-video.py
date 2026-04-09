#!/usr/bin/env python3
"""
YouTube Channel Video Lister
Lists all videos from a YouTube channel with ID, name, and duration.
"""

import argparse
import csv
import os
import sys
import yt_dlp
from yt_dlp.utils import DownloadError

def safe_print(text: str, file=sys.stdout):
    """Print text safely, handling encoding errors."""
    try:
        print(text, file=file)
    except UnicodeEncodeError:
        # Replace non-encodable characters with '?'
        encoding = file.encoding if hasattr(file, 'encoding') else (sys.stdout.encoding or 'utf-8')
        encoded = text.encode(encoding, errors='replace').decode(encoding)
        print(encoded, file=file)

def construct_channel_url(channel_id: str) -> str:
    """Convert channel identifier to YouTube videos URL."""
    base = None
    if channel_id.startswith('@'):
        base = f'https://www.youtube.com/{channel_id}'
    elif channel_id.startswith('UC'):
        # Assume channel ID
        base = f'https://www.youtube.com/channel/{channel_id}'
    else:
        # Try as custom handle without @, or assume it's a full URL
        if channel_id.startswith('http'):
            base = channel_id
        else:
            base = f'https://www.youtube.com/@{channel_id}'
    # Ensure we target the videos tab, avoid duplicate
    if '/videos' not in base:
        # Ensure no double slash
        if not base.endswith('/'):
            base += '/'
        base += 'videos'
    return base

def get_channel_videos(channel_url: str):
    """
    Fetch all video entries from a channel using yt-dlp.
    Returns list of dicts with keys: id, title, duration.
    """
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(channel_url, download=False)
            if not info:
                safe_print(f'No data retrieved for {channel_url}', file=sys.stderr)
                sys.exit(1)

            # Determine if info is a channel with entries or a playlist
            entries = info.get('entries')
            if not entries:
                safe_print(f'No videos found for {channel_url}', file=sys.stderr)
                sys.exit(1)

            videos = []
            for entry in entries:
                video_id = entry.get('id')
                title = entry.get('title')
                duration = entry.get('duration')
                if video_id and title:
                    videos.append({
                        'id': video_id,
                        'title': title,
                        'duration': duration if duration else 0
                    })
            return videos
    except DownloadError as e:
        safe_print(f'Error fetching channel data: {e}', file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        safe_print(f'Unexpected error: {e}', file=sys.stderr)
        sys.exit(1)

def write_csv(videos, output_dir: str, channel_id: str):
    """Write video list to CSV file."""
    os.makedirs(output_dir, exist_ok=True)
    # Sanitize channel_id for filename (remove @ and other invalid chars)
    import re
    safe_name = re.sub(r'[\\/*?:"<>|]', '_', channel_id)
    if not safe_name.endswith('.csv'):
        safe_name += '.csv'
    csv_path = os.path.join(output_dir, safe_name)

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['video id', 'video name', 'video duration'])
        writer.writeheader()
        for video in videos:
            writer.writerow({
                'video id': video['id'],
                'video name': video['title'],
                'video duration': video['duration']
            })
    safe_print(f'CSV saved to {csv_path}')
    return csv_path

def main():
    parser = argparse.ArgumentParser(
        description='List all videos from a YouTube channel and save as CSV.'
    )
    parser.add_argument(
        'channel_id',
        help='YouTube channel ID (e.g., @TsunomakiWatame or UC...)'
    )
    parser.add_argument(
        'output_dir',
        help='Output directory for CSV file'
    )
    args = parser.parse_args()

    channel_url = construct_channel_url(args.channel_id)
    safe_print(f'Fetching videos from {channel_url}')
    videos = get_channel_videos(channel_url)
    safe_print(f'Found {len(videos)} videos')
    write_csv(videos, args.output_dir, args.channel_id)

if __name__ == '__main__':
    main()
