import caffe
import numpy as np


def get_net(caffemodel, deploy_file, use_gpu=True, gpu_id=0):
    if use_gpu:
        caffe.set_mode_gpu()
        caffe.set_device(gpu_id)
    else:
        caffe.set_mode_cpu()

    # load a new model
    return caffe.Net(deploy_file, caffemodel, caffe.TEST)


def get_transformer(shape, mean_file):
    # src: http://nbviewer.ipython.org/github/BVLC/caffe/blob/master/examples/00-classification.ipynb
    # input preprocessing: 'data' is the name of the input blob == net.inputs[0]
    transformer = caffe.io.Transformer({'data': shape})
    transformer.set_transpose('data', (2, 0, 1))
    transformer.set_mean('data', np.load(mean_file).mean(1).mean(1))  # mean pixel
    transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    transformer.set_channel_swap('data', (2, 1, 0))  # the reference model has channels in BGR order instead of RGB
    return transformer


def read_labels(labels_file):
    if not labels_file:
        print('WARNING: No labels file provided. Results will be difficult to interpret.')
        return None

    try:
        return np.loadtxt(labels_file, str, delimiter='\t')
    except:
        print('WARNING: No labels file found. Results will be difficult to interpret.')
        return None
