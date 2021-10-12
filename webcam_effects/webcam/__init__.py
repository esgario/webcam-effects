import cv2
from numpy.lib.type_check import real
import pyfakewebcam


class RealCam():
    def __init__(self, cfg):
        self._cam = cv2.VideoCapture(cfg.VIDEO_DEVICE.REAL)

    def get_frame(self):
        _, frame = self._cam.read()
        # BRG to RGB
        return frame[...,::-1]

def get_devices(cfg):
    real_cam = RealCam(cfg)
    virtual_cam = pyfakewebcam.FakeWebcam(cfg.VIDEO_DEVICE.VIRTUAL, 640, 480)
    return real_cam, virtual_cam