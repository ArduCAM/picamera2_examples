import time
import cv2
from picamera2 import MappedArray, Picamera2, Preview

cv2.startWindowThread()
picam2 = Picamera2()
config = picam2.create_still_configuration(main={"format": 'RGB888', "size": (1920, 1080)})
picam2.configure(config)
exposure_time = 2000000

picam2.set_controls({"ExposureTime": exposure_time,"AnalogueGain": 1.0})
picam2.start()
while True:
    RGB888 = picam2.capture_array("main")
    cv2.imshow("Camera", RGB888)
    cv2.waitKey(1)
picam2.stop()

cv2.destroyAllWindows()