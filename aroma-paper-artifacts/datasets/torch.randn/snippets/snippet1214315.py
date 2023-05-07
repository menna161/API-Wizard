import math
from typing import Optional
import pytest
import torch
from sklearn.cluster import KMeans as SklearnKMeans
from pycave.clustering import KMeans
from tests._data.gmm import sample_gmm


def test_fit_num_iter():
    data = torch.cat([((torch.randn(1000, 4) * 0.1) - 100), ((torch.randn(1000, 4) * 0.1) + 100)])
    estimator = KMeans(2)
    estimator.fit(data)
    assert (estimator.num_iter_ == 1)
