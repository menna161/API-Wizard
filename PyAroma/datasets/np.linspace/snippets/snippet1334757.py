import os
import warnings
from itertools import product
import pytest
import numpy as np
from numpy.testing import assert_allclose
from astropy.modeling import fitting
from astropy import wcs
from astropy.io import fits
from astropy.modeling.polynomial import Chebyshev1D, Hermite1D, Legendre1D, Polynomial1D, Chebyshev2D, Hermite2D, Legendre2D, Polynomial2D, SIP, PolynomialBase, OrthoPolynomialBase
from astropy.modeling.functional_models import Linear1D
from astropy.modeling.mappings import Identity
from astropy.utils.data import get_pkg_data_filename
from astropy.utils.exceptions import AstropyUserWarning
from scipy import optimize


@pytest.mark.parametrize('cls', (Polynomial1D, Chebyshev1D, Legendre1D, Polynomial2D, Chebyshev2D, Legendre2D))
def test_zero_degree_polynomial(cls):
    '\n    A few tests that degree=0 polynomials are correctly evaluated and\n    fitted.\n\n    Regression test for https://github.com/astropy/astropy/pull/3589\n    '
    if (cls.n_inputs == 1):
        p1 = cls(degree=0, c0=1)
        assert (p1(0) == 1)
        assert np.all((p1(np.zeros(5)) == np.ones(5)))
        x = np.linspace(0, 1, 100)
        y = (1 + np.random.uniform(0, 0.1, len(x)))
        p1_init = cls(degree=0)
        fitter = fitting.LinearLSQFitter()
        p1_fit = fitter(p1_init, x, y)
        assert_allclose(p1_fit.c0, 1, atol=0.1)
    elif (cls.n_inputs == 2):
        if issubclass(cls, OrthoPolynomialBase):
            p2 = cls(x_degree=0, y_degree=0, c0_0=1)
        else:
            p2 = cls(degree=0, c0_0=1)
        assert (p2(0, 0) == 1)
        assert np.all((p2(np.zeros(5), np.zeros(5)) == np.ones(5)))
        (y, x) = np.mgrid[(0:1:100j, 0:1:100j)]
        z = (1 + np.random.uniform(0, 0.1, x.size)).reshape(100, 100)
        if issubclass(cls, OrthoPolynomialBase):
            p2_init = cls(x_degree=0, y_degree=0)
        else:
            p2_init = cls(degree=0)
        fitter = fitting.LinearLSQFitter()
        p2_fit = fitter(p2_init, x, y, z)
        assert_allclose(p2_fit.c0_0, 1, atol=0.1)
