from .utils import *


class Model:
    def __init__(self, model_config, use_gpu=True):

        """
        Holds a neural net and its pre-trained weights

        Args:
            model_config: paths to a pre-trained model
            use_gpu (bool): state if gpu shall be used for predictions with this model
        """
        assert isinstance(model_config, ModelConfiguration)
        self.model_config = model_config
        self.use_gpu = use_gpu
        self.net, self.transformer, self.labels = self._load_model()

    def _load_model(self):

        """
        Loads a neural net and its pre-trained weights

        Returns:
            [net, transformer, labels]: the caffe net; a caffe transformer object and the corresponding labels

        """
        config = self.model_config
        net = get_net(config.caffemodel, config.deploy_file, self.use_gpu)
        transformer = get_transformer(net.blobs['data'].data.shape, config.mean_file)
        labels = read_labels(config.labels_file)

        return net, transformer, labels


class ModelConfiguration:
    @property
    def deploy_file(self):
        return self._deploy_file

    @property
    def caffemodel(self):
        return self._caffemodel

    @property
    def labels_file(self):
        return self._labels_file

    @property
    def mean_file(self):
        return self._mean_file

    def __init__(self, deploy_file, caffemodel, labels_file, mean_file):
        self._deploy_file = deploy_file
        self._caffemodel = caffemodel
        self._labels_file = labels_file
        self._mean_file = mean_file
