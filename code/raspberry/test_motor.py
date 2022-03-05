import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time
import stepper

direction= 22 # Direction (DIR) GPIO Pin
step = 23 # Step GPIO Pin
EN_pin = 24 # enable pin (LOW to enable)
#GPIO.output(EN_pin,GPIO.LOW) # pull enable to low to enable motor
GPIO_pins = (14, 15, 18)


# Declare a instance of class pass GPIO pins numbers and the motor type
mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")
step_number = 200
step_size = "Full"


#on fait faire un step
while True:
	mymotortest.motor_go(False, step_size, step_number, 0.005, False, initdelay = 0.05)
