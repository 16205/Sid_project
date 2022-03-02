# from gpiozero import LED
from time import sleep

led = LED(17)

def turnLaserOn():
    print("on")
    led.on()
def turnLaserOff():
    print("off")
    led.off()


