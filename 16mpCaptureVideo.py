#!/usr/bin/python3
'''
This is just a simple example. 
If you cannot accept that the Raspberry Pi hardware only supports 1080P, this example will give you an idea.
Using opencv for software encoding will have some problems, but you can optimize it according to this idea.
This example only test in Pi4, if you use other hardware, maybe have more problem.
'''

import sys
import signal
import time
import cv2
from picamera2 import Picamera2

def signal_handler(signal, frame):
    print('Program exits normally.')
    out.release()
    picam2.stop()
    print("Save video sucessful.")
    sys.exit(0)
    

signal.signal(signal.SIGINT, signal_handler)

width = 4624
height = 3472

picam2 = Picamera2()
video_config = picam2.create_still_configuration(main={"size": (width, height), "format": "RGB888"}, buffer_count=1)
picam2.configure(video_config)
fourcc = cv2.VideoWriter_fourcc(*'XVID')

picam2.start()

print("Please use ctrl c to exit the program.")
frame_count = 0
times = 3
start = time.time()
while True: 
    frame = picam2.capture_array(name="main")
    if times >= 1:
        frame_count += 1
        if time.time() - start >= 1:
            if sys.version[0] == '2':
                print("fps: {}".format(frame_count))    
            else:
                print("fps: {}".format(frame_count),end='\r')
            if times == 1:
                out = cv2.VideoWriter('output.mp4' ,fourcc, frame_count, (width, height))
            frame_count = 0
            times -= 1
            start = time.time()
    else:
        if times == 0:
            print("Start save video.")
            times -= 1
        out.write(frame)
        
