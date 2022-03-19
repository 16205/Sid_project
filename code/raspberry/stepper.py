#######################################
# Copyright (c) 2021 Maker Portal LLC
# Author: Joshua Hrisko
#######################################
#
# NEMA 17 (17HS4023) Raspberry Pi Tests
# --- rotating the NEMA 17 to test
# --- wiring and motor functionality
#######################################

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

# define GPIO pins
direction= 22 # Direction (DIR) GPIO Pin
step = 23 # Step GPIO Pin
EN_pin = 24 # enable pin (LOW to enable)

mymotortest = RpiMotorLib.A4988Nema(direction, step, (2,3,4), "A4988")
GPIO.setmode(GPIO.BCM)
GPIO.setup(EN_pin,GPIO.OUT) # set enable pin as output

'''
step size : 
full = 1000 ; 0.36°
half = 2000 ; 0.18°
1/4  = 4000 ; 0.09°
1/8 = 1600 ; 0.225°
1/16 = 3200; 0.1125°
'''

def makeStep(number_of_step, step_size, doEnd = True):
    print(f"making {number_of_step} steps at {step_size} size")

    GPIO.output(EN_pin,GPIO.LOW) # pull enable to low to enable motor
    mymotortest.motor_go(False,         # True=Clockwise, False=Counter-Clockwise
                        step_size ,     # Step type (Full,Half,1/4,1/8,1/16,1/32)
                        number_of_step, # number of steps
                        .05,            # step delay [sec]
                        False,          # True = print verbose output 
                        .05)            # initial delay [sec]
    if doEnd:
        GPIO.output(EN_pin,GPIO.HIGH)


def stopMotor():
    print("stop")
    mymotortest.motor_stop()
    GPIO.cleanup()


# TO RUN INDEPENDENTLY
makeStep(4000,"1/4")
 