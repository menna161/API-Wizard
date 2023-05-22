import pytest
import numpy as np
from numpy.testing import assert_allclose
from astropy.modeling import models
from astropy.modeling import fitting
from astropy.modeling.core import Model, FittableModel, Fittable1DModel
from astropy.modeling.parameters import Parameter
from scipy import optimize


def test_scalar_parameters_2d_array_input(self):
    '\n        Scalar parameters should broadcast with an array input to result in an\n        array output of the same shape as the input.\n        '
    t = TModel_1_1(1, 10)
    y = t((np.arange(6).reshape(2, 3) * 100))
    assert isinstance(y, np.ndarray)
    assert (np.shape(y) == (2, 3))
    assert np.all((y == [[11, 111, 211], [311, 411, 511]]))
