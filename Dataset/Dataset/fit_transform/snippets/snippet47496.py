import numpy as np
import scipy.sparse as sp
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.utils.validation import check_is_fitted


def fit(self, raw_documents, y=None):
    'Learn vocabulary and log-entropy from training set.\n        Parameters\n        ----------\n        raw_documents : iterable\n            an iterable which yields either str, unicode or file objects\n        Returns\n        -------\n        self : LogEntropyVectorizer\n        '
    X = super(LogEntropyVectorizer, self).fit_transform(raw_documents)
    (n_samples, n_features) = X.shape
    gf = np.ravel(X.sum(axis=0))
    if self.smooth_idf:
        n_samples += int(self.smooth_idf)
        gf += int(self.smooth_idf)
    P = (X * sp.spdiags((1.0 / gf), diags=0, m=n_features, n=n_features))
    p = P.data
    P.data = ((p * np.log2(p)) / np.log2(n_samples))
    g = (1 + np.ravel(P.sum(axis=0)))
    f = np.log2((1 + X.data))
    X.data = f
    self._G = sp.spdiags(g, diags=0, m=n_features, n=n_features)
    return self
