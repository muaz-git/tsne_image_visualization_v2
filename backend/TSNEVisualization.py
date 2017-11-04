import impl.DataProvision.ImageNet.ImageNetDataProvider
import json
import impl.NeuralNetworking
import impl.DimensionalityReduction
import numpy as np

if __name__ == "__main__":

    image_folder = "data/ImageNet"
    network_name = "AlexNet"
    layer_name = "fc8"

    # create DataProvider
    img_net_dp = impl.DataProvision.ImageNet.ImageNetDataProvider.ImageNetImagePatchProvider(image_folder)

    # load image data
    pil_images = img_net_dp.get_pil_images()
    print("Loaded Data")

    # process features
    cnn = impl.NeuralNetworking.create_neural_net(network_name, False)
    features = []

    for index, image in enumerate(pil_images):
        print("Processing image {}/{}".format(index, len(pil_images)))
        cnn.process_image(image)
        features.append(cnn.get_tensor(layer_name))

    print("Processed Features")
    print(np.array(features).shape)

    # reduce dimensionality
    dim_reducer = impl.DimensionalityReduction.TSNEReducer(3)
    image_coords = dim_reducer.reduce_dimensions(features)

    # save data
    image_paths = img_net_dp.load_image_paths()
    result_data = {}

    for i in range(len(image_paths)):
        result_data[image_paths[i]] = image_coords[i].tolist()

    with open("data.json", 'w') as outfile:
        json.dump(result_data, outfile, indent=4)

    print("Saved Data")
    print("Done")
