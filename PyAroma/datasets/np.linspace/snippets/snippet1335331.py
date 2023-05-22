import warnings
import pytest
import numpy as np
from numpy.testing import assert_allclose
from astropy.stats import histogram, calculate_bin_edges, scott_bin_width, freedman_bin_width, knuth_bin_width
from astropy.utils.exceptions import AstropyUserWarning
import scipy


def test_histogram_range_with_bins_list(N=1000, rseed=0):
    rng = np.random.RandomState(rseed)
    x = rng.randn(N)
    range = (0.1, 0.8)
    input_bins = np.linspace((- 5), 5, 31)
    bins = calculate_bin_edges(x, input_bins, range=range)
    assert all((bins == input_bins))
