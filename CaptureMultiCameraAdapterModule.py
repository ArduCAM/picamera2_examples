#!/usr/bin/python3

from picamera2 import Picamera2, Preview
import time

for i in range(4):
    """
        Only one camera can be turned on at a time, and four cameras cannot be turned on at the same time.
        If you need to switch cameras, you need to close the last opened camera first 'picam2.close()'.
    """
    picam2 = Picamera2(camera_num=i)

    capture_config = picam2.create_still_configuration(main={"format": 'RGB888', "size": (1920, 1080)})
    picam2.configure(capture_config)

    picam2.start()
    RGB888 = picam2.capture_array("main")
    picam2.switch_mode_and_capture_file(capture_config, "camera_{}.jpg".format(i))
    picam2.stop()
    picam2.close()
    print("Camera {} save picture success".format(i))
