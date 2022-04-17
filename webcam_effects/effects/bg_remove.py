from .models.portrait_segmentation import predict


def apply(image, cfg, inverted=False, dilate=0):
    mask = predict(image, cfg, blur_kernel=(5, 5), dilate=dilate)
    if inverted:
        ret = image * (1 - mask)
    else:
        ret = image * mask
    return ret.astype("u1")
