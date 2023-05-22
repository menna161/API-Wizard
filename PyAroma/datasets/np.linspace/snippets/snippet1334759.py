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


def setup_class(self):
    self.N = 100
    self.M = 100
    self.x1 = np.linspace(1, 10, 100)
    (self.y2, self.x2) = np.mgrid[(:100, :83)]
    rsn = np.random.RandomState(0)
    self.n1 = (rsn.randn(self.x1.size) * 0.1)
    self.n2 = rsn.randn(self.x2.size)
    self.n2.shape = self.x2.shape
    self.linear_fitter = fitting.LinearLSQFitter()
    self.non_linear_fitter = fitting.LevMarLSQFitter()
