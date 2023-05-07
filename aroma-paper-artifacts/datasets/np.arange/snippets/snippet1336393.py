from __future__ import absolute_import, division, print_function
import numpy as np
from astropy import units as u
from astropy.uncertainty.core import Distribution
from astropy.uncertainty import distributions as ds
from astropy.utils import NumpyRNGContext
from astropy.tests.helper import assert_quantity_allclose, pytest
from scipy.stats import norm


def test_reprs():
    darr = np.arange(30).reshape(3, 10)
    distr = Distribution((darr * u.kpc))
    assert ('n_samples=10' in repr(distr))
    assert ('n_samples=10' in str(distr))
    assert ('n_{\\rm samp}=10' in distr._repr_latex_())
