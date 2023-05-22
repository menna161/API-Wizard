import numpy as np
import torch
from pytest_benchmark.fixture import BenchmarkFixture
from sklearn.mixture._gaussian_mixture import _compute_precision_cholesky
from sklearn.mixture._gaussian_mixture import _estimate_log_gaussian_prob
from torch.distributions import MultivariateNormal
from pycave.bayes.core import cholesky_precision, log_normal


def test_log_normal_full(benchmark: BenchmarkFixture):
    data = torch.randn(10000, 100)
    means = torch.randn(50, 100)
    A = torch.randn(50, 1000, 100)
    covars = A.permute(0, 2, 1).bmm(A)
    precisions = cholesky_precision(covars, 'full')
    benchmark(log_normal, data, means, precisions, covariance_type='full')
