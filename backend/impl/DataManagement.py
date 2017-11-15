import json


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

    def update_data(self, data_object):
        self.image_data.update(data_object.to_json())


class SampleData:

    def __init__(self, filename, coordinates, cur_cluster_id=-1, user_cluster_id=-1, model_id=-1):
        self.filename = filename
        self.coordinates = coordinates
        self.cur_cluster_id = cur_cluster_id
        self.user_cluster_id = user_cluster_id
        self.model_id = model_id

    def to_json(self):
        new_dict = {}
        new_dict[self.filename] = {"coordinates": self.coordinates.to_json(),
                                   "cur_cluster_id": self.cur_cluster_id,
                                   "user_cluster_id": self.user_cluster_id,
                                   "model_id": self.model_id}
        return new_dict


class Coordinate:

    def __init__(self, x, y, z):
        self.x, self.y, self.z = float(x), float(y), float(z)

    def to_json(self):
        return {"x": self.x, "y": self.y, "z": self.z}
