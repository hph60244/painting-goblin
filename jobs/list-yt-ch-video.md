use $PAINTING_GOBLIN_DIR/skills/build-python-cli-tool to write a tool for querying all video data from youtube channel.

- Usage : `python list-yt-ch-video.py <CHANNEL_ID> <OUTPUT_DIR>`
- Args :
  - CHANNEL_ID : target channel id for querying
  - OUTPUT_DIR : folder path for output file
- Others :
  - download the best quility video and audio
  - output data file format is csv
  - output data file name is channel id
  - output data has following for all video:
    - video id
    - video name
    - video duration
  - use this channel id for testing : `@TsunomakiWatame`
