import numpy as np
import scipy.sparse as sp
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.utils.validation import check_is_fitted


def fit_transform(self, raw_documents, y=None):
    X = super(BM25Vectorizer, self).fit_transform(raw_documents)
    X = X.tocoo()
    (n_samples, n_features) = X.shape
    doc_len = np.ravel(X.sum(axis=1))
    avg_len = doc_len.mean()
    len_norm = ((1.0 - self.b) + ((self.b * doc_len) / avg_len))
    idf = np.log((float(n_samples) / (1 + np.bincount(X.col))))
    X.data = (((X.data * (self.k1 + 1.0)) / ((self.k1 * len_norm[X.row]) + X.data)) * idf[X.col])
    return X.tocsr()
