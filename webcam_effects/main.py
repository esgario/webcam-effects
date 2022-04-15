
from webcam_effects.configs import cfg, load_config
from webcam_effects.utils import fps
from webcam_effects import webcam
from webcam_effects import effects

real_cam = None
virtual_cam = None
effects_list = None


def loop():
    load_config()

    frame = real_cam.get_frame()
    frame = effects.apply(frame, effects_list)

    if cfg.SHOW_FPS:
        frame = fps.print(frame)
        fps.update()

    virtual_cam.schedule_frame(frame)


def init():
    global real_cam, virtual_cam, effects_list
    real_cam, virtual_cam = webcam.get_devices(cfg)
    effects_list = effects.get(cfg)

    print("Starting WebCam Effects.")


def main():
    init()
    while True:
        try:
            loop()
        except KeyboardInterrupt:
            print("Stopping.")
            break
