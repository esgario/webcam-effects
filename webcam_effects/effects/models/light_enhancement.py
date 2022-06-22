import cv2
import numpy as np

from webcam_effects.configs import cfg
from webcam_effects.effects.models import OnnxModel


class LightEnhancement(OnnxModel):
    def __init__(self):
        super().__init__("./weights/sci_512x512.onnx", cfg.DEVICE)

    def predict(self, frame):
        input_shape = frame.shape

        frame = cv2.resize(frame, (512, 512))
        frame = frame / 255.0
        frame = frame.transpose((2, 0, 1))
        frame = frame[np.newaxis, ...]

        pred = self._predict(frame)
        output_frame = np.squeeze(pred[0])
        output_frame = output_frame.transpose(1, 2, 0)
        output_frame = output_frame * 255.0
        output_frame = cv2.resize(output_frame, input_shape[:2][::-1])

        return output_frame
