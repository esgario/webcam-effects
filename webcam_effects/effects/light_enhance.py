import numpy as np

from webcam_effects.utils.pipeline import PipelineStep
from webcam_effects.effects.models.light_enhancement import LightEnhancement


class Effect(PipelineStep):
    def __init__(self, level=5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.level = level
        self.model = LightEnhancement()

    def handle_message(self, frame):
        new_frame = self.model.predict(frame)
        out_frame = frame * (1 - self.level) + new_frame * self.level
        out_frame = np.clip(out_frame, 0, 255)

        yield out_frame
