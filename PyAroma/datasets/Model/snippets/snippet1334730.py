import itertools
import pytest
import numpy as np
from . import irafutil
from astropy.modeling import models, fitting
from astropy.modeling.core import Model, FittableModel
from astropy.modeling.parameters import Parameter, InputParameterError
from astropy.utils.data import get_pkg_data_filename


def test_single_model_2d_non_square_parameters(self):
    coeff = np.array([[10, 20], [30, 40], [50, 60]])
    e = np.array([[1, 2], [3, 4], [5, 6]])
    t = TParModel(coeff, e)
    assert (len(t) == 1)
    assert (t.model_set_axis is False)
    assert np.all((t.param_sets == [[[[10, 20], [30, 40], [50, 60]]], [[[1, 2], [3, 4], [5, 6]]]]))
    assert np.all((t.parameters == [10, 20, 30, 40, 50, 60, 1, 2, 3, 4, 5, 6]))
    assert (t.coeff.shape == (3, 2))
    assert (t.e.shape == (3, 2))
    t2 = TParModel(coeff.T, e.T)
    assert (len(t2) == 1)
    assert (t2.model_set_axis is False)
    assert np.all((t2.param_sets == [[[[10, 30, 50], [20, 40, 60]]], [[[1, 3, 5], [2, 4, 6]]]]))
    assert np.all((t2.parameters == [10, 30, 50, 20, 40, 60, 1, 3, 5, 2, 4, 6]))
    assert (t2.coeff.shape == (2, 3))
    assert (t2.e.shape == (2, 3))
    with pytest.raises(InputParameterError):
        TParModel(coeff, e.T)
    with pytest.raises(InputParameterError):
        TParModel(coeff.T, e)
