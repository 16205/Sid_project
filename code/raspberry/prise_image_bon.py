import sys
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

def imageCapture(scan_name, name_picture):
    
    # initialize the camera and grab a reference to the raw camera capture  
    camera = PiCamera()
    rawCapture = PiRGBArray(camera)

    # allow the camera to warm up
    time.sleep(0.1)

    # grab image from the camera
    camera.capture(rawCapture, format='bgr')
    img = rawCapture.array

    # on stocke l'image rgb
    cv2.imwrite('/home/pi/Sid_project/scans/' + scan_name + '/' + name_picture + '.jpg', img)
