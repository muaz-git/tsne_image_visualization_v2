import impl.DataManagement


class PatchExtractor:

    def __init__(self):
        pass

    def extract(self, image):
        pass


class FullImageExtractor(PatchExtractor):

    def __init__(self):
        PatchExtractor.__init__(self)

    def extract(self, image):
        width, height = image.size
        full_crop = impl.DataManagement.Cropping(0, 0, width, height)
        return [image], [full_crop]


class CoordPatchExtractor(PatchExtractor):

    def __init__(self, annotation_file):
        PatchExtractor.__init__(self)

        # TODO: read annotations properly
        self.annotations = annotation_file

    def extract(self, image):
        # img.crop((0, 0, 100, 100))
        pass

