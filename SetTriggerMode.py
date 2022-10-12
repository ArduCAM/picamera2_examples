#!/usr/bin/python3

import time

from picamera2 import Picamera2, Preview

import subprocess


def run_cmd(cmd):
    print(f'{cmd}')
    try:
        p = subprocess.run(cmd, universal_newlines=True, check=False, shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(p.stdout)
        print("Set up successfully.")
    except RuntimeError as e:
        print(f'Error: {e}')
    except:
        print("Set up error!")

set_trigger_mode = "v4l2-ctl -d /dev/v4l-subdev0 -c trigger_mode=0"
run_cmd(set_trigger_mode)


picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)

preview_config = picam2.create_preview_configuration()
picam2.configure(preview_config)
picam2.start()
time.sleep(5)
