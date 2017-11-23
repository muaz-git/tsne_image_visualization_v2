import impl.DataProvision.ImageProvision
import impl.DataProvision.PatchExtraction
import impl.NeuralNetworking
import impl.DataManagement


class ImagePatchProvider:

    def __init__(self, image_provider, patch_extractor, cnn, layer, dim_reducers):

        self.data_extracted = False

        self.image_provider = image_provider
        self.patch_extractor = patch_extractor

        self.cnn = cnn
        self.layer = layer

        self.dim_reducers = dim_reducers

        # check if last dim reducer creates 3D coordinates
        if self.dim_reducers[-1].dim_count != 3:
            print("The last dimensionality reducer does not return 3D data.")
            assert False

        self.patches = {}

    def __get_patch_images(self):
        images = []
        for file_name in self.patches:
            images += self.patches[file_name]["pils"]

        return images

    def __set_features(self, new_features):

        index = 0

        for file_name in self.patches:
            sample_count = len(self.patches[file_name]["pils"])

            for i in range(sample_count):
                self.patches[file_name]["pils"][i] = new_features[index]
                index += 1

    def __get_patch_features(self):
        features = []

        for file_name in self.patches:
            features += self.patches[file_name]["features"]

        return features

    def __extract_patches(self):

        # create croppings
        for file_name, pil_image in self.image_provider:
            cropped_images, croppings = self.patch_extractor.extract(pil_image)

            self.patches[file_name] = {"pils": cropped_images, "corps": croppings, "features": []}

    def __process_patch_features(self):

        features = []

        # TODO: Can be improved when increasing batch size
        for image in self.__get_patch_images():
            self.cnn.process_image(image)
            features.append(self.cnn.get_tensor(self.layer))

        self.__set_features(features)

    def __reduce_dimensionality(self):

        reduced_features = self.__get_patch_features()

        # reduce features with each reducer
        for dim_reducer in self.dim_reducers:
            reduced_features = dim_reducer.reduce_dimensions(reduced_features)

        # replace features with reduced features
        self.__set_features(reduced_features)

    def get_samples(self):

        if not self.data_extracted:
            self.setup_patches()

        samples = []

        for image_name in self.patches:
            coord_list = []

            for [x, y, z] in self.patches[image_name]["features"]:
                coords = impl.DataManagement.Coordinate(x, y, z)
                coord_list.append(coords)

            image_sample = impl.DataManagement.DataSample(image_name, coord_list, self.patches[image_name]["crops"], -1, -1, self.cnn.generate_id(self.layer))
            samples.append(image_sample)

        return samples

    def setup_patches(self):
        self.__extract_patches()
        self.__process_patch_features()
        self.__reduce_dimensionality()

        self.data_extracted = True
