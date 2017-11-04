from ..DataProvision import ImagePatchProvider
from PIL import Image
import os
from random import randrange


class ImageNetImagePatchProvider(ImagePatchProvider):

    def __init__(self, image_folder):
        ImagePatchProvider.__init__(self, image_folder)

    def load_image_paths(self):
        image_paths = []
        for root, dirs, files in os.walk(self.image_folder):
            for path in files:
                if path.endswith(".jpg") or path.endswith(".JPEG"):
                    image_paths.append(path)

        image_paths.sort()
        return image_paths

    def get_single_pil_image(self, image_file):
        image_file_path = self.image_folder + "/" + image_file

        im = Image.open(image_file_path)
        return im

    def get_pil_images(self, image_files=None):

        images = []

        if image_files is None:
            image_files = self.load_image_paths()

        for image_path in image_files:
            images.append(self.get_single_pil_image(image_path))

        return images

    def get_random_pil_images(self, amount):

        all_image_paths = self.load_image_paths()
        image_paths = []

        for i in range(amount):
            random_index = randrange(0, len(all_image_paths))
            image_paths.append(all_image_paths[random_index])

        return self.get_pil_images(image_paths)
