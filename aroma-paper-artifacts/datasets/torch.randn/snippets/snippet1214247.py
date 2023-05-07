import numpy as np
import torch
from pytest_benchmark.fixture import BenchmarkFixture
from sklearn.mixture._gaussian_mixture import _compute_precision_cholesky
from sklearn.mixture._gaussian_mixture import _estimate_log_gaussian_prob
from torch.distributions import MultivariateNormal
from pycave.bayes.core import cholesky_precision, log_normal


def test_torch_log_normal_spherical(benchmark: BenchmarkFixture):
    data = torch.randn(10000, 100)
    means = torch.randn(50, 100)
    covars = torch.rand(50)
    covar_matrices = torch.stack([(torch.eye(means.size((- 1))) * c) for c in covars])
    cholesky = torch.linalg.cholesky(covar_matrices)
    distribution = MultivariateNormal(means, scale_tril=cholesky, validate_args=False)
    benchmark(distribution.log_prob, data.unsqueeze(1))
