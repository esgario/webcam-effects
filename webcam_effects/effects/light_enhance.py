import cv2
import numpy as np

from . import EffectBase
from .models.light_enhancement import load_model, predict


class Effect(EffectBase):
    def __init__(self, level=0.2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = None
        self.level = level

    def load(self, device):
        super().load()
        self.model = load_model(device)

    def process(self, frame):
        new_frame = predict(self.model, frame)
        out_frame = frame * (1 - self.level) + new_frame * self.level
        out_frame = np.clip(out_frame, 0, 255)
        return out_frame

    def run(self, frame):
        if self.model is None:
            return frame

        out_frame = self.process(frame)

        return out_frame
