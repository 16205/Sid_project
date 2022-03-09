#######################################
# Copyright (c) 2021 Maker Portal LLC
# Author: Joshua Hrisko
#######################################
#
# NEMA 17 (17HS4023) Raspberry Pi Tests
# --- rotating the NEMA 17 to test
# --- wiring and motor functionality
#
#  
#######################################
#
"""
source = https://makersportal.com/blog/raspberry-pi-stepper-motor-control-with-nema-17
TUTO = https://lastminuteengineers.com/a4988-stepper-motor-driver-arduino-tutorial/
library = https://github.com/gavinlyonsrepo/RpiMotorLib
"""


import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time

################################
# RPi and Motor Pre-allocations
################################
#
#define GPIO pins
direction= 22 # Direction (DIR) GPIO Pin
step = 23 # Step GPIO Pin
EN_pin = 24 # enable pin (LOW to enable)

# Declare a instance of class pass GPIO pins numbers and the motor type
#mymotortest = RpiMotorLib.A4988Nema(direction, step, (21,21,21), "A4988")
#GPIO.setup(EN_pin,GPIO.OUT) # set enable pin as output

###########################
# Actual motor control
###########################
#
# GPIO.output(EN_pin,GPIO.LOW) # pull enable to low to enable motor
# mymotortest.motor_go(False, # True=Clockwise, False=Counter-Clockwise
#                      "Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
#                      200, # number of steps
#                      .0005, # step delay [sec]
#                      False, # True = print verbose output 
#                      .05) # initial delay [sec]
# GPIO.cleanup() # clear GPIO allocations after run

'''
step size : 
full = 200 ; 1.8°
half = 400 ; 0.9°
1/4  = 800 ; 0.45°
1/8 = 1600 ; 0.225°
1/16 = 3200; 0.1125°
1/32 = 6400;0.05625°
'''

def makeStep(number_of_step, step_size):
    global mymotortest
    mymotortest = RpiMotorLib.A4988Nema(direction, step, (21,21,21), "A4988")
    GPIO.setup(EN_pin,GPIO.OUT) # set enable pin as output
    print(f"making {number_of_step} steps")
    GPIO.output(EN_pin,GPIO.LOW) # pull enable to low to enable motor
    mymotortest.motor_go(False, # True=Clockwise, False=Counter-Clockwise
                     "Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                     200, # number of steps
                     .0005, # step delay [sec]
                     False, # True = print verbose output 
                     .05) # initial delay [sec]

    GPIO.cleanup() # clear GPIO allocations after run
    


def stopMotor():
    mymotortest.motor_stop()
    GPIO.cleanup()
 