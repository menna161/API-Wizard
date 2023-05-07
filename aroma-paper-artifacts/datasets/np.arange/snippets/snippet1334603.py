import pytest
import numpy as np
from numpy.testing import assert_allclose
from astropy.modeling import models
from astropy.modeling import fitting
from astropy.modeling.core import Model, FittableModel, Fittable1DModel
from astropy.modeling.parameters import Parameter
from scipy import optimize


def test_scalar_parameters_1d_array_input(self):
    '\n        The dimension of the input should match the number of models unless\n        model_set_axis=False is given, in which case the input is copied across\n        all models.\n        '
    t = TModel_1_1([1, 2], [10, 20], n_models=2)
    with pytest.raises(ValueError):
        y = t((np.arange(5) * 100))
    y1 = t([100, 200])
    assert (np.shape(y1) == (2,))
    assert np.all((y1 == [111, 222]))
    y2 = t([100, 200], model_set_axis=False)
    assert (np.shape(y2) == (2, 2))
    assert np.all((y2 == [[111, 211], [122, 222]]))
    y3 = t([100, 200, 300], model_set_axis=False)
    assert (np.shape(y3) == (2, 3))
    assert np.all((y3 == [[111, 211, 311], [122, 222, 322]]))
