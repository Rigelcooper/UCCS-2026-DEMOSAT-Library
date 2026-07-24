from datetime import datetime
import time
import os
import board
import adafruit_bmp3xx
from digitalio import DigitalInOut


def initialize_bmp388(retries=3):
    for attempt in range(retries):
        try:
            time.sleep(0.5)

            spi = board.SPI()
            cs = DigitalInOut(board.CE0)
            bmp = adafruit_bmp3xx.BMP3XX_SPI(spi, cs)

            bmp.pressure_oversampling = 8
            bmp.temperature_oversampling = 2

            return bmp
        except Exception as e:
            print(f"Initialization attempt {attempt + 1} failed: {e}")

            if attempt == retries - 1:
                raise
            time.sleep(1)


try:
    bmp = initialize_bmp388()
    print("BMP388 initialized successfully.\n")

    filename = "bmp388_log.csv"
    new_file = not os.path.exists(filename)

    with open(filename, "a") as f:
        if new_file:
            f.write("timestamp,pressure,temperature\n")

            while True:
                try:
                    now = datetime.now()
                    pressure = bmp.pressure
                    temperature = bmp.temperature
                    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

                    print(f"[{timestamp}] "
                        f"Pressure: {pressure:7.2f} hPa "
                        f"Temperature: {temperature:5.2f} °C"
                        )
                    f.write(f"{timestamp},{pressure:.2f},{temperature:.2f}\n")
                    f.flush()

                except Exception as e:
                    print(f"BMP388 read error: {type(e).__name__}: {e}")

                time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram stopped by user.")

except Exception as e:
    print("Failed during initialization.")
    print(e)
