#!bin/bash

timeout 5 cvlc http://127.0.0.1:5050 --sout "#transcode{venc=x264{fps=2}}:file{dst=/home/pi/Git/hailo-rpi5-examples/projet/buffer-videos/output.mp4}" --run-time=5 vlc://quit

ffmpeg -i /home/pi/Git/hailo-rpi5-examples/projet/buffer-videos/output.mp4 -r 25 -s 640x640 -c:a copy /home/pi/Git/hailo-rpi5-examples/projet/buffer-videos/output-bis.mp4

source /home/pi/Git/hailo-rpi5-examples/setup_env.sh

source /home/pi/Git/hailo-rpi5-examples/projet/test.sh /home/pi/Git/hailo-rpi5-examples/projet/buffer-videos/output-bis /home/pi/Git/hailo-rpi5-examples/projet/resultat

source /home/pi/test-venv/bin/activate

python /home/pi/Git/hailo-rpi5-examples/projet/seconde-ia.py /home/pi/Git/hailo-rpi5-examples/projet/resultat.txt


