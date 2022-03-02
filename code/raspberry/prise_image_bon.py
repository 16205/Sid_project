import sys
import cv2
from picamera.array import piRGBArray
import time

# initialize the camera and grab a reference to the raw camera capture  
camera = piCamera()
rawCapture = PiRGBArray(camera)

#allow the camera to warm up
time.sleep(0.1)

#grab image from the camera
camera.capture(rawCapture, format='bgr')
img = rawCapture.array

#on stocke l'image rgb
cv2.imwrite(sys.argv[1]+'/'+sys.argv[2]+'_complet.jpg', img)
