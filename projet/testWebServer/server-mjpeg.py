from flask import Flask, Response
import cv2
import threading
import time

app = Flask(__name__)

# serveur de rebroadcast
frame_buffer = None
lock = threading.Lock()

def update_frame_buffer():
    global frame_buffer
    cap = cv2.VideoCapture("http:10.0.0.131:81/stream")

    if not cap.isOpened():
        print("Error: Failed to open video stream.")
        return

    while True:
        ret, frame = cap.read()
        
        if not ret or frame is None:
            print("Failed to grab frame")
            continue
        
        with lock:
            frame_buffer = frame

@app.route('/')
def stream():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen():
    while True:
        if frame_buffer is not None:
            ret, jpeg = cv2.imencode('.jpg', frame_buffer)
            
            if not ret:
                print("Failed to encode frame to JPEG")
                continue
            
            frame_bytes = jpeg.tobytes()
            yield (b'--frame\r\n' 
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')
        else:
            time.sleep(0.01)

if __name__ == '__main__':
    # thread pour update le buffer d'images
    threading.Thread(target=update_frame_buffer, daemon=True).start()

    app.run(host='0.0.0.0', port=5050)

