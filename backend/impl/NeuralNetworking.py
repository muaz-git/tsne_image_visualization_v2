import impl.wincaffe.image
from impl.wincaffe.model import *
import skimage.io
from impl.wincaffe.utils import *
from time import gmtime, strftime



def create_neural_net(network_name, GPU):

    if network_name == "AlexNet":
        return AlexNet(GPU)

    elif network_name == "GoogleNet":
        return GoogleNet(GPU)

    elif network_name == "GoogleNetPlaces":
        return GoogleNetPlaces(GPU)

    elif network_name == "VGG16":
        return VGG16(GPU)

    elif network_name == "VOC_FC8s":
        return VOC_FC8s(GPU)
    else:

        print ("{} is no valid Neural Network".format(network_name))
        assert False


class NeuralNet:

    def __init__(self, caffemodel, deploy, mean, GPU):

        # Net representation
        self.net = get_net(caffemodel, deploy, GPU)

        # image transformer
        self.transformer = get_transformer(self.net.blobs['data'].data.shape, mean)

    def process_image(self, pil_image):

        image = impl.wincaffe.image.load_pil_image(pil_image)
        float_img = skimage.img_as_float(np.array(image)).astype(np.float32)

        self.process_float_image(float_img)

    def process_float_image(self, float_image):

        image_data = self.transformer.preprocess('data', float_image)
        self.net.blobs['data'].data[0] = image_data

        self.net.forward()

    def get_tensor(self, layer_name):
        tensor = self.net.blobs[layer_name].data[0].copy()
        flat_tensor = np.reshape(tensor, tensor.size)
        return flat_tensor

    def get_layer_names(self):
        layer_names = []

        all_blob_names = self.net.blobs

        for name in all_blob_names:
            layer_names.append(name)

            # # foreach layer just print the size of the tensors
            # data = self.net.blobs[name].data[0]
            # print(name)
            # print(data.shape)

        return layer_names

    def check_layer_name(self, layer_name):
        return layer_name in self.get_layer_names()

    def generate_id(self, layer):
        time_stamp = strftime("%d_%m_%Y_%H%M%S", gmtime())
        id_string = "{}_{}_{}".format(str(self), layer, time_stamp)
        return id_string


class AlexNet(NeuralNet):

    def __init__(self, GPU):

        NeuralNet.__init__(self, "impl/wincaffe/models/bvlc_alexnet/bvlc_alexnet.caffemodel",
                           "impl/wincaffe/models/bvlc_alexnet/deploy.prototxt",
                           "impl/wincaffe/datasets/ilsvrc2012/ilsvrc_2012_mean.npy", GPU)

    def __str__(self):
        return "AlexNet"


class GoogleNet(NeuralNet):

    def __init__(self, GPU):
        NeuralNet.__init__(self, "impl/wincaffe/models/bvlc_googlenet/bvlc_googlenet.caffemodel",
                           "impl/wincaffe/models/bvlc_googlenet/deploy.prototxt",
                           "impl/wincaffe/datasets/ilsvrc2012/ilsvrc_2012_mean.npy", GPU)

    def __str__(self):
        return "GoogleNet"


class GoogleNetPlaces(NeuralNet):

    def __init__(self, GPU):
        NeuralNet.__init__(self, "impl/wincaffe/models/googlenet_places/places205CNN_iter_300000.caffemodel",
                           "impl/wincaffe/models/googlenet_places/places205CNN_deploy.prototxt",
                           "impl/wincaffe/datasets/ilsvrc2012/ilsvrc_2012_mean.npy", GPU)

    def __str__(self):
        return "GoogleNetPlaces"


class VGG16(NeuralNet):

    def __init__(self, GPU):
        NeuralNet.__init__(self, "impl/wincaffe/models/VGG_16/VGG_16.caffemodel",
                           "impl/wincaffe/models/VGG_16/deploy.prototxt",
                           "impl/wincaffe/datasets/ilsvrc2012/ilsvrc_2012_mean.npy", GPU)

    def __str__(self):
        return "VGG16"


class VOC_FC8s(NeuralNet):

    def __init__(self, GPU):
        NeuralNet.__init__(self, "impl/wincaffe/models/VOC-FCN8s/fcn8s.caffemodel",
                           "impl/wincaffe/models/VOC-FCN8s/deploy.prototxt",
                           "impl/wincaffe/datasets/ilsvrc2012/ilsvrc_2012_mean.npy", GPU)

    def __str__(self):
        return "VOC_FC8s"

if __name__ == "__main__":

    # default image path
    # image_path = 'goldfish.jpg'
    #
    # pil_image = Image.open(image_path)
    # image_patch_matrix = subdivide_image_with_striving(pil_image, 60,

    #
    CNN = AlexNet(False)
    # CNN1 = AlexNet(False)
    #
    # CNN.process_image_patches_fast(image_patches1, "prob")
    # CNN1.process_image_patches(image_patches2, "prob")
    #
    # for i in range(len(image_patches1)):
    #     for j in range(len(image_patches1[i].tensor)):
    #         print "{} - {}".format(str(image_patches1[i].tensor[j]), str(image_patches2[i].tensor[j]))

    names = CNN.get_layer_names()

    print (names)

