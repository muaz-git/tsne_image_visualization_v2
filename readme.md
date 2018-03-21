# TSNE Visualization

This tool allows to encode datasets containing annotated image data with convolutional neural networks and visualize these encodings in a low dimensional space.

Feature extraction as well as image managing is handled in a Python 2.7 backend, while the visualization of the data encodings is implemented in Unity.

## Setup

- First make sure that Python 2.7 and Unity are installed.
- Install the Deep Learning Framework Caffe on your machine. 
- An additional project (Deep-Image-Clustering) handles the network processing stuff. To use it, it is required to clone this repository with all submodules. Do this with...
```sh
$ git clone --recursive http://lnv-3201/machinelearning/tsne_image_visualization.git
```

## Usage

This project is organized using the following modules which manage the whole data processing pipeline:

![Project Organisation Graphics](http://lnv-3201.sb.dfki.de/machinelearning/tsne_image_visualization/raw/master/improved_pipeline.png)

Preprocessing in Python and visualization in Unity are two separated processes. First, from image data, the coordinates computed by the Neural Network and by the feature reduction processes get created and saved to a .json file. Afterwards, Unity uses this file to load and position the images in a 3D space.

To start the preprocessing pipeline, run...
```sh
$ cd backend
$ python ./TSNEVisualization.py
```

In the file `TSNEVisualization.py`, all required settings for each module of the pipeline can be controlled. By default, this script expects image data from ImageNet in the folder `data/POET/pascal_mini` and bounding box annotations in `data/POET/etData`. From the Neural Network "AlexNet", the layer fc8 is used for feature extraction.

For dimensionality reduction, first, PCA reduces the CNN features down to 50 units. Afterwards, TSNE reduces the features to 3 dimensions, so Unity can later use these as coordinate values.

To visualize the images with the reduced features, just load the Unity project and run the scene.

### Load new Image Data

To load new image data, change the path for the `ImageProvider`. For just using images without further annotations, use the `FullImageExtractor` as PatchProvider.
For the dimensionality reduction, it is only important that the resulting dimensionality of an image is 3. New dimensionality reduction methods can be implemented and added.

