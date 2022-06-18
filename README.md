# WebCam Effects


## Requirements

Go through the following steps to get your environment up and running.
### Installation

To install the WebCam Effects module run the following command:

```bash
pip install -e .
```

obs: It has only been tested on python 3.7 but it is likely to work on other versions.

### Setup Virtual Video Device

To create the virtual video device run the following command:

```bash
sudo modprobe v4l2loopback exclusive_caps=1 video_nr=2 # creates /dev/video2
```

### Download model
The model must be downloaded to the `weights` folder:
```bash
wget -N https://www.dropbox.com/s/pxptykehvvvgcec/weights.zip && unzip -o weights.zip
```