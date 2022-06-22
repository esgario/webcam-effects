import cv2

from webcam_effects.utils.pipeline import PipelineStep


class Effect(PipelineStep):
    def __init__(self, kernel_size=9, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kernel_size = kernel_size

    def handle_message(self, frame):
        frame = cv2.bilateralFilter(frame, self.kernel_size, 75, 75)

        yield frame
