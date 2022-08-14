import cv2

from webcam_effects.utils.pipeline import PipelineStep


class Effect(PipelineStep):
    def __init__(self, alpha=1, beta=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alpha = alpha
        self.beta = beta

    def handle_message(self, frame):
        frame = cv2.convertScaleAbs(frame, alpha=self.alpha, beta=self.beta)

        yield frame
