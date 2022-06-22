import cv2

from webcam_effects.utils.pipeline import PipelineStep


class Effect(PipelineStep):
    def __init__(self, horizontal=False, vertical=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flip_h = horizontal
        self.flip_v = vertical

    def handle_message(self, frame):
        if self.flip_h and self.flip_v:
            frame = cv2.flip(frame, -1)
        elif self.flip_h:
            frame = cv2.flip(frame, 1)
        elif self.flip_v:
            frame = cv2.flip(frame, 0)

        yield frame
