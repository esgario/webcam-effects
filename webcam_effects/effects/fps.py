import cv2
import time
from collections import deque

times = deque(maxlen=30)


def update():
    times.append(time.time())


def get():
    fps = 0
    if len(times) >= 2:
        sec_per_frame = (times[-1] - times[0]) / len(times)
        fps = 1 / sec_per_frame
    return round(fps)


def apply(image, cfg):
    update()
    cv2.putText(
        image, f"FPS: {get()}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
        1, (255, 255, 255), 2, cv2.LINE_AA
    )
    return image
