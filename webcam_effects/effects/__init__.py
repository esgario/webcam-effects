from . import bg_blur
from . import bg_remove


EFFECTS = {
    'BG_BLUR': bg_blur,
    'BG_REMOVE': bg_remove
}

def apply(image, cfg):

    for effect in cfg.EFFECTS:
        assert "name" in effect, "Effect name is missing."

        if effect["name"] in EFFECTS:
            kwargs = effect.get("args", {})
            image = EFFECTS[effect["name"]].apply(image, cfg, **kwargs)

        else:
            print("Effect '{}' not found.".format(effect))

    return image
