#script to take the images for a scan
#arg1 : the scan's name
#arg2 : the number of steps
from tkinter import N
import cv2
import os
import pexpect
from pexpect import pxssh
import sys
#import sshTools
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
# import stepper
# import laser
import time
from raspberry.stepper import *
from raspberry.laser import *
# reading the scan_name from the input
# scan_name = sys.argv[1]
# quality = sys.argv[2]

def runScan(quality, laser_power = 30, color_space="Red", scale=10, scan_name = "test"):
    """
    Run the scan : activate stepper and take pictures\n
    Params:\n
    - quality = step size ("High","Medium","Low","test")\n
    - laser_power = output power in pwm (0 to 100)\n
    - color_space = color spectrum to work with ("Saturation", "Hue","Red")\n
    - scale = size of the piece to scan (5,10,15,20)\n
    - scan_name = name of the scan (if None => 'test')
    """
    
    print(scan_name)
    print(quality)

    # define GPIO pins for the motor
    GPIO.setmode(GPIO.BCM)

    # defining the caracteristic of on step of the motor
    if quality == "test":
        step_number = 10
        step_size = "Full"
        step_nbr = 100
    elif quality == "Low":
        step_number = 10
        step_size = "1/4"
        step_nbr = 400
    elif quality == "Medium":
        step_number = 4
        step_size = "1/4"
        step_nbr = 1000
    elif quality == "High":
        step_number = 1
        step_size = "1/4"
        step_nbr = 4000
    
    # turn led On
    setDuty(laser_power)
    turnLaserOn()

    
    for i in range(step_nbr):


        # Run the stepper
        makeStep(step_number,step_size, doEnd=True)
        time.sleep(.2)

    # turn laser off
    turnLaserOff()




    GPIO.cleanup() # clear GPIO allocations after run
    
#runScan("test")