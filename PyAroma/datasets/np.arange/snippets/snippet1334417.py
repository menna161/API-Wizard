import types
import pytest
import numpy as np
from numpy.testing import assert_allclose
from numpy.random import RandomState
from astropy.modeling.core import Fittable1DModel
from astropy.modeling.parameters import Parameter
from astropy.modeling import models
from astropy.modeling import fitting
from astropy.utils.exceptions import AstropyUserWarning
from .utils import ignore_non_integer_warning
from scipy import optimize
from astropy.utils import NumpyRNGContext


def setup_class(self):
    self.g1 = models.Gaussian1D(10, 14.9, stddev=0.3)
    self.g2 = models.Gaussian1D(10, 13, stddev=0.4)
    self.x = np.arange(10, 20, 0.1)
    self.y1 = self.g1(self.x)
    self.y2 = self.g2(self.x)
    rsn = RandomState(1234567890)
    self.n = rsn.randn(100)
    self.ny1 = (self.y1 + (2 * self.n))
    self.ny2 = (self.y2 + (2 * self.n))
