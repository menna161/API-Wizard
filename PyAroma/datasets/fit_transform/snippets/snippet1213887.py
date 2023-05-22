import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from ute.utils.util_functions import join_data
from os.path import join
from ute.utils.arg_pars import opt
from ute.utils.util_functions import dir_check, timing


@timing
def fit_data(self):
    if self.saved_dots:
        self._result = np.loadtxt(self.saved_dots)
    else:
        if (self._mode == 'pca'):
            self._model = PCA(n_components=self._dim, random_state=opt.seed)
        if (self._mode == 'tsne'):
            self._model = TSNE(n_components=self._dim, perplexity=15, random_state=opt.seed)
        if (self.reduce is None):
            self._result = self._model.fit_transform(self._data)
        else:
            fraction = int(((self._data.shape[0] * self.reduce) / 100))
            self._model.fit(self._data[:fraction])
            self._result = self._model.transform(self._data)
