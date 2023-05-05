import time
from picamera2 import Picamera2, Preview

picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(main={"size": (1920, 1080)})
picam2.configure(preview_config)

picam2.start_preview(Preview.QTGL)

FRAME_RATE = 37
FRAME_RATE = 1000000 // FRAME_RATE

picam2.start()
picam2.set_controls({"FrameDurationLimits":(FRAME_RATE,FRAME_RATE)})

print(picam2.controls)
time.sleep(20)
