#!bin/bash

ffmpeg -i http://192.168.1.3:81/stream -t 5 -c:v copy output.mp4

ffmpeg -i output.mp4 -s 640x640 -c:a copy output-bis.mp4

source /home/pi/Git/hailo-rpi5-examples/setup_env.sh

source /home/pi/Git/hailo-rpi5-examples/projet/test.sh output-bis resultat

source /home/pi/test-venv/bin/activate

python /home/pi/Git/hailo-rpi5-examples/projet/seconde-ia.py resultat.txt


