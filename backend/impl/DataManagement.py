import json
import numpy as np
import copy


class DataManager:
    """
    Class managing image data, clusters, user interactions and croppings of an image dataset
    """

    def __init__(self):
        self.image_data = {}

    def load_data(self, filename):
        """
        Loads data from an existing json file
        :param filename: name of the json file
        """
        self.image_data = json.loads(filename)
        print("Loaded data from {}".format(filename))

    def load_patches(self, patch_provider):
        samples = patch_provider.get_samples()
        for sample in samples:
            self.update_data(sample)

    def save_data(self, filename):
        """
        Serialize current state of data to a json file
        :param filename: filename where data is saved to
        """
        with open(filename, 'w') as outfile:
            json.dump(self.image_data, outfile, indent=4, sort_keys=True)

        print("Saved data to {}".format(filename))

    def update_data(self, data_sample):
        """
        Updates the current data by adding or replacing the values of a data sample
        :param data_sample: Data sample which should be updated/added to the data
        """
        self.image_data.update(data_sample.to_json())


class DataSample:
    """
    Instance of data for a single image. One image can contain several croppings while for each cropping the TSNE
    coordinates, the cluster where the cropping is currently related to, the cluster the user set the cropping to,
    the model which computed a the features that lead to the TSNE coordinates.
    """

    def __init__(self, filename, coordinates, croppings=None, cur_cluster_ids=None, user_cluster_ids=None, model_ids=None):

        self.filename = filename
        self.coordinates = coordinates

        sample_count = len(coordinates)

        # Cluster ID Checks
        if cur_cluster_ids is None:
            self.cur_cluster_ids = (np.ones(sample_count) * -1).tolist()

        elif len(cur_cluster_ids) != sample_count:
            print("The amount of cluster IDs has to be the same like the amount of given coordinates!")
            print("Coordinate counts: {} Cluster ID counts: {}".format(sample_count, len(cur_cluster_ids)))
            assert False
        else:
            self.cur_cluster_ids = cur_cluster_ids

        # User Cluster ID Checks
        if user_cluster_ids is None:
            self.user_cluster_ids = (np.ones(sample_count) * -1).tolist()

        elif len(user_cluster_ids) != sample_count:
            print("The amount of user cluster IDs has to be the same like the amount of given coordinates!")
            print("Coordinate counts: {} User Cluster ID counts: {}".format(sample_count, len(user_cluster_ids)))
            assert False
        else:
            self.user_cluster_ids = user_cluster_ids

        # Model ID Checks
        if model_ids is None:
            self.model_ids = (np.ones(sample_count) * -1).tolist()

        elif len(model_ids) != sample_count:
            print("The amount of Model IDs has to be the same like the amount of given coordinates!")
            print("Coordinate counts: {} Model ID counts: {}".format(sample_count, len(model_ids)))
            assert False
        else:
            self.model_ids = model_ids

        # Cropping Checks
        if croppings is None:
            dummy_crop = Cropping(-1, -1, -1, -1)
            self.croppings = []
            for i in range(sample_count):
                self.croppings.append(copy.deepcopy(dummy_crop))
        elif len(croppings) != sample_count:
            print("The amount of Croppings has to be the same like the amount of given coordinates!")
            print("Coordinate counts: {} Cropping counts: {}".format(sample_count, len(croppings)))
            assert False
        else:
            self.croppings = croppings

    def to_json(self):
        """
        Creates a json serializable dictionary which will be used for saving and serializing the data
        :return: dictionary containing all data of this sample
        """

        new_dict = {}
        new_dict[self.filename] = {}

        new_dict[self.filename]["coordinates"] = []
        for coord in self.coordinates:
            new_dict[self.filename]["coordinates"].append(coord.to_json())

        new_dict[self.filename]["cur_cluster_ids"] = []
        for cur_cluster_id in self.cur_cluster_ids:
            new_dict[self.filename]["cur_cluster_ids"].append(cur_cluster_id)

        new_dict[self.filename]["user_cluster_ids"] = []
        for user_cluster_id in self.user_cluster_ids:
            new_dict[self.filename]["user_cluster_ids"].append(user_cluster_id)

        new_dict[self.filename]["model_ids"] = []
        for model_id in self.model_ids:
            new_dict[self.filename]["model_ids"].append(model_id)

        new_dict[self.filename]["croppings"] = []
        for cropping in self.croppings:
            new_dict[self.filename]["croppings"].append(cropping.to_json())

        return new_dict#

    def count(self):
        """
        Returns the amount of croppings in this sample
        :return: amount of croppings
        """
        return len(self.coordinates)

    def add(self, coordinates, cropping, cluster_id, user_cluster_id, model_id):
        """
        Adds a cropping with its corresponding values to the sample
        :param coordinates: TSNE corrdinates of the cropping
        :param cropping: the cropping properties
        :param cluster_id: ID of the current cluster of this cropping
        :param user_cluster_id: ID of the user cluster of this cropping
        :param model_id: ID of the model which computed the TSNE coordinate features
        """
        self.coordinates.append(coordinates)
        self.croppings.append(cropping)
        self.cur_cluster_ids.append(cluster_id)
        self.user_cluster_ids.append(user_cluster_id)
        self.model_ids.append(model_id)

    def remove(self, index):
        """
        Removes a cropping instance from this sample
        """

        if index < 0 or index >= self.count():
            print("Index {} is out of bounds for a sample of size {}".format(index, self.count()))
            assert False

        del self.coordinates[index]
        del self.croppings[index]
        del self.cur_cluster_ids[index]
        del self.user_cluster_ids[index]
        del self.model_ids[index]

    @staticmethod
    def create_empty(filename):
        """
        Creates a data sample of an image containing no croppings
        :param filename: filename of the image
        :return: Empty data sample
        """
        sample = DataSample(filename, [], [], [], [], [])
        return sample


class Coordinate:
    """
    Representation of a 3D coordinate vector
    """

    def __init__(self, x, y, z):
        self.x, self.y, self.z = float(x), float(y), float(z)

    def to_json(self):
        return {"x": self.x, "y": self.y, "z": self.z}


class Cropping:
    """
    Representation of an image cropping
    """

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def to_json(self):
        return {"x": self.x, "y": self.y, "width": self.width, "height": self.height}
