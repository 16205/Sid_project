""" USE LASER WITH A PWM PIN"""
import RPi.GPIO as IO       # calling header file which helps us use GPIO’s of PI

import time                 # calling time to provide delays in program

# IO.setwarnings(False)      # do not show any warnings

IO.setmode (IO.BCM)        # we are programming the GPIO by BCM pin numbers. (PIN33 as ‘GPIO13')

# IO.setup(13,IO.OUT)        # initialize GPIO13 as an output.

p = IO.PWM(13,100)          # GPIO13 as PWM output, with 100Hz frequency

def setDuty(duty):
    """
    Change the duty cycle of the pwm
    PARAM: duty (0-100)
    """
    global dutyCycle
    dutyCycle = duty
    p.ChangeDutyCycle(duty)
    
def turnLaserOn():
    print("on")
    p.start(dutyCycle)	
    print(dutyCycle)

def turnLaserOff():
    print("off")
    p.stop()