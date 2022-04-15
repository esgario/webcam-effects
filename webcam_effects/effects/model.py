import cv2
import numpy as np
import onnxruntime as ort
from webcam_effects.utils.image import normalize_image


MODEL = None

class OnnxModel:

    def __init__(self, model_path, device):
        self.load_model(model_path, device)

    def _get_providers(self, device):
        providers = []
        if device.upper() == "GPU":
            providers.append('CUDAExecutionProvider')
        providers.append('CPUExecutionProvider')
        return providers

    def load_model(self, model_path, device):
        self.sess = ort.InferenceSession(model_path, providers=self._get_providers(device))
        self.input_name = self.sess.get_inputs()[0].name
        self.input_shape = self.sess.get_inputs()[0].shape
        self.output_name = self.sess.get_outputs()[0].name

    def predict(self, img):
        pred = self.sess.run(None, {self.input_name: img})
        return pred


def _inference(image, device, blur_kernel):
    global MODEL
    if MODEL is None:
        MODEL = OnnxModel('./weights/SINet.onnx', device)

    shape = image.shape[:2][::-1]
    image = normalize_image(image)
    pred = MODEL.predict(image)[0]
    mask = np.argmax(pred[0], axis=0).astype("f4")
    mask = cv2.blur(mask, blur_kernel)

    return cv2.resize(mask, shape)


def get_soft_mask(image, cfg, blur_kernel=(5, 5)):
    pred = _inference(image, cfg.DEVICE, blur_kernel)

    return pred[:, :, np.newaxis]
