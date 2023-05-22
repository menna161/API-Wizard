import numpy as np
from numpy.testing import assert_array_almost_equal
from tadataka.stat import zca_whitening, normalize_mean, ChiSquaredTest


def test_zca_whitening():
    X = np.random.uniform((- 10), 10, (100, 3))
    X = normalize_mean(X)
    Y = zca_whitening(X)
    C = np.cov(Y, rowvar=False)
    assert np.isclose(C, np.identity(3)).all()
    assert_array_almost_equal(np.mean(Y, axis=0), np.zeros(3))
