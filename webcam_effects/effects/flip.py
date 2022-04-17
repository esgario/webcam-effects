import cv2

def apply(image, cfg, horizontal=False, vertical=False):
    if horizontal and vertical:
        image = cv2.flip(image, -1)
    elif horizontal:
        image = cv2.flip(image, 1)
    elif vertical:
        image = cv2.flip(image, 0)
    return image
    