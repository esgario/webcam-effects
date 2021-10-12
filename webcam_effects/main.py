import time
import cv2
import numpy as np
from webcam_effects.webcam import get_devices
from webcam_effects.configs import cfg, load_config

blue = np.zeros((480,640,3), dtype=np.uint8)
blue[:,:,2] = 255

red = np.zeros((480,640,3), dtype=np.uint8)
red[:,:,0] = 255

real_cam = None
virtual_cam = None


def loop():
    load_config()
    frame = real_cam.get_frame()
    virtual_cam.schedule_frame(frame)


def init():
    global real_cam, virtual_cam
    real_cam, virtual_cam = get_devices(cfg)

    print("Starting WebCam Effects.")



def main():
    init()
    while True:
        try:
            loop()
        except KeyboardInterrupt:
            print("Stopping.")
            break
    