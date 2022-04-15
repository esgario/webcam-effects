import cv2
from .model import get_soft_mask


def apply(image, cfg, kernel_size=5):
    if hasattr(kernel_size, '__len__') and len(kernel_size) == 2:
        kernel = kernel_size
    else:
        kernel = (kernel_size, kernel_size)

    mask = get_soft_mask(image, cfg, (5, 5))
    background = cv2.blur(image, kernel)
    ret = image * mask + background * (1 - mask)

    return ret.astype("u1")
