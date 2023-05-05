#!/usr/bin/python3

import cv2
import sys
import argparse
from picamera2 import Picamera2
import subprocess
import time

def run_cmd(cmd):
    # print(f'{cmd}')
    try:
        subprocess.run(cmd, universal_newlines=True, check=False, shell=True,
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except RuntimeError as e:
        print(f'Error: {e}')
    except:
        print("Set up error!")


cv2.startWindowThread()
width = 640
height = 480
sub_image_num = 2
sub_height = height // sub_image_num
sub_width = width // sub_image_num

sub_images = []
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (width, height)}))
picam2.start()

im = picam2.capture_array()

for i in range(4):
    cv2.namedWindow(str(i),cv2.WINDOW_NORMAL)

while True:
    src = picam2.capture_array()
    sub_images = []
    for j in range(sub_image_num):
        for i in range(sub_image_num):
            if j < sub_image_num - 1 and i < sub_image_num - 1:
                image_roi = src[j * sub_height: (j + 1) * sub_height, i * sub_width: (i + 1) * sub_width, :]
            elif j < sub_image_num - 1:
                image_roi = src[j * sub_height: (j + 1) * sub_height, i * sub_width:, :]
            elif i < sub_image_num - 1:
                image_roi = src[j * sub_height:, i * sub_width: (i + 1) * sub_width, :]
            else:
                image_roi = src[j * sub_height:, i * sub_width:, :]
            sub_images.append(image_roi)

    for i, img in enumerate(sub_images):
        cv2.imshow(str(i), img)
