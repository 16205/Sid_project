#script to control the temporary stepper 
import RPi.GPIO as GPIO
import time


def make_step(motor_pins, motor_step_counter, step_sequence, direction): 
    for pin in range(len(motor_pins)):
        GPIO.output(motor_pins[pin], step_sequence[motor_step_counter][pin])
        if direction == True:
            motor_step_counter =  (motor_step_counter -1) % 8
        elif direction == False:
            motor_step_counter = (motor_step_counter + 1) % 8
