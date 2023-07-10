import time
import cv2
from picamera2 import Picamera2

picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(main={"size": (4656, 3496)})
picam2.configure(preview_config)

FRAME_RATE = 9
FRAME_RATE = 1000000 // FRAME_RATE

picam2.start()
picam2.set_controls({"FrameDurationLimits":(FRAME_RATE,FRAME_RATE)})

save_picture_list = []
for i in range(2):
    save_picture_list.append(picam2.capture_array())

for i in range(len(save_picture_list)):
    cv2.imwrite("test_{}.jpg".format(i), save_picture_list[i])
    print("Save picture {} success.".format(i))

picam2.close()
