import warnings
import itertools
import copy
import pytest
import numpy as np
from astropy.time import Time
from astropy.utils import iers


def test_argsort(self, masked):
    order = ([2, 0, 4, 3, 1] if masked else [2, 0, 1, 4, 3])
    assert np.all((self.t0.argsort() == np.array(order)))
    assert np.all((self.t0.argsort(axis=0) == np.arange(2).reshape(2, 1, 1)))
    assert np.all((self.t0.argsort(axis=1) == np.arange(5).reshape(5, 1)))
    assert np.all((self.t0.argsort(axis=2) == np.array(order)))
    ravel = np.arange(50).reshape((- 1), 5)[(:, order)].ravel()
    if masked:
        t0v = self.t0.argsort(axis=None)
        mask = self.t0.mask.ravel()[ravel]
        ravel = ravel[(~ mask)]
        assert np.all((t0v[:(- 10)] == ravel))
    else:
        assert np.all((self.t0.argsort(axis=None) == ravel))
