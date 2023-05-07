import numpy as np
import torch
from pytest_benchmark.fixture import BenchmarkFixture
from sklearn.mixture._gaussian_mixture import _compute_precision_cholesky
from sklearn.mixture._gaussian_mixture import _estimate_log_gaussian_prob
from torch.distributions import MultivariateNormal
from pycave.bayes.core import cholesky_precision, log_normal


def test_torch_log_normal_tied(benchmark: BenchmarkFixture):
    data = torch.randn(10000, 100)
    means = torch.randn(50, 100)
    A = torch.randn(1000, 100)
    covars = A.t().mm(A)
    cholesky = torch.linalg.cholesky(covars)
    distribution = MultivariateNormal(means, scale_tril=cholesky, validate_args=False)
    benchmark(distribution.log_prob, data.unsqueeze(1))
