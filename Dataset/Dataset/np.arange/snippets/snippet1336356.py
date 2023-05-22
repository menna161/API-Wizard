import pytest
import numpy as np
from numpy.testing import assert_equal
from astropy import units as u
from astropy.time import Time
from astropy.timeseries.sampled import TimeSeries
from astropy.timeseries.downsample import aggregate_downsample, reduceat


def test_reduceat():
    add_output = np.add.reduceat(np.arange(8), [0, 4, 1, 5, 2, 6, 3, 7])
    sum_output = reduceat(np.arange(8), [0, 4, 1, 5, 2, 6, 3, 7], np.sum)
    assert_equal(sum_output, add_output)
    mean_output = reduceat(np.arange(8), np.arange(8)[::2], np.mean)
    assert_equal(mean_output, np.array([0.5, 2.5, 4.5, 6.5]))
    nanmean_output = reduceat(np.arange(8), [0, 4, 1, 5, 2, 6, 3, 7], np.mean)
    assert_equal(nanmean_output, np.array([1.5, 4, 2.5, 5, 3.5, 6, 4.5, 7.0]))
    assert_equal(reduceat(np.arange(8), np.arange(8)[::2], np.mean), reduceat(np.arange(8), np.arange(8)[::2], np.nanmean))
