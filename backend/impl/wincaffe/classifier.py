from model import *
import numpy as np
import time
import os


class Classifier:

    def __init__(self, model_config, use_gpu=True):
        self.model = Model(model_config, use_gpu)

    def forward_pass(self, images, batch_size=1):
        caffe_images = []
        for image in images:
            if image.ndim == 2:
                caffe_images.append(image[:, :, np.newaxis])
            else:
                caffe_images.append(image)

        caffe_images = np.array(caffe_images)

        transformer = self.model.transformer
        net = self.model.net

        dims = transformer.inputs['data'][1:]

        scores = None
        for chunk in [caffe_images[x:x + batch_size] for x in range(0, len(caffe_images), batch_size)]:
            new_shape = (len(chunk),) + tuple(dims)
            if net.blobs['data'].data.shape != new_shape:
                net.blobs['data'].reshape(*new_shape)
            for index, image in enumerate(chunk):
                image_data = transformer.preprocess('data', image)
                net.blobs['data'].data[index] = image_data
            output = net.forward()[net.outputs[-1]]
            if scores is None:
                scores = np.zeros(output.shape)
                scores[:] = output
            else:
                scores = np.vstack((scores, output))
                # print 'Processed %s/%s images ...' % (len(scores), len(caffe_images))

        return scores

    def classify(self, images):

        # Classify the image
        scores = self.forward_pass(images)

        # Process the results
        indices = (-scores).argsort()[:, :5]  # take top 5 results
        classifications = []
        for image_index, index_list in enumerate(indices):
            result = []
            for i in index_list:
                # 'i' is a category in labels and also an index into scores
                if self.model.labels is None:
                    label = 'Class #%s' % i
                else:
                    label = self.model.labels[i]
                result.append((label, round(100.0 * scores[image_index, i], 4)))
            classifications.append(result)

        return classifications
