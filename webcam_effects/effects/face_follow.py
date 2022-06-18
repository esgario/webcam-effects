import cv2
import numpy as np

from . import EffectBase
from .models.face_detection import load_model, predict


class Effect(EffectBase):
    def __init__(self, scale=0.8, filter=0.8, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = None
        self.scale = scale
        self.filter = filter
        self.last_center = np.array((320, 640)).astype(int)

    def load(self, device):
        super().load()
        self.model = load_model(device)

    def process(self, frame):
        shape = np.array(frame.shape).astype(float)
        cs = ((shape[:2] * self.scale) / 2).astype(int)

        boxes, _, _ = predict(self.model, frame)
        best_area = 0
        if len(boxes):
            best_box = boxes[0]
            for box in boxes:
                area = np.prod(box[2:] - box[:2])
                if area > best_area:
                    best_area = area
                    best_box = box

            c = (best_box[:2] + best_box[2:]) / 2
            c = c * (1 - self.filter) + self.last_center * self.filter
            self.last_center = c
        else:
            c = self.last_center

        c = c.astype(int)[::-1]
        c[0] = min(max(cs[0], c[0]), shape[0] - cs[0])
        c[1] = min(max(cs[1], c[1]), shape[1] - cs[1])

        crop = frame[c[0] - cs[0] : c[0] + cs[0], c[1] - cs[1] : c[1] + cs[1]]
        frame = cv2.resize(crop, np.array(shape[:2][::-1]).astype(int))

        return frame

    def run(self, frame):
        if self.model is None:
            return frame

        out_frame = self.process(frame)

        return out_frame
