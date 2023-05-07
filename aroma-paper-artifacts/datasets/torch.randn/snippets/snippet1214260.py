import numpy as np
import torch
from pytest_benchmark.fixture import BenchmarkFixture
from sklearn.mixture._gaussian_mixture import _compute_precision_cholesky
from pycave.bayes.core import cholesky_precision


def test_cholesky_precision_tied(benchmark: BenchmarkFixture):
    A = torch.randn(10000, 100)
    covars = A.t().mm(A)
    benchmark(cholesky_precision, covars, 'tied')
