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
    self.p1 = models.Polynomial1D(4)
    self.p1.c0 = 0
    self.p1.c1 = 0
    self.p1.window = [0.0, 9.0]
    self.x = np.arange(10)
    self.y = self.p1(self.x)
    rsn = RandomState(1234567890)
    self.n = rsn.randn(10)
    self.ny = (self.y + self.n)
