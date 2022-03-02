import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time
import stepper

#define GPIO pins for the motor
GPIO.setmode(GPIO.BOARD)
direction= 22 # Direction (DIR) GPIO Pin
GPIO.setup(direction, GPIO.OUT)
step = 23 # Step GPIO Pin
GPIO.setup(step, GPIO.OUT)
EN_pin = 24 # enable pin (LOW to enable)
GPIO.setup(EN_pin, GPIO.OUT)

step_number = 1
step_size = "1/32"
step_nbr = 6400

while(True):
    stepper.makeStep(step_number, step_size)
    print("step done")
    