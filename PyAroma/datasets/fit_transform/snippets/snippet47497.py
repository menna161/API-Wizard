import numpy as np
import scipy.sparse as sp
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.utils.validation import check_is_fitted


def fit_transform(self, raw_documents, y=None):
    self.fit(raw_documents)
    return self.transform(raw_documents)
