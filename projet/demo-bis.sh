#!bin/bash

echo "début de l'enregistrement de la vidéo......" >> /home/pi/Git/hailo-rpi5-examples/projet/resultat-bis.txt

timeout 5 cvlc http://127.0.0.1:5050 --sout "#transcode{venc=x264{fps=2}}:file{dst=/home/pi/Git/hailo-rpi5-examples/projet/buffer-videos/output.mp4}" --run-time=5 vlc://quit

echo "post-traitement de la vidéo......" >> /home/pi/Git/hailo-rpi5-examples/projet/resultat-bis.txt

ffmpeg -i /home/pi/Git/hailo-rpi5-examples/projet/buffer-videos/output.mp4 -r 25 -s 640x640 -c:a copy /home/pi/Git/hailo-rpi5-examples/projet/buffer-videos/output-bis.mp4

echo "analyse via YOLO-v8 de la vidéo......" >> /home/pi/Git/hailo-rpi5-examples/projet/resultat-bis.txt

source /home/pi/Git/hailo-rpi5-examples/setup_env.sh

source /home/pi/Git/hailo-rpi5-examples/projet/test.sh /home/pi/Git/hailo-rpi5-examples/projet/buffer-videos/output-bis.mp4 /home/pi/Git/hailo-rpi5-examples/projet/resultat.txt

echo "analyse par le random forest de la vidéo......" >> /home/pi/Git/hailo-rpi5-examples/projet/resultat-bis.txt
source /home/pi/test-venv/bin/activate

python /home/pi/Git/hailo-rpi5-examples/projet/seconde-ia.py /home/pi/Git/hailo-rpi5-examples/projet/resultat.txt >> /home/pi/Git/hailo-rpi5-examples/projet/resultat-bis.txt
