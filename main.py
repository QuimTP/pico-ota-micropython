from machine import I2C, Pin
from pico_i2c_lcd import I2cLcd
from ds3231 import DS3231
import utime
import time
from ota_updater import OTAUpdater
import machine

def check_for_update():
    OTAUpdater('https://github.com/QuimTP/pico-ota-micropython').download_and_install_update_if_available('main')

check_for_update()

# Aquí el teu codi principal
print("Hola, món! Codi actualitzat.")


# --- CONFIGURACIÓ ---
I2C_SDA = 0
I2C_SCL = 1
LCD_ADDR = 0x3F  # o 0x27 si cal
LCD_ROWS = 2
LCD_COLS = 16

# --- INICIALITZACIÓ ---
i2c = I2C(0, sda=Pin(I2C_SDA), scl=Pin(I2C_SCL), freq=400000)
lcd = I2cLcd(i2c, LCD_ADDR, LCD_ROWS, LCD_COLS)
rtc = DS3231(i2c)

# Obté la data i hora actual del PC via Thonny
t = time.localtime()
# Format: (any, mes, dia, hora, minut, segon, 0, 0)
rtc.set_time((t[0], t[1], t[2], t[3], t[4], t[5], 0, 0))

print("Hora sincronitzada amb l'ordinador!")
print("Nou valor RTC:", rtc.get_time())


# --- BUCLE PRINCIPAL ---
while True:
    try:
        # Hora i temperatura del DS3231
        temp = rtc.get_temperature()
        y, m, d, h, mi, s = rtc.get_time()

        # Escriure a l'LCD
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("  Temp: {:.2f}C".format(temp))

        lcd.move_to(0, 1)
        lcd.putstr("  {:02d}:{:02d}  {:02d}/{:02d}  ".format(h, mi, d, m))

    except Exception as e:
        lcd.clear()
        lcd.putstr("Error RTC/Temp")
        print("Error:", e)

    utime.sleep(60)

