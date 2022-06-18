import cv2
import numpy as np

from . import OnnxModel
from webcam_effects.utils.image import normalize_image


def load_model(device):
    return OnnxModel("./weights/portrait-seg.onnx", device)


def predict(model, frame, blur_kernel=(5, 5), dilate=0):
    shape = frame.shape[:2][::-1]
    frame = normalize_image(frame)
    pred = model.predict(frame)[0]
    mask = np.argmax(pred[0], axis=0).astype("f4")
    mask = cv2.blur(mask, blur_kernel)

    if dilate:
        kernel = np.ones((dilate,) * 2, np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=1)

    pred = cv2.resize(mask, shape)

    return pred[:, :, np.newaxis]
