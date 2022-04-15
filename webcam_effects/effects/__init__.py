from . import model
from .bg_remove import apply as bg_remove


def get(cfg):
    effects = []
    effects.append(bg_remove)
    return effects


def apply(image, effects):
    for func in effects:
        image = func(image)
    return image
