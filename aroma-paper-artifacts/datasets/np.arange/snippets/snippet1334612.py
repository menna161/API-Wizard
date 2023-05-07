import pytest
import numpy as np
from numpy.testing import assert_allclose
from astropy.modeling import models
from astropy.modeling import fitting
from astropy.modeling.core import Model, FittableModel, Fittable1DModel
from astropy.modeling.parameters import Parameter
from scipy import optimize


def test_scalar_parameters_1d_array_input(self):
    '\n        Scalar parameters should broadcast with an array input to result in an\n        array output of the same shape as the input.\n        '
    t = TModel_1_2(1, 10, 1000)
    (y, z) = t((np.arange(5) * 100))
    assert isinstance(y, np.ndarray)
    assert isinstance(z, np.ndarray)
    assert (np.shape(y) == np.shape(z) == (5,))
    assert np.all((y == [11, 111, 211, 311, 411]))
    assert np.all((z == (y + 1000)))
