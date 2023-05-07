import itertools
import pytest
import numpy as np
from . import irafutil
from astropy.modeling import models, fitting
from astropy.modeling.core import Model, FittableModel
from astropy.modeling.parameters import Parameter, InputParameterError
from astropy.utils.data import get_pkg_data_filename


@pytest.mark.parametrize('kwargs', [{'n_models': 2}, {'model_set_axis': 0}, {'n_models': 2, 'model_set_axis': 0}])
def test_two_model_scalar_and_array_parameters(self, kwargs):
    t = TParModel([10, 20], [[1, 2], [3, 4]], **kwargs)
    assert (len(t) == 2)
    assert (t.model_set_axis == 0)
    assert (len(t.param_sets) == 2)
    assert np.issubdtype(t.param_sets.dtype, np.object_)
    assert np.all((t.param_sets[0] == [[10], [20]]))
    assert np.all((t.param_sets[1] == [[1, 2], [3, 4]]))
    assert np.all((t.parameters == [10, 20, 1, 2, 3, 4]))
    assert (t.coeff.shape == (2,))
    assert (t.e.shape == (2, 2))
