from gpiozero import DigitalInputDevice
from threading import Lock
from datetime import datetime
import time
import os

PIN = 17
counts = 0
CALIBRATION_CPM_PER_USVH = 153.8
TEST_DURATION = 10 * 60
start_time = time.monotonic()

lock = Lock()

tube = DigitalInputDevice(PIN,pull_up=True)

def reading_detected():
        global counts
        with lock:
            counts += 1
tube.when_activated = reading_detected
print("Geiger counter started.")
print("Counting pulses for 60 seconds...")

try:
    filename = "geiger_log.csv"
    new_file = not os.path.exists(filename)
    print(f"logging to {filename}\n")

    with open(filename,"a") as f:
        if new_file:
            f.write("timestamp,pulses,cpm,dose_microSv_h\n")
            f.flush()

        while time.monotonic() - start_time < TEST_DURATION:

            start = time.monotonic()
            time.sleep(60)
            elapsed = time.monotonic() - start

            with lock:
                pulse_count = counts
                counts = 0

            cpm = pulse_count * (60 / elapsed)

            usvh = cpm / CALIBRATION_CPM_PER_USVH
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(
                f"[{timestamp}] "
                f"Pulse Count: {pulse_count} "
                f"CPM: {cpm:.1f} "
                f"Dose Rate: {usvh:.3f} μSv/h"
            )
            f.write(f"{timestamp},{pulse_count},{cpm:.1f},{usvh:.3f}\n")
            f.flush()

except KeyboardInterrupt:
    print("\nGeiger counter stopped.")