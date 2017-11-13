import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA


class DimReducer:

    def __init__(self, dim_count):
        self.dim_count = dim_count

    def reduce_dimensions(self, x):
        pass


class TSNEReducer(DimReducer):

    def __init__(self, dim_count):
        DimReducer.__init__(self, dim_count)

    def reduce_dimensions(self, x):

        data = np.array(x)
        data_embedded = TSNE(n_components=self.dim_count).fit_transform(data)

        return data_embedded


class PCAReducer(DimReducer):

    def __init__(self, dim_count):
        DimReducer.__init__(self, dim_count)

    def reduce_dimensions(self, x):
        data = np.array(x)
        data_embedded = PCA(n_components=self.dim_count).fit_transform(data)

        return data_embedded
