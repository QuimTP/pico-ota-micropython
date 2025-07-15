import ugit
from machine import Pin
import time

LED = Pin("LED", Pin.OUT)

pin = Pin(5,Pin.IN,Pin.PULL_DOWN)
if pin.value() is 0:
    LED.on()
    ugit.pull_all() 

#main code here
TIME_MS=200
while True:
    LED.off()
    time.sleep_ms(TIME_MS)
    LED.on()
    time.sleep_ms(TIME_MS)
