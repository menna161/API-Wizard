import warnings
import pytest
import numpy as np
from numpy.testing import assert_allclose
from astropy.stats import histogram, calculate_bin_edges, scott_bin_width, freedman_bin_width, knuth_bin_width
from astropy.utils.exceptions import AstropyUserWarning
import scipy


@pytest.mark.parametrize('bin_type', (_bin_types_to_test + [np.linspace((- 5), 5, 31)]))
def test_histogram(bin_type, N=1000, rseed=0):
    rng = np.random.RandomState(rseed)
    x = rng.randn(N)
    (counts, bins) = histogram(x, bin_type)
    assert (counts.sum() == len(x))
    assert (len(counts) == (len(bins) - 1))
