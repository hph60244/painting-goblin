#!/usr/bin/env python3
"""
Download YouTube video with highest quality and convert to MP4.
Usage: python dl-yt-video.py <VIDEO_ID> <OUTPUT_DIR>
"""

import sys
import os
import subprocess
import logging
from pathlib import Path

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def check_yt_dlp():
    try:
        subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def download_video(video_id: str, output_dir: str):
    output_path = Path(output_dir).absolute()
    output_path.mkdir(parents=True, exist_ok=True)
    
    has_ffmpeg = check_ffmpeg()
    if has_ffmpeg:
        format_str = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        merge_opt = ['--merge-output-format', 'mp4']
    else:
        logging.warning('ffmpeg not found, downloading single MP4 stream (may be lower quality)')
        format_str = 'best[ext=mp4]'
        merge_opt = []
    
    cmd = [
        'yt-dlp',
        '-f', format_str,
        *merge_opt,
        '-o', str(output_path / '%(title)s.%(ext)s'),
        f'https://www.youtube.com/watch?v={video_id}'
    ]
    
    logging.info(f'Downloading video {video_id} to {output_path}')
    logging.debug(f'Command: {" ".join(cmd)}')
    
    try:
        subprocess.run(cmd, check=True)
        logging.info('Download completed successfully')
    except subprocess.CalledProcessError as e:
        logging.error(f'Download failed with exit code {e.returncode}')
        sys.exit(1)

def main():
    if len(sys.argv) != 3:
        print('Usage: python dl-yt-video.py <VIDEO_ID> <OUTPUT_DIR>')
        sys.exit(1)
    
    video_id = sys.argv[1]
    output_dir = sys.argv[2]
    
    setup_logging()
    
    if not check_yt_dlp():
        logging.error('yt-dlp is not installed or not in PATH.')
        logging.error('Please install it via: pip install yt-dlp')
        sys.exit(1)
    
    download_video(video_id, output_dir)

if __name__ == '__main__':
    main()