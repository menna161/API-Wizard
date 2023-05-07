import itertools
import pytest
import numpy as np
from . import irafutil
from astropy.modeling import models, fitting
from astropy.modeling.core import Model, FittableModel
from astropy.modeling.parameters import Parameter, InputParameterError
from astropy.utils.data import get_pkg_data_filename


def test_two_model_mixed_dimension_array_parameters(self):
    with pytest.raises(InputParameterError):
        TParModel([[[1, 2], [3, 4]], [[5, 6], [7, 8]]], [[9, 10, 11], [12, 13, 14]], n_models=2)
    t = TParModel([[[10, 20], [30, 40]], [[50, 60], [70, 80]]], [[1, 2], [3, 4]], n_models=2)
    assert (len(t) == 2)
    assert (t.model_set_axis == 0)
    assert (len(t.param_sets) == 2)
    assert np.issubdtype(t.param_sets.dtype, np.object_)
    assert np.all((t.param_sets[0] == [[[10, 20], [30, 40]], [[50, 60], [70, 80]]]))
    assert np.all((t.param_sets[1] == [[[1, 2]], [[3, 4]]]))
    assert np.all((t.parameters == [10, 20, 30, 40, 50, 60, 70, 80, 1, 2, 3, 4]))
    assert (t.coeff.shape == (2, 2, 2))
    assert (t.e.shape == (2, 2))
