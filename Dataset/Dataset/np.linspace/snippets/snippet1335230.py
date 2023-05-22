import pytest
import numpy as np
from numpy.testing import assert_allclose
from astropy.stats import bayesian_blocks, RegularEvents
from astropy.utils.exceptions import AstropyUserWarning


def test_measures_fitness_heteroscedastic():
    rng = np.random.RandomState(1)
    t = np.linspace(0, 1, 11)
    x = np.exp((((- 0.5) * ((t - 0.5) ** 2)) / (0.01 ** 2)))
    sigma = (0.02 + (0.02 * rng.rand(len(x))))
    x = (x + (sigma * rng.randn(len(x))))
    bins = bayesian_blocks(t, x, sigma, fitness='measures')
    assert_allclose(bins, [0, 0.45, 0.55, 1])
