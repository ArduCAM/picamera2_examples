#!/usr/bin/python3

from picamera2 import Picamera2, Preview

EXPOURSE_TIME =  20000
i = 1

picam2 = Picamera2()
# picam2.start_preview(Preview.QTGL)

capture_config = picam2.create_still_configuration(main={"format": 'RGB888', "size": (1920, 1080)})
picam2.configure(capture_config)


picam2.set_controls({"ExposureTime": EXPOURSE_TIME, "AnalogueGain": 1.0})
picam2.start()
RGB888 = picam2.capture_array("main")
print("Start save ldr_{:02d}.jpg".format(i))
picam2.switch_mode_and_capture_file(capture_config, "ldr_{:02d}.jpg".format(i))
picam2.stop()
print("Save ldr_{:02d}.jpg success".format(i))
