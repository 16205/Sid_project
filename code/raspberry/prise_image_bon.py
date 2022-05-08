import sys
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

def imageCapture(scan_name, name_picture, camera):
    

    rawCapture = PiRGBArray(camera)

    # allow the camera to warm up
    time.sleep(0.1)

    # grab image from the camera
    camera.capture(rawCapture, format='bgr')
    img = rawCapture.array

    # on stocke l'image rgb
    cv2.imwrite(f"/home/pi/Sid_project/scans/{scan_name}/scanRight/" + name_picture + '.jpg', img)
