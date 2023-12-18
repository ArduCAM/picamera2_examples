# Picamera2_example
Some picamera2 use cases

The official picamera2 examples are not comprehensive, and all additional examples are based on the arducam camera.

If you want to use it, please install the relevant dependencies according to the link below: <br>
https://www.arducam.com/docs/cameras-for-raspberry-pi/picamera2-with-arducam-v1-v2-hq-16mp-af-64mp-af-pivariety-cameras-guide/

```
wget -O install_pivariety_pkgs.sh https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver/releases/download/install_script/install_pivariety_pkgs.sh 
chmod +x install_pivariety_pkgs.sh
./install_pivariety_pkgs.sh -p libcamera_dev
./install_pivariety_pkgs.sh -p libcamera_apps
sudo apt install -y python3-kms++
sudo apt install -y python3-pyqt5
sudo apt install -y python3-prctl 
sudo apt install -y libatlas-base-dev 
sudo apt install -y ffmpeg
sudo apt install -y python3-pip
sudo pip3 install numpy --upgrade
```
