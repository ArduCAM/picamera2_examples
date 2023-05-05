#!/usr/bin/python3

import time
import subprocess
from picamera2 import Picamera2, Preview

def run_cmd(cmd):
    """
    Method for running the command line.
    """
    print(f'{cmd}')
    try:
        result = subprocess.run(cmd, universal_newlines=True, check=False, shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(result.stdout)
        print("Set up successfully.")
    except RuntimeError as error:
        print(f'Error: {error}')
    else:
        print("Set up error!")

SET_TRIGGRT_MODE = "v4l2-ctl -d /dev/v4l-subdev0 -c trigger_mode=0"
run_cmd(SET_TRIGGRT_MODE)


picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)

preview_config = picam2.create_preview_configuration()
picam2.configure(preview_config)
picam2.start()
time.sleep(5)
