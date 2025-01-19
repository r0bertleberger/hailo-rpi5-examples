#! /bin/bash


VIDEO_PATH="$1.mp4"
OUT_PATH="$2"

echo $VIDEO_PATH
echo $OUT_PATH

if [ -e "$VIDEO_PATH" ]
then
	FRAME_NUMBER=$(ffprobe -i $VIDEO_PATH -show_entries "stream=nb_frames" -of default=noprint_wrappers=1 | tail -n2 | head -n1 | sed 's/nb_frames='//)
	echo $FRAME_NUMBER
else
	echo "le fichier n'existe pas"
fi

if (($FRAME_NUMBER > 0))
then
	TIME_TO_RUN=$(expr $(expr $FRAME_NUMBER / 40) + 1)

	echo $TIME_TO_RUN

	timeout $TIME_TO_RUN python /home/pi/Git/hailo-rpi5-examples/basic_pipelines/pose_estimation.py --input $VIDEO_PATH >> $OUT_PATH.txt
else
	echo "probleme"
fi

python /home/pi/Git/hailo-rpi5-examples/projet/enlever-ligne.py $OUT_PATH.txt "Frame count: $FRAME_NUMBER"
