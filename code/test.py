import cv2

import os
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
cap = cv2.VideoCapture("rtsp://pislave.local:8080/", cv2.CAP_FFMPEG)
#cap = cv2.VideoCapture('tcp://pislave.local:5000')
#cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 900)

while True:
    
    ret, frame = cap.read()

    if ret == True:

        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('frame',frame)


        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()
