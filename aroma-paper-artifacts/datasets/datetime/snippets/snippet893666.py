from pyodds.algo.base import Base
from luminol import anomaly_detector
import numpy as np
import pandas as pd
from luminol.modules.time_series import TimeSeries
from luminol.utils import to_epoch
from sklearn.decomposition import IncrementalPCA


def fit(self, X):
    'Fit detector.\n        Parameters\n        ----------\n        X : dataframe of shape (n_samples, n_features)\n            The input samples.\n        '
    X = X.to_numpy()
    timestamp = np.asarray(X[(:, 0)].astype(np.datetime64))
    pca = IncrementalPCA(n_components=1)
    value = np.reshape(pca.fit_transform(X[(:, 1:)]), (- 1))
    X = pd.Series(value, index=timestamp)
    X.index = X.index.map((lambda d: to_epoch(str(d))))
    lts = TimeSeries(X.to_dict())
    self.ts = timestamp
    self.ts_value = value
    self.detector = anomaly_detector.AnomalyDetector(lts)
    return self
