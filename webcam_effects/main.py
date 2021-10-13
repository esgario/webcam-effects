import time
import cv2
import numpy as np
from webcam_effects.webcam import get_devices
from webcam_effects.configs import cfg, load_config
from webcam_effects.effects import get_effects, apply_effects
from webcam_effects.utils import fps as fps_utils

real_cam = None
virtual_cam = None
effects = None


def loop():
    load_config()
    frame = real_cam.get_frame()
    frame = apply_effects(frame, effects)
    virtual_cam.schedule_frame(frame)
    fps_utils.update_fps()
    fps = fps_utils.get_fps()
    print(fps)


def init():
    global real_cam, virtual_cam, effects
    real_cam, virtual_cam = get_devices(cfg)
    effects = get_effects(cfg)

    print("Starting WebCam Effects.")


def main():
    init()
    while True:
        try:
            loop()
        except KeyboardInterrupt:
            print("Stopping.")
            break
