from . import EffectBase
from .models.portrait_segmentation import load_model, predict


class Effect(EffectBase):
    def __init__(self, kernel_size=5, dilate=0, inverted=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = None
        self.ks = kernel_size
        self.dilate = dilate
        self.inverted = inverted

    def load(self, device):
        super().load()
        self.model = load_model(device)

    def process(self, frame):
        if hasattr(self.ks, "__len__") and len(self.ks) == 2:
            kernel = self.ks
        else:
            kernel = (self.ks, self.ks)

        mask = predict(self.model, frame, kernel, self.dilate)
        if self.inverted:
            mask = 1 - mask

        return frame * mask

    def run(self, frame):
        if self.model is None:
            return frame

        out_frame = self.process(frame)

        return out_frame
