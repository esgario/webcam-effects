import abc
from webcam_effects.configs import cfg


class EffectBase(abc.ABC):
    """Base class for all effects."""

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.loaded = False

    @abc.abstractmethod
    def run(self):
        """Run effect."""
        pass

    def load(self, *args):
        """Load any effect model."""
        self.loaded = True

    def __call__(self, frame):
        if not self.loaded:
            self.load(cfg.DEVICE)

        return self.run(frame)
