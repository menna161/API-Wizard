import numpy as np
import torch
from pytest_benchmark.fixture import BenchmarkFixture
from sklearn.mixture._gaussian_mixture import _compute_precision_cholesky
from pycave.bayes.core import cholesky_precision


def test_cholesky_precision_full(benchmark: BenchmarkFixture):
    A = torch.randn(50, 10000, 100)
    covars = A.permute(0, 2, 1).bmm(A)
    benchmark(cholesky_precision, covars, 'full')
