from flask import Flask, Response
import gi
import subprocess

# Import GStreamer Python bindings
gi.require_version('Gst', '1.0')
from gi.repository import Gst

# Initialize GStreamer
Gst.init(None)

app = Flask(__name__)

@app.route('/')
def stream():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen():
    # Updated GStreamer pipeline
    command = [
        'gst-launch-1.0',
        'souphttpsrc', 'location=http://192.168.1.3:81/stream',
        '!', 'decodebin',
        '!', 'videoconvert',
        '!', 'jpegenc',
        '!', 'appsink'
    ]
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        frame = process.stdout.read(1024*1024)  # Read in chunks of 1MB

        if len(frame) == 0:
            print("Error reading frame or stream ended")
            break

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050)

