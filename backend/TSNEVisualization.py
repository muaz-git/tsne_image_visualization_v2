import impl.NeuralNetworking
import impl.DimensionalityReduction
import impl.DataProvision.ImageProvision
from impl.DataManagement import *
import impl.DataProvision.PatchExtraction
import impl.DataProvision.PatchManagement

if __name__ == "__main__":

    # image_folder = "data/ImageNet/images"
    # annotation_folder = "data/ImageNet/annotations"

    network_name = "AlexNet"
    layer_name = "fc8"

    # ImageProvider
    # img_net_dp = impl.DataProvision.ImageProvision.ImageNetImageProvider("data/ImageNet/images")
    pascal_images = impl.DataProvision.ImageProvision.PascalImageProvider("data/POET/pascal_mini")

    # PatchProvider
    # img_net_annotations = impl.DataProvision.PatchExtraction.ImageNetAnnotationExtractor(annotation_folder=annotation_folder)
    # img_net_annotations = impl.DataProvision.PatchExtraction.FullImageExtractor()
    gaze_patch_data = impl.DataProvision.PatchExtraction.PascalGroundTruthExtractor(annotation_folder="data/POET/etData")

    # CNN module
    cnn = impl.NeuralNetworking.create_neural_net(network_name, False)

    # dimensionality reduction modules
    pca_dim_reducer = impl.DimensionalityReduction.PCAReducer(50)
    tsne_dim_reducer = impl.DimensionalityReduction.TSNEReducer(3)
    dim_reducers = [pca_dim_reducer, tsne_dim_reducer]

    # PatchProvider
    patch_provider = impl.DataProvision.PatchManagement.ImagePatchProvider(pascal_images, gaze_patch_data, cnn, layer_name, dim_reducers)

    # create DataManager
    data_man = DataManager()

    data_man.load_patches(patch_provider)

    data_man.save_data("poet_gt.json")
    print("Done")
