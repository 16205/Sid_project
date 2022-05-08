import RPi.GPIO as IO           # calling header file which helps us use GPIO’s of PI
import time                     # calling time to provide delays in program

def gpioSetup():   
    
    IO.cleanup()

    IO.setwarnings(False)           # do not show any warnings
    IO.setmode(IO.BCM)              # we are programming the GPIO by BCM pin numbers. (PIN33 as ‘GPIO13’)

    pwm_laser = 13
    enable = 24

    IO.setup(pwm_laser, IO.OUT)     # initialize GPIO13 (PWM) as an output.
    IO.setup(enable, IO.OUT)        # initialize GPIO24 as an output.

    IO.output(enable, IO.HIGH)      # set enable to high to lock the motor in place