import pytest
import numpy as np
from numpy.testing import assert_allclose
from astropy.modeling import models
from astropy.modeling import fitting
from astropy.modeling.core import Model, FittableModel, Fittable1DModel
from astropy.modeling.parameters import Parameter
from scipy import optimize


def setup_class(self):
    self.x1 = np.arange(10)
    (self.y, self.x) = np.mgrid[(:10, :10)]
