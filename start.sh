#!/bin/bash

# if (( "${UID}" != 0 )) ; then
#     echo "You are not root, exiting ..."
#     exit 1
# fi

if ! type ffmpeg &> /dev/null ; then
    echo "
    ffmpeg is not installed or not in PATH.
    Exiting ...      
    "
    exit 127
fi

if ! type python &> /dev/null ; then
    echo "
    python is not installed or not in PATH.
    Exiting ...      
    "
    exit 127
fi

if ! type "geckodriver" &> /dev/null ; then
    echo "
    Firefox geckodriver is not in PATH.
    Exiting ..."
    exit 127
fi

# echo "Starting python requirements installation:"
# python -m pip install -r ./requirements.txt

# if [ $? == 1 ]; then
#     echo "An error occured while installing requirements with pip, make sure pip is installed and accessible with python -m pip"
#     exit 1
# fi

if [ -d "./shots" ]; then
    echo "Shots folder exists, removing dir (and files of it) and making it again." && rm -rf shots && mkdir shots
else
    echo "Shots folder does not exist, making shots directoy." && mkdir shots
fi

echo "Starting recording process ..."

DURATION=`python sound-duration.py $2`
echo "Duration: ${DURATION}"

FRAME_RATE=`python video-recorder.py $1 ${DURATION}`

echo "Creating video stream:"
ffmpeg -r "${FRAME_RATE}" -f image2 -s 1920x1080 -i "shots/screenshot%d.png" -vcodec libx264 -crf 25 -pix_fmt yuv420p video-output.mp4

echo "Creating sound stream:"
ffmpeg -i "$2" -map 0:a -acodec adpcm_ima_wav sound-output.wav

echo "Merging sound stream with video stream:"
ffmpeg -i video-output.mp4 -i sound-output.wav -c copy final.mkv