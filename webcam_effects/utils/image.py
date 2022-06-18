import cv2
import numpy as np


def normalize_image(
    frame, mean=(102.9, 111.3, 126.9), std=(62.9, 62.8, 66.4), shape=(320, 320)
):
    """Normalizes image before inference."""
    h, w = shape

    mean = np.array(mean, dtype=np.float32)
    std = np.array(std, dtype=np.float32)

    frame = cv2.resize(frame, (h, w))
    frame = frame.astype(np.float32)

    # Normalize and add batch dimension
    img = frame
    img = (img - mean) / std
    img /= 255.0
    img = img.transpose((2, 0, 1))
    img = img[np.newaxis, ...]

    return img
