
from nms import nms
import numpy as np

from . import OnnxModel
from webcam_effects.utils.image import normalize_image


def _inference(image, device):
    if _inference.MODEL is None:
        _inference.MODEL = OnnxModel('./weights/face-det.onnx', device)

    input_shape = image.shape[:2]
    image = normalize_image(
        image,
        mean=(127, 127, 127),
        std=(0.5, 0.5, 0.5),
        shape=(640, 480)
    )
    pred = _inference.MODEL.predict(image)
    boxes, labels, confs = postprocessing(pred, input_shape)
    keep = nms.boxes(boxes, confs, confidence_threshold=0.5)
    boxes, labels, confs = [
        field[keep] for field in [
            boxes, labels, confs
        ]
    ]

    return boxes, labels, confs

_inference.MODEL = None


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


def predict(image, cfg):
    return _inference(image, cfg.DEVICE)
