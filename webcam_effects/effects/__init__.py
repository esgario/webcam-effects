from . import bg_blur
from . import bg_remove
from . import style_transfer
from . import flip
from . import fps


EFFECTS = {
    'BG_BLUR': bg_blur,
    'BG_REMOVE': bg_remove,
    'STYLE_TRANSFER': style_transfer,
    'FLIP': flip,
    'FPS': fps
}

def apply(image, cfg):

    for effect in cfg.EFFECTS:
        assert "name" in effect, "Effect name is missing."

        if effect["name"] in EFFECTS:
            if effect.get("enable", False):
                kwargs = effect.get("args", {})
                image = EFFECTS[effect["name"]].apply(image, cfg, **kwargs)

        else:
            print("Effect '{}' not found.".format(effect))

    return image
