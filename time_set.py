import time
from ds3231 import DS3231
from machine import I2C, Pin

I2C_SDA = 0
I2C_SCL = 1

i2c = I2C(0, sda=Pin(I2C_SDA), scl=Pin(I2C_SCL), freq=400000)

rtc = DS3231(i2c)

t = time.localtime()
# Format: (any, mes, dia, hora, minut, segon, 0, 0)
rtc.set_time((t[0], t[1], t[2], t[3], t[4], t[5], 0, 0))

print("Hora sincronitzada amb l'ordinador!")
print("Nou valor RTC:", rtc.get_time())