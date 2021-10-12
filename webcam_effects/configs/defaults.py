from yacs.config import CfgNode as CN

_C = CN()

_C.VIDEO_DEVICE = CN()

# Real video device path
_C.VIDEO_DEVICE.REAL = ""

# Virtual video device path
_C.VIDEO_DEVICE.VIRTUAL = ""