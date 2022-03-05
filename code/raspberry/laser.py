"""USE LASER WITH A DIGITAL PIN"""

# from gpiozero import LED
# led = LED(17)


"""USE LASER WITH A PWM PIN"""

import RPi.GPIO as GPIO

ledpin = 12				        # PWM pin connected to LED
GPIO.setwarnings(False)			#disable warnings
GPIO.setmode(GPIO.BOARD)		#set pin numbering system
GPIO.setup(ledpin,GPIO.OUT)
pi_pwm = GPIO.PWM(ledpin,1000)  #create PWM instance with frequency
	

def setDuty(duty):
    """
    Change the duty cycle of the pwm
    PARAM: duty (0-100)
    """
    global dutyCycle
    dutyCycle = duty
    # pi_pwm.ChangeDutyCycle(duty)
    
def turnLaserOn():
    print("on")
    pi_pwm.start(dutyCycle)	
    print(dutyCycle)
    # led.on()
def turnLaserOff():
    print("off")
    pi_pwm.stop()
    # led.off()