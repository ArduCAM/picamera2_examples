import RPi.GPIO as GPIO
import time
import threading
import cv2
import os
from picamera2 import Picamera2
from picamera2.controls import Controls
import subprocess


def run_cmd(cmd):
    print(f'{cmd}')
    try:
        subprocess.run(cmd, universal_newlines=True, check=False, shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except RuntimeError as e:
        print(f'Error: {e}')
    except:
        print("Set up error!")

stop_threads = False
single_trigger = False
picture_num = 1
RGB888 = None
set_trigger_mode = "v4l2-ctl -d /dev/v4l-subdev0 -c trigger_mode=1"

class myThread (threading.Thread):

    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay

        self.stop_threads_picture = False

    def run(self):
        if self.threadID == 1:
            self.gpio(self.name, self.delay)
        if self.threadID == 2:
            self.picture(self.name, self.delay)
        if self.threadID == 3:
            self.key(self.name, self.delay)

    def gpio(self, threadName, delay):

        global RGB888
        global picture_num
        global single_trigger

        ledPin = 3 
        GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
        GPIO.setup(ledPin, GPIO.OUT) # LED pin set as output

        # Initial state for LEDs:
        GPIO.output(ledPin, GPIO.LOW)

        print("Start Trigger! Press CTRL+C to exit")
        while 1:

            if stop_threads == False:
                GPIO.output(ledPin, GPIO.HIGH)
                time.sleep(0.001)
                GPIO.output(ledPin, GPIO.LOW)
                time.sleep(0.060)
            elif single_trigger == True:
                RGB888 = None
                GPIO.output(ledPin, GPIO.HIGH)
                time.sleep(0.001)
                GPIO.output(ledPin, GPIO.LOW)
                time.sleep(0.030)
                try:
                    cv2.imwrite("arducam_picature_{}.jpg".format(picture_num), RGB888)
                    picture_num += 1
                    print("Save image sucessful")
                except:
                    print("Failure!")
                single_trigger = False
                # GPIO.cleanup()

    def picture(self, threadName, delay):

        global RGB888
        global picture_num
        global stop_threads
        global single_trigger

        picam2 = Picamera2()
#         ctrls = Controls(picam2)
#         ctrls.ExposureTime = 10000000
#         picam2.set_controls(ctrls)
        picam2.start()

        run_cmd(set_trigger_mode)

        while 1:

            RGB888 = picam2.capture_array("main")    
            
            if self.stop_threads_picture:
                os._exit(0)
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                self.stop_threads_picture = True
            elif key & 0xFF == ord('f'):
                stop_threads = True
            elif key & 0xFF == ord('s'):
                cv2.imwrite("arducam_picature_{}.jpg".format(picture_num), RGB888)
                picture_num += 1
                print("Save image sucessful")

            cv2.imshow("test", RGB888)

    def key(self, threadName, delay):

        global single_trigger
        global stop_threads
        
        while 1:
            keyvalue = input()
            if keyvalue == "trigger_mode":
                print("trigger_mode start")
            elif keyvalue == "open":
                stop_threads = False
            elif keyvalue == "single_trigger":
                single_trigger = True
            elif keyvalue == "quit":
                os._exit(0)
            else:
                print("This is not a valid input")

thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)
thread3 = myThread(3, "Thread-2", 3)

thread1.start()
thread2.start()
thread3.start()
thread1.join()
thread2.join()
thread3.join()
