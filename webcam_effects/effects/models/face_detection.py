import cv2
import numpy as np
from nms import nms

from webcam_effects.configs import cfg
from webcam_effects.effects.models import OnnxModel
from webcam_effects.utils.image import normalize_image


class FaceFollow(OnnxModel):
    def __init__(self):
        super().__init__("./weights/face-det.onnx", cfg.DEVICE)

    def predict(self, frame):

        input_shape = frame.shape[:2]
        frame = cv2.resize(frame, (640, 480))
        frame = normalize_image(frame, mean=(127, 127, 127), std=(0.5, 0.5, 0.5))
        pred = self._predict(frame)
        boxes, labels, confs = self._postprocessing(pred, input_shape)
        keep = nms.boxes(boxes, confs, confidence_threshold=0.5)
        boxes, labels, confs = [field[keep] for field in [boxes, labels, confs]]

        return boxes, labels, confs

    def _postprocessing(self, out, input_shape):
        """Custom parser for the model output."""
        scores = out[0].squeeze()
        boxes = out[1].squeeze()

        y = np.argmax(scores, axis=1)
        idx = y > 0
        boxes = boxes[idx, :]

        boxes[:, 0] = boxes[:, 0] * input_shape[1]
        boxes[:, 1] = boxes[:, 1] * input_shape[0]
        boxes[:, 2] = boxes[:, 2] * input_shape[1]
        boxes[:, 3] = boxes[:, 3] * input_shape[0]

        labels = y[idx]
        confs = np.max(scores[idx], axis=1)

        return [boxes, labels, confs]
