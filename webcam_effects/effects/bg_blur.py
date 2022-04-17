import cv2
from .models.portrait_segmentation import predict


def apply(image, cfg, kernel_size=5, dilate=0):
    if hasattr(kernel_size, '__len__') and len(kernel_size) == 2:
        kernel = kernel_size
    else:
        kernel = (kernel_size, kernel_size)

    mask = predict(image, cfg, (5, 5), dilate=dilate)
    background = cv2.blur(image, kernel)
    ret = image * mask + background * (1 - mask)

    return ret.astype("u1")
