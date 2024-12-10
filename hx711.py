import lgpio
import time

DATA_PIN = 17
CLK_PIN = 27

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


for _ in range(10):
    data = read_hx711()
    print(f"HX711 Veri: {data}")
    time.sleep(0.5)

lgpio.gpiochip_close(h)