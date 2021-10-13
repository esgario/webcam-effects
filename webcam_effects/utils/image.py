import cv2


def normalize_image(
    image,
    input_shape=(224, 300),
    mean=(0.485, 0.456, 0.406),
    std=(0.229, 0.224, 0.225)
):
    """Normalizes image before inference."""
    image = cv2.resize(image, input_shape[::-1])
    image = image.astype("f4") / 255.0
    image = (image - mean) / std
    return image.astype("f4")
