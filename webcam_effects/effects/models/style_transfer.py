import os
import cv2
import numpy as np

from . import OnnxModel
from webcam_effects.utils.image import normalize_image


STYLES = {
    "mosaic": "st-mosaic.onnx",
    "pointilism": "st-pointilism.onnx",
    "udnie": "st-udnie.onnx",
    "candy": "st-candy.onnx",
    "rain-princess": "st-rain-princess.onnx",
}

def _inference(image, device, style):
    if _inference.MODEL is None or style not in _inference.MODEL.model_path:
        if style not in STYLES:
            raise ValueError("Unknown style: {}".format(style))

        model_path = os.path.join(
            './weights', STYLES.get(style, "st-mosaic.onnx"))
        model_path = './weights/st-mosaic.onnx'
        _inference.MODEL = OnnxModel(model_path, device)

    shape = image.shape[:2][::-1]
    image = normalize_image(image, shape=(224, 224))
    pred = _inference.MODEL.predict(image)[0][0]

    result = np.clip(pred, 0, 255)
    result = result.transpose(1,2,0).astype("uint8")

    return cv2.resize(result, shape)


_inference.MODEL = None


def predict(image, cfg, style):
    return _inference(image, cfg.DEVICE, style)
