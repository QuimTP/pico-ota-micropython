import ugit
from machine import Pin
import time

ugit.pull_all() 

#main code here
TIME_MS=100
LED = Pin("LED", Pin.OUT)
while True:
    LED.off()
    time.sleep_ms(TIME_MS)
    LED.on()
    time.sleep_ms(TIME_MS)
