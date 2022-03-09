#script to take the images for a scan
#arg1 : the scan's name
#arg2 : the number of steps
import cv2
import os
import pexpect
from pexpect import pxssh
import sys
import sshTools
import RPi.GPIO as GPIO
import time
import stepper_temp

#setting up the motor
GPIO.setwarnings(False)

in1 = 17
in2 = 18
in3 = 27
in4 = 22

step_sleep = 0.002
step_count = 4096
direction = False

step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

GPIO.setmode( GPIO.BCM )

#set up the pins
GPIO.setmode( GPIO.BCM )
GPIO.setup( in1, GPIO.OUT )
GPIO.setup( in2, GPIO.OUT )
GPIO.setup( in3, GPIO.OUT )
GPIO.setup( in4, GPIO.OUT )

GPIO.output (in1, GPIO.LOW)
GPIO.output (in2, GPIO.LOW)
GPIO.output (in3, GPIO.LOW)
GPIO.output (in4, GPIO.LOW)

motor_pins = [in1,in2,in3,in4]
motor_step_counter = 0

#reading the scan_name from the input
scan_name = sys.argv[1]
quality = sys.argv[2]
print(scan_name)
print(quality)

#on crée les dossier pour le scan dans le master et dans la slave 
os.system('mkdir '+ scan_name) #on crée le dossier dans le master
sshTools.createFolderSlave(scan_name) #on crée le dossier dans le slave
print("folders created")


for i in range(step_count):
    name_picture_r = scan_name +"_R_"+str(i) #create the file name for the i th picture from the rigth camera
    name_picture_l = scan_name+"_L_"+str(i) #create the filename for the i th picture from the left camera
    #on prend les images
    print("name_picture_r = ", name_picture_r)
    print("name_picture_l = ", name_picture_l)
    os.system('python3 prise_image_bon.py '+scan_name+' '+name_picture_r) #on pose que le master sera la camera de droite
    print("im master taken")
    sshTools.takePictureWithSlave(scan_name, name_picture_l)
    print("imslave taken")
    stepper_temp.make_step(motor_pins, motor_step_counter, step_sequence, direction)


#après la prise d'image on recup les images
for i in range(step_count):
    name_picture = scan_name+"_L_"+str(i)
    sshTools.getPictureSlave(scan_name)

