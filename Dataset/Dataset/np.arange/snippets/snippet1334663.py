import pytest
import numpy as np
from numpy.testing import assert_allclose, assert_equal
from .example_models import models_1D, models_2D
from astropy.modeling import fitting, models
from astropy.modeling.models import Gaussian2D
from astropy.modeling.core import FittableModel
from astropy.modeling.parameters import Parameter
from astropy.modeling.polynomial import PolynomialBase
from astropy import units as u
from astropy.utils import minversion
from astropy.tests.helper import assert_quantity_allclose
from astropy.utils import NumpyRNGContext
import scipy


def setup_class(self):
    self.N = 100
    self.M = 100
    self.eval_error = 0.0001
    self.fit_error = 0.1
    self.x = 5.3
    self.y = 6.7
    self.x1 = np.arange(1, 10, 0.1)
    self.y1 = np.arange(1, 10, 0.1)
    (self.y2, self.x2) = np.mgrid[(:10, :8)]
