import impl.DataProvision.ImageProvision
import json
import impl.NeuralNetworking
import impl.DimensionalityReduction
import numpy as np
# from .impl.deep-image-clustering.model.util import create_model
# from .impl.deep-image-clustering.model.model import Backend, CNN
from impl.DataManagement import *

if __name__ == "__main__":

    image_folder = "data/ImageNet"
    network_name = "AlexNet"
    layer_name = "fc8"

    # create DataProvider
    img_net_dp = impl.DataProvision.ImageProvision.ImageNetImageProvider(image_folder)

    # create DataManager
    data_man = DataManager()

    # load image data
    pil_images = img_net_dp.get_pil_images()
    print("Loaded Data")

    # process features
    cnn = impl.NeuralNetworking.create_neural_net(network_name, False)
    features = []

    # model = create_model(Backend.CAFFE, CNN.GOOGLENET)

    print("")
    for index, image in enumerate(pil_images):
        print("\rProcessing image {}/{}".format(index + 1, len(pil_images)), end='')
        cnn.process_image(image)
        features.append(cnn.get_tensor(layer_name))

    print("Processed Features")

    # reduce dimensionality
    pca_dim_reducer = impl.DimensionalityReduction.PCAReducer(50)
    tsne_dim_reducer = impl.DimensionalityReduction.TSNEReducer(3)

    pca_reduced = pca_dim_reducer.reduce_dimensions(features)
    image_coords = tsne_dim_reducer.reduce_dimensions(pca_reduced)

    # save data
    image_paths = img_net_dp.load_image_paths()
    result_data = {}

    for i in range(len(image_paths)):

        # create new sample object
        coords = Coordinate(image_coords[i][0], image_coords[i][1], image_coords[i][2])
        sample = DataSample(image_paths[i], [coords])

        data_man.update_data(sample)

    data_man.save_data("data.json")
    print("Done")
