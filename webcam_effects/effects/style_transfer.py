from .models.style_transfer import predict

def apply(image, cfg, style="mosaic"):
    return predict(image, cfg, style)
    