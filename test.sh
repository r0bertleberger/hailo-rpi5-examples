#! /bin/bash


VIDEO_PATH="/home/pi/$1"

echo $VIDEO_PATH

if [ -e "$VIDEO_PATH" ]
then
	FRAME_NUMBER=$(ffprobe -v error -select_streams v:0 -count_packets  -show_entries stream=nb_read_packets -of csv=p=0 $VIDEO_PATH)
	echo $FRAME_NUMBER
else
	echo "le fichier n'existe pas"
fi

if (($FRAME_NUMBER > 0))
then
	TIME_TO_RUN=$(expr $(expr $FRAME_NUMBER / 40) + 1)

	echo $TIME_TO_RUN

	timeout $TIME_TO_RUN python basic_pipelines/pose_estimation.py --input $VIDEO_PATH >> resultats_$1.txt
else
	echo "probleme"
fi

python enlever-ligne.py resultats_$1.txt "Frame count: $FRAME_NUMBER"
