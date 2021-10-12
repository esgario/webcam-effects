import os
from .defaults import _C as cfg

CFG_PATH = "config.yaml"

def load_config():
    """Load the config file."""
    try:
        cfg_mtime = os.stat(CFG_PATH).st_mtime
        if cfg_mtime != load_config.last_cfg_mtime:
            print("Updating config.")
            cfg.merge_from_file(CFG_PATH)
            load_config.last_cfg_mtime = cfg_mtime
    except OSError:
        pass

load_config.last_cfg_mtime = None
load_config()