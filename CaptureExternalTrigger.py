import cv2
from datetime import datetime
import subprocess
import signal
import os
import queue
import RPi.GPIO as GPIO
import time
import threading
from picamera2 import Picamera2, Preview

# Flag for stopping threads
stop_threads = False

# Command for opening and closing trigger mode
open_trigger_mode = "v4l2-ctl -d /dev/v4l-subdev0 -c trigger_mode=1"
close_trigger_mode = "v4l2-ctl -d /dev/v4l-subdev0 -c trigger_mode=0"
# Queue for storing captured images
image_queue = queue.Queue(maxsize=100)

Semaphore = threading.Semaphore(1)

# Lock for thread synchronization
lock = threading.Lock()

# Function for handling keyboard interrupt signal
def signal_handler(sig, frame):
    global stop_threads
    stop_threads = True
    os._exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

# Function for running a command in the shell
def run_cmd(cmd):
    print(f'{cmd}')
    try:
        subprocess.run(cmd, universal_newlines=True, check=False, shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except RuntimeError as e:
        print(f'Error: {e}')
    except:
        print("Set up error!")

# Close the trigger mode before starting the program
run_cmd(close_trigger_mode)

# Class for controlling GPIO pins
class GPIOModule():
    def __init__(self):
        self.ledPin = 3 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ledPin, GPIO.OUT)
        self.index_flag = True
        global stop_threads
                                                                                                                            
    def run(self):
        # Wait for 3 seconds before starting the trigger
        time.sleep(3)
        print("Start Trigger! Press CTRL+C to exit")
        while True:
            time.sleep(0.2)
            try:
                val = input("enter your trig num: ")
                index = int(val)
                self.index_flag = True
            except:
                self.index_flag = False

            if self.index_flag:
                while index:
                    index-=1
                    GPIO.output(self.ledPin, GPIO.HIGH)
                    time.sleep(0.001)
                    GPIO.output(self.ledPin, GPIO.LOW)
                    time.sleep(0.030)
                    time.sleep(0.1)

# Class for controlling the camera
class CameraModule():
        
    def run(self):
        # Initialize the Picamera2 object
        picam2 = Picamera2()
        # Disable preview to save resources
        picam2.start_preview(Preview.NULL)
        # Create a still configuration and configure the camera
        capture_config = picam2.create_still_configuration()
        picam2.configure(capture_config)
        # Start the camera
        picam2.start()

        # Wait for 2 seconds before opening the trigger mode
        time.sleep(2)
        run_cmd(open_trigger_mode)
        time.sleep(1)

        # Keep capturing images and add them to the queue
        while True:
            image = None
            try:
                image = picam2.capture_array("main")
                if image is not None:
                    image_queue.put(image)
                    print("Add image to queue.")
                    Semaphore.release()
            except Exception as e:
                print(e)

class myThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.camera_module = CameraModule()
        self.gpio_module = GPIOModule()

    def run(self):
        if self.threadID == 1:
            self.camera_module.run()
        if self.threadID == 2:
            self.gpio_module.run()

# Thread for saving images
class SaveImageThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        while not stop_threads:
            Semaphore.acquire()
            if not image_queue.empty():
                image = image_queue.get()
                cv2.imwrite("{}.jpg".format(datetime.now()), cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

if __name__ == '__main__':
    # Create and start the threads
    thread1 = SaveImageThread()
    thread1.start()
    thread2 = myThread(1, "Thread-Camera")
    thread3 = myThread(2, "Thread-GPIO")
    thread2.start()
    thread3.start()
    # Wait for the threads to complete
    thread2.join()
    thread3.join()
