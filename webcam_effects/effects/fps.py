import cv2
import time
from collections import deque

from webcam_effects.utils.pipeline import PipelineStep


class Effect(PipelineStep):
    def __init__(
        self, flip=True, scale=1.25, thickness=8, color=(255, 0, 0), *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.times = deque(maxlen=10)
        self.flip = flip
        self.scale = scale
        self.thickness = thickness
        self.color = color

    def _update_fps(self):
        self.times.append(time.time())

    def _get_fps(self):
        fps = 0
        if len(self.times) >= 2:
            sec_per_frame = (self.times[-1] - self.times[0]) / len(self.times)
            fps = 1 / sec_per_frame

        return round(fps)

    def _draw_text(self, frame):
        cv2.putText(
            frame,
            f"FPS: {self._get_fps()}",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            self.scale,
            self.color,
            self.thickness,
            cv2.LINE_AA,
        )

    def handle_message(self, frame):
        self._update_fps()
        if self.flip:
            frame = cv2.flip(frame, 1)
        self._draw_text(frame)
        if self.flip:
            frame = cv2.flip(frame, 1)

        yield frame
