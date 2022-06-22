import cv2
from webcam_effects.utils.pipeline import PipelineStep
from webcam_effects.effects.models.portrait_segmentation import PortraitSegmentation


class Effect(PipelineStep):
    def __init__(self, kernel_size=5, dilate=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ks = kernel_size
        self.dilate = dilate
        self.model = PortraitSegmentation()

    def handle_message(self, frame):
        if hasattr(self.ks, "__len__") and len(self.ks) == 2:
            kernel = self.ks
        else:
            kernel = (self.ks, self.ks)

        mask = self.model.predict(frame, kernel, self.dilate)
        background = cv2.blur(frame, kernel)

        yield frame * mask + background * (1 - mask)
