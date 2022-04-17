import cv2
import numpy as np

from . import OnnxModel
from webcam_effects.utils.image import normalize_image


def _inference(image, device, blur_kernel, dilate):
    if _inference.MODEL is None:
        _inference.MODEL = OnnxModel('./weights/portrait-seg.onnx', device)

    shape = image.shape[:2][::-1]
    image = normalize_image(image)
    pred = _inference.MODEL.predict(image)[0]
    mask = np.argmax(pred[0], axis=0).astype("f4")
    mask = cv2.blur(mask, blur_kernel)

    if dilate:
        kernel = np.ones((dilate,) * 2, np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=1)

    return cv2.resize(mask, shape)

_inference.MODEL = None


def predict(image, cfg, blur_kernel=(5, 5), dilate=0):
    pred = _inference(image, cfg.DEVICE, blur_kernel, dilate)
    return pred[:, :, np.newaxis]
