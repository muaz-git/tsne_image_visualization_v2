import json
import numpy as np
import copy


class DataManager:

    def __init__(self):
        self.image_data = {}

    def load_data(self, filename):
        self.image_data = json.loads(filename)
        print("Loaded data from {}".format(filename))

    def save_data(self, filename):
        with open(filename, 'w') as outfile:
            json.dump(self.image_data, outfile, indent=4, sort_keys=True)

        print("Saved data to {}".format(filename))

    def update_data(self, data_sample):
        self.image_data.update(data_sample.to_json())


class DataSample:

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
        return len(self.coordinates)

    def add(self, coordinates, cropping, cluster_id, user_cluster_id, model_id):
        self.coordinates.append(coordinates)
        self.croppings.append(cropping)
        self.cur_cluster_ids.append(cluster_id)
        self.user_cluster_ids.append(user_cluster_id)
        self.model_ids.append(model_id)

    def remove(self, index):

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
        sample = DataSample(filename, [], [], [], [], [])
        return sample


class Coordinate:

    def __init__(self, x, y, z):
        self.x, self.y, self.z = float(x), float(y), float(z)

    def to_json(self):
        return {"x": self.x, "y": self.y, "z": self.z}


class Cropping:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def to_json(self):
        return {"x": self.x, "y": self.y, "width": self.width, "height": self.height}
