from .model import get_soft_mask


def apply(image, cfg):
    mask = get_soft_mask(image, cfg, blur_kernel=(5, 5))
    ret = image * mask
    return ret.astype("u1")
