#!/usr/bin/python3
import time

from picamera2 import Picamera2, Preview

# Here we load up the tuning for the HQ cam and alter the default exposure profile.
# For more information on what can be changed, see chapter 5 in
# https://datasheets.raspberrypi.com/camera/raspberry-pi-camera-guide.pdf

tuning = Picamera2.load_tuning_file("imx708-b0311.json", "/opt/arducam")

picam2 = Picamera2(tuning=tuning)
picam2.configure(picam2.create_preview_configuration())
picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(10)