import cv2
import numpy as np
from .models.face_detection import predict


def apply(image, cfg, text=""):
    boxes, labels, confs = predict(image, cfg)
    image = image.astype(np.float32)
    for box in boxes:
        box = [int(b) for b in box]
        cv2.rectangle(image, box[:2], box[2:], (0, 0, 255), 2)

    return image.astype("u1")
