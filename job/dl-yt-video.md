use $PAINTING_GOBLIN_DIR/skills/build-python-cli-tool to write a tool for downloading youtube video.

- Usage : `python dl-yt-video.py <VIDEO_ID> <OUTPUT_DIR>`
- Args :
  - VIDEO_ID : target video id in origin youtube video url
  - OUTPUT_DIR : folder path for output video file
- Others :
  - download the best quility video and audio
  - output video file format is mp4
  - output video file name is based on video title, beware of special characters
  - automatically creates output directory if it doesn't exist
  - use this video id for testing : `d3UTywBDSW4`
