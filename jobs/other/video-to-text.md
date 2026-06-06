Use $AGENT_CWD/skills/build-python-cli-tool to write a tool for extracting speech text from video.

- Args :
  - VIDEO_PATH : target video file path
  - OUTPUT_DIR : folder path for output text file

- Features :
  - automatically creates output directory if it doesn't exist
  - speech text is extracted with timestamp in `HH:mm:ss` format
  - output video file format is txt
  - output video file name is video file name

- Others :
  - use this video id for testing : `$AGENT_CWD\.tmp\videos\【Animation MV】 What an amazing swing _角巻わため【original】.mp4`
