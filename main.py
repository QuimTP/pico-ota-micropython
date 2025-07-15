from machine import Pin, I2C
from time import sleep
import dht
from ds3231 import DS3231
from i2c_lcd import I2cLcd
import ugit

# I2C configuration (GPIO0 = SDA, GPIO1 = SCL)
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)

# Detectem dispositius I2C
devices = i2c.scan()
if len(devices) < 3:
    print("⚠️ Falten dispositius I2C (LCD o RTC)")
else:
    print("I2C trobats:", devices)
    
def revisar_ota(estats_botons):
    if estats_botons[1]:
        print("🔄 Actualitzant via OTA...")
        lcd1602.clear()
        lcd1602.putstr("OTA iniciada")

        try:
            ugit.pull_all()
            print("✅ Actualització completada. Reiniciant...")
            sleep(2)
            import machine
            machine.reset()
        except Exception as e:
            print("❌ Error OTA:", e)


# Assignació adreces automàtica (ajusta si cal)
LCD1602_ADDR = devices[0]
LCD2004_ADDR = devices[1]
RTC_ADDR = devices[2]

# Inicialitzem pantalles LCD
lcd1602 = I2cLcd(i2c, LCD1602_ADDR, 2, 16)
lcd2004 = I2cLcd(i2c, LCD2004_ADDR, 4, 20)

lcd1602.clear()
lcd1602.putstr("Inici")
# RTC DS3231
rtc = DS3231(i2c)

# Sensor DHT11 al GPIO2
dht_sensor = dht.DHT11(Pin(2))

# Botons: GPIO3, 4, 5, 6, 11, 12, 13, 14, 15
botons = [Pin(i, Pin.IN, Pin.PULL_UP) for i in [3, 4, 5, 6, 11, 12, 13, 14]]

# LEDs: GPIO7, 8, 9, 10
leds = [Pin(i, Pin.OUT) for i in [7, 8, 9, 10]]

def llegir_botons():
    estats = []
    for i, boto in enumerate(botons):
        estat = not boto.value()  # actiu quan es prem
        estats.append(estat)
        if i < len(leds):
            leds[i].value(estat)  # Encenem LEDs amb els primers 4 botons
    return estats

def mostrar_lcds(temp, humitat, hora):
    lcd1602.clear()
    lcd2004.clear()
    lcd1602.putstr("Temp:{}C\nHum:{}%".format(temp, humitat))
    lcd2004.putstr("Hora: {}\nTemp:{}C\nHum:{}%".format(hora, temp, humitat))
    lcd2004.putstr('HOLA PIROLACONYAS')

while True:
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
    except Exception as e:
        print("Error DHT11:", e)
        temp = hum = 0

    # Llegim hora del RTC
    try:
        any, mes, dia, wd, hora, minut, segon, _ = rtc.datetime()
        hora_str = "{:02d}:{:02d}:{:02d}".format(hora, minut, segon)
    except:
        hora_str = "--:--:--"

    # Mostrem info
    mostrar_lcds(temp, hum, hora_str)

    # Llegim botons i controlem LEDs
    estats_botons = llegir_botons()

    # Debug per consola
    print("Hora:", hora_str, "Temp:", temp, "Hum:", hum, "Botons:", estats_botons)

    revisar_ota(estats_botons)
    sleep(0.1)


