#script to take the images for a scan
#arg1 : the scan's name
#arg2 : the number of steps
from tkinter import N
import cv2
import os
import pexpect
from pexpect import pxssh
import sys
import sshTools
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import stepper

#reading the scan_name from the input
scan_name = sys.argv[1]
quality = sys.argv[2]
print(scan_name)
print(quality)
#define GPIO pins for the motor
GPIO.setmode(GPIO.BCM)
direction= 22 # Direction (DIR) GPIO Pin
GPIO.setup(direction, GPIO.OUT)
step = 23 # Step GPIO Pin
GPIO.setup(step, GPIO.OUT)
EN_pin = 24 # enable pin (LOW to enable)
GPIO.setup(EN_pin, GPIO.OUT)
print("setup motor done")
#defining the caracteristic of on step of the motor
if quality == "test":
    step_number = 10
    step_size = "Full"
    step_nbr = 20
elif quality == "low":
    step_number = 1
    step_size = "1/8"
    step_nbr = 1600
elif quality == "medium":
    step_number = 1
    step_size = "1/16"
    step_nbr = 3200
elif quality == "high":
    step_number = 1
    step_size = "1/32"
    step_nbr = 6400

#on crée les dossier pour le scan dans le master et dans la slave 
os.system('mkdir '+ scan_name) #on crée le dossier dans le master
sshTools.createFolderSlave(scan_name) #on crée le dossier dans le slave
print("folders created")
 


for i in range(step_nbr):
    name_picture_r = scan_name +"_R_"+str(i) #create the file name for the i th picture from the rigth camera
    name_picture_l = scan_name+"_L_"+str(i) #create the filename for the i th picture from the left camera
    #on prend les images
    print("name_picture_r = ", name_picture_r)
    print("name_picture_l = ", name_picture_l)
    os.system('python3 prise_image_bon.py '+scan_name+' '+name_picture_r) #on pose que le master sera la camera de droite
    print("im master taken")
    sshTools.takePictureWithSlave(scan_name, name_picture_l)
    print("imslave taken")
    stepper.makeStep(step_number, step_size)
    print("motor step done")

    
#après la prise d'image on recup les images
for i in range(quality):
    name_picture = scan_name+"_L_"+str(i)
    sshTools.getPictureSlave(scan_name)


GPIO.cleanup() # clear GPIO allocations after run
  