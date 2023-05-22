import pytest
import numpy as np
from numpy.testing import assert_allclose
from astropy.modeling import models
from astropy.modeling import fitting
from astropy.modeling.core import Model, FittableModel, Fittable1DModel
from astropy.modeling.parameters import Parameter
from scipy import optimize


def test_scalar_parameters_3d_array_input(self):
    '\n        The dimension of the input should match the number of models unless\n        model_set_axis=False is given, in which case the input is copied across\n        all models.\n        '
    t = TModel_1_1([1, 2], [10, 20], n_models=2)
    data = (np.arange(12).reshape(2, 3, 2) * 100)
    y1 = t(data)
    assert (np.shape(y1) == (2, 3, 2))
    assert np.all((y1 == [[[11, 111], [211, 311], [411, 511]], [[622, 722], [822, 922], [1022, 1122]]]))
    y2 = t(data, model_set_axis=False)
    assert (np.shape(y2) == (2, 2, 3, 2))
    assert np.all((y2 == np.array([(data + 11), (data + 22)])))
