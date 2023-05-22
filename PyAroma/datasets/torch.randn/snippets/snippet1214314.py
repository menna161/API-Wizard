import math
from typing import Optional
import pytest
import torch
from sklearn.cluster import KMeans as SklearnKMeans
from pycave.clustering import KMeans
from tests._data.gmm import sample_gmm


def test_fit_automatic_config():
    estimator = KMeans(4)
    data = torch.cat([((torch.randn(1000, 3) * 0.1) - 100), ((torch.randn(1000, 3) * 0.1) + 100)])
    estimator.fit(data)
    assert (estimator.model_.config.num_clusters == 4)
    assert (estimator.model_.config.num_features == 3)
