from machine import Pin, I2C
import utime
import dht
from ds3231 import DS3231

# Sensor DHT11
dht_sensor = dht.DHT11(Pin(2))

# LEDs GPIO7–10
led_pins = [Pin(i, Pin.OUT) for i in range(7, 11)]

# Botons GPIO3–6 i 11–14
button_gpios = [3, 4, 5, 6, 11, 12, 13, 14]
button_pins = [Pin(gpio, Pin.IN, Pin.PULL_UP) for gpio in button_gpios]

# RTC DS3231 a I2C0 (SDA=0, SCL=1)
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
rtc = DS3231(i2c)

# (Opcional) Estableix hora si cal (només 1 cop)
# rtc.set_time(2025, 7, 7, 12, 0, 0)

def llegir_dht():
    try:
        dht_sensor.measure()
        t = dht_sensor.temperature()
        h = dht_sensor.humidity()
        return t, h
    except Exception as e:
        print("Error DHT11:", e)
        return None, None

while True:
    y, m, d, hh, mm, ss = rtc.get_time()
    temps_str = "{:02d}/{:02d}/{} {:02d}:{:02d}:{:02d}".format(d, m, y, hh, mm, ss)
    print("Hora RTC:", temps_str)

    t, h = llegir_dht()
    if t is not None:
        print("Temp: {}°C | Hum: {}%".format(t, h))

    boto_estats = [not b.value() for b in button_pins]

    for i, estat in enumerate(boto_estats):
        print("Botó {}: {}".format(i + 1, "PREMUT" if estat else "lliure"))

    for i in range(4):
        led_pins[i].value(boto_estats[i])

    print("-" * 40)
    utime.sleep(1)

