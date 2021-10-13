import time
from collections import deque

times = deque(maxlen=30)


def update_fps():
    times.append(time.time())


def get_fps():
    fps = 0
    if len(times) >= 2:
        sec_per_frame = (times[-1] - times[0]) / len(times)
        fps = 1 / sec_per_frame
    return fps
