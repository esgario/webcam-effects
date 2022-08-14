import abc
import onnxruntime as ort


class OnnxModel(abc.ABC):
    def __init__(self, model_path, device):
        self.model_path = model_path
        self.device = device
        self.load_model()

    def _get_providers(self, device):
        providers = []
        if device.upper() == "GPU":
            providers.append("CUDAExecutionProvider")
        providers.append("CPUExecutionProvider")
        return providers

    def load_model(self):
        opts = ort.SessionOptions()
        opts.inter_op_num_threads = 2
        opts.intra_op_num_threads = 2
        self.sess = ort.InferenceSession(
            self.model_path,
            providers=self._get_providers(self.device),
            sess_options=opts,
        )
        self.input_name = self.sess.get_inputs()[0].name
        self.input_shape = self.sess.get_inputs()[0].shape
        self.output_name = self.sess.get_outputs()[0].name

    def _predict(self, img):
        pred = self.sess.run(None, {self.input_name: img})
        return pred

    @abc.abstractmethod
    def predict(self, *args, **kwargs):
        pass
