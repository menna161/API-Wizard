import itertools
import pytest
import numpy as np
from . import irafutil
from astropy.modeling import models, fitting
from astropy.modeling.core import Model, FittableModel
from astropy.modeling.parameters import Parameter, InputParameterError
from astropy.utils.data import get_pkg_data_filename


@pytest.mark.parametrize('kwargs', [{'n_models': 2}, {'model_set_axis': 0}, {'n_models': 2, 'model_set_axis': 0}])
def test_two_model_scalar_parameters(self, kwargs):
    t = TParModel([10, 20], [1, 2], **kwargs)
    assert (len(t) == 2)
    assert (t.model_set_axis == 0)
    assert np.all((t.param_sets == [[10, 20], [1, 2]]))
    assert np.all((t.parameters == [10, 20, 1, 2]))
    assert (t.coeff.shape == (2,))
    assert (t.e.shape == (2,))
