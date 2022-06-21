import cv2
import numpy as np
from nms import nms

from . import OnnxModel
from webcam_effects.utils.image import normalize_image


def load_model(device):
    return OnnxModel("./weights/face-det.onnx", device)


def predict(model, frame):
    input_shape = frame.shape[:2]
    frame = cv2.resize(frame, (640, 480))
    frame = normalize_image(frame, mean=(127, 127, 127), std=(0.5, 0.5, 0.5))
    pred = model.predict(frame)
    boxes, labels, confs = postprocessing(pred, input_shape)
    keep = nms.boxes(boxes, confs, confidence_threshold=0.5)
    boxes, labels, confs = [field[keep] for field in [boxes, labels, confs]]

    return boxes, labels, confs


def postprocessing(out, input_shape):
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
