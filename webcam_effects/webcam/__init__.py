import cv2
from pyfakewebcam import FakeWebcam
from webcam_effects.configs import cfg


class RealWebcam():
    def __init__(self, cfg):
        self._cam = cv2.VideoCapture(cfg.VIDEO_DEVICE.REAL)
        if not self._cam.set(cv2.CAP_PROP_BUFFERSIZE, 1):
            print('Failed to reduce capture buffer size.')
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self._cam.set(cv2.CAP_PROP_FOURCC, fourcc)
        self._cam.set(cv2.CAP_PROP_FRAME_WIDTH, cfg.IMAGE_WIDTH)
        self._cam.set(cv2.CAP_PROP_FRAME_HEIGHT, cfg.IMAGE_HEIGHT)
        cfg.IMAGE_WIDTH = int(self._cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        cfg.IMAGE_HEIGHT = int(self._cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def get_frame(self):
        _, frame = self._cam.read()
        # BRG to RGB
        return frame[..., ::-1]


def get_devices(cfg):
    real_cam = RealWebcam(cfg)
    virtual_cam = FakeWebcam(cfg.VIDEO_DEVICE.VIRTUAL, cfg.IMAGE_WIDTH, cfg.IMAGE_HEIGHT)
    return real_cam, virtual_cam
