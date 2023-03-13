#!/usr/bin/python3

import time

from picamera2 import Picamera2, Preview

i = 0
FrameRate = 2.7
frame_time = 1000000 // FrameRate 

start = time.time()

picam2 = Picamera2()
# picam2.start_preview(Preview.QTGL)

capture_config = picam2.create_still_configuration(main={"format": 'RGB888', "size": (9152, 6944)})
picam2.configure(capture_config)

# picam2.set_controls({"FrameDurationLimits":(frame_time, frame_time)})
picam2.start()

open_camera_time = time.time()
print("open time:" + str(open_camera_time -start))

while True:
    last_photo_time = time.time()
    picam2.capture_array("main")
    photo_time = time.time()
    print("picture {} take time: {}".format(i, photo_time - last_photo_time))

    i += 1
