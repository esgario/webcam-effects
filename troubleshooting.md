# Troubleshooting

## PyFakewebcam fails to start

Sometimes you can get the following error:

```
Traceback (most recent call last):
  File "/home/esgario/.virtualenvs/webcamenv/bin/wce", line 33, in <module>
    sys.exit(load_entry_point('WebCam-Effects', 'console_scripts', 'wce')())
  File "/home/esgario/Documents/Code/MyCodes/webcam-effects/webcam_effects/main.py", line 47, in main
    init_webcam()
  File "/home/esgario/Documents/Code/MyCodes/webcam-effects/webcam_effects/main.py", line 42, in init_webcam
    real_cam, virtual_cam = webcam.get_devices(cfg)
  File "/home/esgario/Documents/Code/MyCodes/webcam-effects/webcam_effects/webcam/__init__.py", line 26, in get_devices
    virtual_cam = FakeWebcam(
  File "/home/esgario/.virtualenvs/webcamenv/lib/python3.8/site-packages/pyfakewebcam/pyfakewebcam.py", line 54, in __init__
    fcntl.ioctl(self._video_device, _v4l2.VIDIOC_S_FMT, self._settings)
OSError: [Errno 22] Invalid argument
```

To fix this you can try to remove the modprobe v4l2loopback and enable it again:

```bash
$ sudo modprobe -r v4l2loopback
$ sudo modprobe v4l2loopback exclusive_caps=1 video_nr=2
```
