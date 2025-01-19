import cv2

# Affiche dans une fenêtre WAYLAND le flux MJPEG
cam = cv2.VideoCapture("http://192.168.1.3:81/stream")

# Get the default frame width and height
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))



while True:
    ret, frame = cam.read()


    cv2.imshow('Camera', frame)


    if cv2.waitKey(1) == ord('q'):
        break


cam.release()
out.release()
cv2.destroyAllWindows()
