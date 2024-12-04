#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <video_file> <python_script>"
    exit 1
fi

# Get the input video file and Python script
video_file=$1
python_script=$2

# Get the number of frames in the video
frame_count=$(ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of default=noprint_wrappers=1:nokey=1 "$video_file")

# Check if the frame count was successfully retrieved
if [ -z "$frame_count" ]; then
    echo "Failed to retrieve the number of frames from the video file."
    exit 1
fi

# Run the Python script in the background and capture its PID
python3 "$python_script" --input  "$video_file" &
python_pid=$!

# Monitor the output of the Python script
python3 "$python_script" "$video_file" | while IFS= read -r line; do
    echo "$line"
    if [[ "$line" =~ Frame\ count:\ ([0-9]+) ]]; then
        current_frame=${BASH_REMATCH[1]}
        if [ "$current_frame" -ge $((frame_count + 1)) ]; then
            echo "Reached frame count + 1. Stopping the script."
            kill -9 "$python_pid"
            break
        fi
    fi
done
