import math
from typing import Optional
import pytest
import torch
from sklearn.mixture import GaussianMixture as SklearnGaussianMixture
from pycave.bayes import GaussianMixture
from pycave.bayes.core import CovarianceType
from tests._data.gmm import sample_gmm


def test_fit_model_config():
    estimator = GaussianMixture()
    data = torch.randn(1000, 4)
    estimator.fit(data)
    assert (estimator.model_.config.num_components == 1)
    assert (estimator.model_.config.num_features == 4)
