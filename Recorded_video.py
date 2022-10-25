#!/usr/bin/python3
# Live preview, enter `r` in the terminal to start recording video
import time

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from picamera2 import Picamera2, Preview
import threading


picam2 = Picamera2()

class myThread (threading.Thread):

    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay    
    def run(self):
        if self.threadID == 1:
            self.preview()
            print(1)
        elif self.threadID == 2:
            self.keyboard_()
    def preview(self):
        global picam2
        picam2.start_preview(Preview.QTGL)
        preview_config = picam2.create_preview_configuration()
        picam2.configure(preview_config)
        picam2.start()
    def keyboard_(self):
        global picam2
        encoder = H264Encoder(10000000)
        output = FfmpegOutput('test.mp4', audio=True)
        r = input()
        if r == 'r':
            print(1)
            picam2.stop()
            video_config = picam2.create_video_configuration()
            picam2.configure(video_config)
            picam2.start_recording(encoder, output)
            time.sleep(10)
            picam2.stop_recording()

thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

thread1.start()
thread2.start()
thread1.join()
thread2.join()
