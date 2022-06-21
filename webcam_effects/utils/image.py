import numpy as np
import numba as nb


@nb.njit()
def normalize_image(frame, mean=(102.9, 111.3, 126.9), std=(62.9, 62.8, 66.4)):
    """Normalizes image before inference."""
    mean = np.array(mean, dtype=np.float32)
    std = np.array(std, dtype=np.float32)

    frame = frame.astype(np.float32)

    # Normalize and add batch dimension
    img = frame
    img = (img - mean) / std
    img /= 255.0
    img = img.transpose((2, 0, 1))
    img = np.expand_dims(img, 0)

    return img
