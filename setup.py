#!/usr/bin/env python
from setuptools import find_packages, setup

requirements = [
    "pyfakewebcam==0.1.0",
    "yacs==0.1.8",
    "onnxruntime-gpu==1.10.0",
    "opencv-python==4.5.5.64",
    "nms==0.1.6",
]


setup(
    name="WebCam Effects",
    entry_points=dict(console_scripts=["wce=webcam_effects.main:main"]),
    version="0.0.2",
    description="WebCam Effects",
    author="Guilherme Esgario",
    packages=find_packages(),
    install_requires=requirements,
)
