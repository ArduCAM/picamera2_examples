#!/usr/bin/python3

import cv2
import sys
import argparse
from picamera2 import Picamera2
import subprocess
import time

def run_cmd(cmd):
    print(f'{cmd}')
    try:
        subprocess.run(cmd, universal_newlines=True, check=False, shell=True,
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except RuntimeError as e:
        print(f'Error: {e}')
    except:
        print("Set up error!")

argv = sys.argv[:]
parser = argparse.ArgumentParser()
parser.add_argument(
	"--choose", 
	# action='store_true',
    nargs = "+",
	help="Select camera"
	)
args = parser.parse_args()


picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
picam2.start()

# while True:
im = picam2.capture_array()
index = 0

if args.choose:
    for i in range(len(args.choose)):
        # print(args.choose)
        if args.choose[i] == 'a':
            # picam2.stop()
            run_cmd("i2cset -y 10 0x24 0x24 0x02")
            time.sleep(0.5)
            im = picam2.capture_array()
            cv2.imwrite("camera_a_picture_{}.jpg".format(index), im)
            print("Camera A save picture success.")
            index += 1

        if args.choose[i] == 'b':
            run_cmd("i2cset -y 10 0x24 0x24 0x12")
            time.sleep(0.5)
            im = picam2.capture_array()
            cv2.imwrite("camera_b_picture_{}.jpg".format(index), im)
            print("Camera B save picture success.")
            index += 1

        if args.choose[i] == 'c':
            run_cmd("i2cset -y 10 0x24 0x24 0x22")
            time.sleep(0.5)
            im = picam2.capture_array()
            cv2.imwrite("camera_c_picture_{}.jpg".format(index), im)
            print("Camera C save picture success.")
            index += 1

        if args.choose[i] == 'd':
            run_cmd("i2cset -y 10 0x24 0x24 0x32")
            time.sleep(0.5)
            im = picam2.capture_array()
            cv2.imwrite("camera_d_picture_{}.jpg".format(index), im)
            print("Camera D save picture success.")
            index += 1

print("The image is saved successfully and the program ends.")
