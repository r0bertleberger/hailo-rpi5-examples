from flask import Flask, Response
import cv2
import threading
import time

app = Flask(__name__)

# Initialize a global variable to store frames
frame_buffer = None
lock = threading.Lock()

def update_frame_buffer():
    global frame_buffer
    cap = cv2.VideoCapture("http://192.168.1.3:81/stream")

    if not cap.isOpened():
        print("Error: Failed to open video stream.")
        return

    while True:
        ret, frame = cap.read()
        
        if not ret or frame is None:
            print("Failed to grab frame")
            continue
        
        # Acquire lock before updating the buffer
        with lock:
            frame_buffer = frame

        # Sleep for a short time to avoid overloading the server
        # time.sleep(0.1)

@app.route('/')
def stream():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen():
    while True:
        if frame_buffer is not None:
            # Encode the frame to JPEG
            ret, jpeg = cv2.imencode('.jpg', frame_buffer)
            
            if not ret:
                print("Failed to encode frame to JPEG")
                continue
            
            frame_bytes = jpeg.tobytes()
            yield (b'--frame\r\n' 
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')
        else:
            # Wait until a frame is available
            time.sleep(0.01)

if __name__ == '__main__':
    # Start a background thread to update the frame buffer
    threading.Thread(target=update_frame_buffer, daemon=True).start()
    
    # Run the Flask server
    app.run(port=5050)

