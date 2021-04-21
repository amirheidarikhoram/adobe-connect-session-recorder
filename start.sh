#!/bin/bash

echo "Make sure python and ffmpeg are in your PATH"
echo "Starting recording process ..."

DURATION=`python sound-duration.py $2`
echo "Duration: ${DURATION}"

sudo mkdir shots
FRAME_RATE=`python video-recorder.py $1 ${DURATION}`

echo "Creating video stream:"
ffmpeg -r "${FRAME_RATE}" -f image2 -s 1920x1080 -i "shots/screenshot%d.png" -vcodec libx264 -crf 25 -pix_fmt yuv420p video-output.mp4

echo "Creating sound stream:"
ffmpeg -i "$2" -map 0:a -acodec adpcm_ima_wav sound-output.wav

echo "Merging sound stream with video stream:"
ffmpeg -i video-output.mp4 -i sound-output.wav -c copy final.mkv