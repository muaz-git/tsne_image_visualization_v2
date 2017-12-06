from PIL import Image
import os
from random import randrange


class ImageProvider:

    def __init__(self, image_folder):
        self.image_folder = image_folder
        self.image_file_names = self.load_image_paths()
        self.iter_index = 0

    def load_image_paths(self):
        image_paths = []
        for root, dirs, files in os.walk(self.image_folder):
            for path in files:
                if path.endswith(".jpg") or path.endswith(".JPEG"):

                    root_name = root.replace("\\", "/")
                    image_paths.append(root_name + "/" + path)

        image_paths.sort()
        return image_paths

    @staticmethod
    def get_single_pil_image(image_file):
        image_file_path = image_file

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

    def __iter__(self):
        return self

    def next(self):
        if self.iter_index < len(self.image_file_names):
            file_name = self.image_file_names[self.iter_index]
            image = self.get_single_pil_image(file_name)
            self.iter_index += 1
            return file_name, image
        else:
            raise StopIteration()

    def __len__(self):
        return len(self.image_file_names)


class ImageNetImageProvider(ImageProvider):

    def __init__(self, image_folder):
        ImageProvider.__init__(self, image_folder)

        self.image_file_names = self.load_image_paths()
        self.iter_index = 0


class PascalImageProvider(ImageProvider):

    def __init__(self, image_folder):
        ImageProvider.__init__(self, image_folder)
