import impl.DataManagement
import xml.etree.ElementTree as ET
import json


class PatchExtractor:

    def __init__(self, **kwargs):
        pass

    def extract(self, image, name):
        pass


class FullImageExtractor(PatchExtractor):

    def __init__(self):
        PatchExtractor.__init__(self)

    def extract(self, image, name):
        width, height = image.size
        full_crop = impl.DataManagement.Cropping(0, 0, width, height)
        return [image], [full_crop]


class ImageNetAnnotationExtractor(PatchExtractor):

    def __init__(self, **kwargs):
        PatchExtractor.__init__(self)
        self.annotation_folder = kwargs["annotation_folder"]

    @staticmethod
    def __read_xml_bbox(xml_file_name):

        bbox_list = []

        tree = ET.parse(xml_file_name)
        root = tree.getroot()

        bbox_objects = root.findall("./object")

        for bbox_obj in bbox_objects:
            bbox_elements = bbox_obj.findall('./bndbox/*')

            bbox = {}
            for bbox_comp in bbox_elements:
                bbox[bbox_comp.tag] = int(bbox_comp.text)

            bbox_list.append(bbox)

        return bbox_list

    def __match_annotation(self, name):

        image_name = name.split("/")[-1]

        folder = image_name.split("_")[0]
        image_name = image_name.split(".")[0]
        xml_file_name = self.annotation_folder + "/" + folder + "/" + image_name + ".xml"

        return xml_file_name

    def extract(self, image, name):

        cropped_images, croppings = [], []

        # parse XML file
        xml_file_name = self.__match_annotation(name)
        bboxes = self.__read_xml_bbox(xml_file_name)

        # create crop instances and cropped PIL images
        for bbox in bboxes:
            cropped_image = image.crop((bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"]))
            crop = impl.DataManagement.Cropping(bbox["xmin"], bbox["ymin"],
                                                bbox["xmax"] - bbox["xmin"],
                                                bbox["ymax"] - bbox["ymin"])

            cropped_images.append(cropped_image)
            croppings.append(crop)

        return cropped_images, croppings


class POETGazePatchExtractor(PatchExtractor):

    def __init__(self, **kwargs):
        PatchExtractor.__init__(self)
        self.annotation_folder = kwargs["annotation_folder"]
        self.patch_size = kwargs["patch_size"]

        if "users" in kwargs:
            self.users = kwargs["users"]
        else:
            self.users = range(5)

        if "eye" in kwargs:
            self.eye = kwargs["eye"]
        else:
            self.eye = "fixR"

    def __get_fixations(self, name):

        image_class = name.split("/")[-1].split("_")[0]
        annotation_file = "{}/etData_{}.json".format(self.annotation_folder, image_class)

        with open(annotation_file, "r") as fp:
            data = json.load(fp)

        # getting fixations
        fixations = []
        for user_index in self.users:
            image_id = name.split("/")[-1].split("_", 1)[-1].split(".")[0]
            fixation_list = data[image_id]["fixations"][user_index]["imgCoord"][self.eye]

            for fixation in fixation_list:
                x, y = fixation["pos"]["x"], fixation["pos"]["y"]
                fixations.append((x, y))

        return fixations

    def __extract_patch_around(self, image, x, y):

        width, height = image.size

        x_min = max(0, x - int(self.patch_size / 2))
        y_min = max(0, y - int(self.patch_size / 2))
        x_max = min(width, x + int(self.patch_size / 2))
        y_max = min(height, y + int(self.patch_size / 2))

        cropped_image = image.crop((x_min, y_min, x_max, y_max))
        crop = impl.DataManagement.Cropping(x_min, y_min, x_max - x_min, y_max - y_min)

        return cropped_image, crop

    def extract(self, image, name):

        fixations = self.__get_fixations(name)

        crop_list = []
        image_list = []

        for (x, y) in fixations:
            cropped_image, crop = self.__extract_patch_around(image, x, y)
            crop_list.append(crop)
            image_list.append(cropped_image)

        return image_list, crop_list


class PascalGroundTruthExtractor(PatchExtractor):

    def __init__(self, **kwargs):
        PatchExtractor.__init__(self)
        self.annotation_folder = kwargs["annotation_folder"]

    def __get_bboxes(self, name):

        image_class = name.split("/")[-1].split("_")[0]
        annotation_file = "{}/etData_{}.json".format(self.annotation_folder, image_class)

        with open(annotation_file, "r") as fp:
            data = json.load(fp)

        image_id = name.split("/")[-1].split("_", 1)[-1].split(".")[0]
        bbox_list = data[image_id]["gtbb"]

        return bbox_list

    def extract(self, image, name):

        cropped_images = []
        croppings = []

        bboxes = self.__get_bboxes(name)

        # create crop instances and cropped PIL images
        for bbox in bboxes:
            cropped_image = image.crop((bbox["x"], bbox["y"], bbox["x"] + bbox["width"], bbox["y"] + bbox["height"]))
            crop = impl.DataManagement.Cropping(bbox["x"], bbox["y"], bbox["width"], bbox["height"])

            cropped_images.append(cropped_image)
            croppings.append(crop)

        return cropped_images, croppings

