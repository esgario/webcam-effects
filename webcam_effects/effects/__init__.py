from . import model
from .remove_background import remove_background


def get_effects(cfg):
    effects = []
    effects.append(remove_background)
    return effects


def apply_effects(image, effects):
    for func in effects:
        image = func(image)
    return image
