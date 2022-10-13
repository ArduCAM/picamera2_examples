from picamera2 import Picamera2, Preview
import time
# from picamera2.controls import Controls

picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(main={"size": (2560, 720)})
# capture_config = picam2.create_still_configuration(main={"size": (1280, 720), "format": "RGB888"},)
# picam2.set_controls({"FrameDurationLimits":(200,1000)})
# capture_config.FrameDurationLimits = (100,100)
# ctrls = picam2.controls(pic/am2)

picam2.configure(preview_config)

picam2.start_preview(Preview.QTGL)

FrameRate = 37
frame_time = 1000000 // FrameRate 

picam2.start()
picam2.set_controls({"FrameDurationLimits":(frame_time,frame_time)})


print(picam2.controls)
time.sleep(20)
