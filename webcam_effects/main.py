from importlib import import_module

from webcam_effects.configs import cfg, load_config
from webcam_effects.utils.pipeline import Pipeline, PipelineStep
from webcam_effects import webcam


real_cam = None
virtual_cam = None
effects_list = None


class ScheduleFrame(PipelineStep):
    def __init__(self):
        PipelineStep.__init__(self)

    def handle_message(self, frame):
        virtual_cam.schedule_frame(frame.astype("u1"))
        yield None


def build_pipeline():
    steps = []
    for effect in cfg.EFFECTS:
        try:
            if effect.get("enable", True):
                kwargs = effect.get("args", {})
                eff_mod = import_module(
                    f"webcam_effects.effects.{effect['name'].lower()}"
                )
                steps.append(eff_mod.Effect(**kwargs))
        except Exception as e:
            print("Failed to load effect: {}. {}".format(effect, e))

    steps.append(ScheduleFrame())

    return Pipeline(steps)


def init_webcam():
    global real_cam, virtual_cam, effects_list
    real_cam, virtual_cam = webcam.get_devices(cfg)
    print("Starting WebCam Effects.")


def main():
    init_webcam()
    try:
        while True:
            pipeline = build_pipeline()
            pipeline.start()
            while True:
                if load_config():
                    pipeline.join()
                    break
                frame = real_cam.get_frame()
                pipeline.send_data(frame.astype("f4"))

    except KeyboardInterrupt:
        pipeline.join()
