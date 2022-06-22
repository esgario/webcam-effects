import cv2
import numpy as np

from webcam_effects.configs import cfg
from webcam_effects.effects.models import OnnxModel
from webcam_effects.utils.image import normalize_image


class PortraitSegmentation(OnnxModel):
    def __init__(self):
        super().__init__("./weights/portrait-seg.onnx", cfg.DEVICE)

    def predict(self, frame, blur_kernel=(5, 5), dilate=0):

        shape = frame.shape[:2][::-1]
        frame = cv2.resize(frame, (320, 320))
        frame = normalize_image(frame)
        pred = self._predict(frame)[0]
        mask = np.argmax(pred[0], axis=0).astype("f4")
        mask = cv2.blur(mask, blur_kernel)

        if dilate:
            kernel = np.ones((dilate,) * 2, np.uint8)
            mask = cv2.dilate(mask, kernel, iterations=1)

        pred = cv2.resize(mask, shape)

        return pred[:, :, np.newaxis]
