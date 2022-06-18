import signal
import threading
import pypeln.thread as pl

from queue import Queue
from importlib import import_module

from webcam_effects.configs import cfg, load_config
from webcam_effects import webcam


real_cam = None
virtual_cam = None
effects_list = None


def read_frames(Q, e):
    while not e.is_set():
        frame = real_cam.get_frame()
        if not Q.full():
            Q.put(frame)


def get_frame_iterable(Q, e):
    while not e.is_set():
        if load_config():
            break
        yield Q.get().astype("f4")


def schedule_frame(frame):
    virtual_cam.schedule_frame(frame.astype("u1"))


def init():
    global real_cam, virtual_cam, effects_list
    real_cam, virtual_cam = webcam.get_devices(cfg)
    print("Starting WebCam Effects.")


def main():
    init()
    try:
        Q = Queue(maxsize=2)
        kill_event = threading.Event()
        thread = threading.Thread(target=read_frames, args=(Q, kill_event), daemon=True)
        thread.start()

        while True:
            stage = get_frame_iterable(Q, kill_event)
            for effect in cfg.EFFECTS:
                try:
                    if effect.get("enable", True):
                        kwargs = effect.get("args", {})
                        eff_mod = import_module(
                            f"webcam_effects.effects.{effect['name'].lower()}"
                        )
                        eff_obj = eff_mod.Effect(**kwargs)
                        stage = pl.map(eff_obj, stage, maxsize=2)
                except Exception:
                    print("Failed to load effect: {}".format(effect))

            list(pl.map(schedule_frame, stage, maxsize=2))

    except KeyboardInterrupt:
        print("Stopping.")
        kill_event.set()
        thread.join()
