### import necessary libraries ###
from gpiozero import DigitalInputDevice
from threading import Lock
from datetime import datetime
import time
import os

### specify GPIO pin number for communication ###
PIN = 17

### define necessary variables ###
    # counts keeps track of the number of radiation events #
counts = 0
### calibration constant for Geiger Counter ###
  # allows us to approx. uSv/h (where 153.8 CPM = 1uSV/h) #
CALIBRATION_CPM_PER_USVH = 153.8
### lock keeps changes to counts var. from happening at the same time ##
lock = Lock()
### defines tube variable linking the device to pin 17, and HIGH(voltage) = True activation ###
tube = DigitalInputDevice(PIN,pull_up=True)

### callback function activates when pulse is detected ###
def reading_detected():
        global counts
        with lock:
            ### counts is increments per pulse detected ###
            counts += 1
### event handler links activation to pulse reading ###
tube.when_activated = reading_detected
print("Geiger counter started.")
print("Counting pulses for 60 seconds...")

### main try-except block for testing ###
try:
    ### defines csv file, opens new file if file DNE ###
    filename = "geiger_log.csv"
    new_file = not os.path.exists(filename)
    print(f"logging to {filename}\n")

### defines column titles for new file ###
    # flush empties buffer "cache" while keeping file open #
    with open(filename,"a") as f:
        if new_file:
            f.write("timestamp,pulses,cpm,dose_microSv_h\n")
            f.flush()

### Main while loop ###
        while True:
            ### starts timer, separates time and elapsed for CPM var ###
            start = time.monotonic()
            time.sleep(60)
            elapsed = time.monotonic() - start

            with lock:
                pulse_count = counts
                counts = 0
            ### calculates pulse rate ###
            cpm = pulse_count * (60 / elapsed)
### calculates dose rate for Geiger Counter ###
            usvh = cpm / CALIBRATION_CPM_PER_USVH
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(
                f"[{timestamp}] "
                f"Pulse Count: {pulse_count} "
                f"CPM: {cpm:.1f} "
                f"Dose Rate: {usvh:.3f} μSv/h"
            )
            ### logs data in csv ###
            f.write(f"{timestamp}, {pulse_count}, {cpm:.1f},{usvh:.3f}\n")
            f.flush()
### SIGINT by user (ctrl + c) ###
except KeyboardInterrupt:
    print("\nGeiger counter stopped.")