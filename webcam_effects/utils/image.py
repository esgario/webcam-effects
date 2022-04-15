import cv2
import numpy as np

MEAN = np.array([102.890434, 111.25247, 126.91212], dtype=np.float32)
STD = np.array([62.93292, 62.82138, 66.355705], dtype=np.float32)


def normalize_image(frame):
    """Normalizes image before inference."""
    h, w = 320, 320

    frame = cv2.resize(frame, (h, w))
    frame = frame.astype(np.float32)

    # Normalize and add batch dimension
    img = frame
    img = (img - MEAN) / STD
    img /= 255
    img = img.transpose((2, 0, 1))
    img = img[np.newaxis,...]

    return img