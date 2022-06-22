import cv2
import numpy as np

from webcam_effects.utils.pipeline import PipelineStep
from webcam_effects.effects.models.face_detection import FaceFollow


class Effect(PipelineStep):
    def __init__(self, scale=0.8, filter=0.8, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale = scale
        self.filter = filter
        self.model = FaceFollow()
        self.last_center = np.array((320, 640)).astype(int)

    def handle_message(self, frame):
        shape = np.array(frame.shape).astype(float)
        cs = ((shape[:2] * self.scale) / 2).astype(int)

        boxes, _, _ = self.model.predict(frame)
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

        yield frame
