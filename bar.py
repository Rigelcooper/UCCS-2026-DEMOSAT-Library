from datetime import datetime
import time

import board
import adafruit_bmp3xx
from digitalio import Digital InOut


def initialize_bmp388():

    spi = board.SPI()
    cs = DigitalInOut(board.D5)
    bmp = adafruit_bmp3xx.BMP3XX_SPI(spi,cs)

    bmp.pressure_oversampling = 8
    bmp.temperature_oversampling = 2

    return bmp

try:
    bmp = initialize_bmp388()
    print("BMP388 initialized successfully.\n")

    while True:
        try:
            now = datetime.now()
            pressure = bmp.pressure
            temperature = bmp.temperature
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

            print(f"Pressure: {pressure:7.2f} hPa")
            print(f"Temperature: {temperature:5.2f} °C")
            print(f"[{timestamp}]")

        except Exception as e:
            print(f"BMP388 read error:")
            print (e)

        time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram stopped by user.")

except Exception as e:
    print("Failed during initialization.")
    print(e)


