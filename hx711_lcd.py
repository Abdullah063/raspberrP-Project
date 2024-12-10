import time
from smbus2 import SMBus
from RPLCD.i2c import CharLCD
import lgpio

DATA_PIN = 17
CLK_PIN = 27

I2C_ADDR = 0x27
lcd = CharLCD(i2c_expander='PCF8574', address=I2C_ADDR, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A00', auto_linebreaks=True)

h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_input(h, DATA_PIN)
lgpio.gpio_claim_output(h, CLK_PIN)

def read_hx711():
    count = 0
    while lgpio.gpio_read(h, DATA_PIN) == 1:
        pass
    for _ in range(24):
        lgpio.gpio_write(h, CLK_PIN, 1)
        count = (count << 1) | lgpio.gpio_read(h, DATA_PIN)
        lgpio.gpio_write(h, CLK_PIN, 0)
    lgpio.gpio_write(h, CLK_PIN, 1)
    lgpio.gpio_write(h, CLK_PIN, 0)
    return count

tare = 100000
calibration_factor = 500

lcd.clear()
lcd.write_string("Tartim Hazir...")
time.sleep(2)

try:
    while True:
        raw_value = read_hx711()
        weight = (raw_value - tare) / calibration_factor
        formatted_weight = f"{weight:.2f}"
        lcd.clear()
        lcd.write_string("Agirlik:{}kg".format(formatted_weight))
        time.sleep(1)
except KeyboardInterrupt:
    print("Program durduruldu.")
finally:
    lgpio.gpiochip_close(h)
    lcd.clear()