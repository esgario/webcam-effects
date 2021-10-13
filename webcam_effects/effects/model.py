import cv2
import numpy as np
import tensorflow as tf
from webcam_effects.utils.image import normalize_image

gpu_devices = tf.config.experimental.list_physical_devices("GPU")
for g in gpu_devices:
    tf.config.experimental.set_memory_growth(g, True)

MODEL = tf.keras.models.load_model(
    'weights/wce_v0.1.h5', custom_objects={'tf': tf})


def _inference(image):
    shape = image.shape[:2][::-1]
    image = normalize_image(image)
    image = image[np.newaxis, ...]
    pred = MODEL.predict(image)[0]
    return cv2.resize(pred[:, :, -1], shape)


def get_soft_mask(image):
    pred = _inference(image)
    return pred[:, :, np.newaxis]
