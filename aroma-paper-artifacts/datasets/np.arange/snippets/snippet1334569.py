import pytest
import numpy as np
from numpy.testing import assert_allclose
from astropy.modeling import models
from astropy.modeling import fitting
from astropy.modeling.core import Model, FittableModel, Fittable1DModel
from astropy.modeling.parameters import Parameter
from scipy import optimize


def setup_class(self):
    self.x = 5.3
    self.y = 6.7
    self.x1 = np.arange(1, 10, 0.1)
    self.y1 = np.arange(1, 10, 0.1)
    (self.y2, self.x2) = np.mgrid[(:10, :8)]
