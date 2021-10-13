from .model import get_soft_mask


def remove_background(image):
    mask = get_soft_mask(image)
    ret = image * mask
    return ret.astype("u1")
