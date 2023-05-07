import itertools
import pytest
import numpy as np
from . import irafutil
from astropy.modeling import models, fitting
from astropy.modeling.core import Model, FittableModel
from astropy.modeling.parameters import Parameter, InputParameterError
from astropy.utils.data import get_pkg_data_filename


def test_two_model_nonzero_model_set_axis(self):
    coeff = np.array([[[10, 20, 30], [30, 40, 50]], [[50, 60, 70], [70, 80, 90]]])
    coeff = np.rollaxis(coeff, 0, 3)
    e = np.array([[1, 2, 3], [3, 4, 5]])
    e = np.rollaxis(e, 0, 2)
    t = TParModel(coeff, e, n_models=2, model_set_axis=(- 1))
    assert (len(t) == 2)
    assert (t.model_set_axis == (- 1))
    assert (len(t.param_sets) == 2)
    assert np.issubdtype(t.param_sets.dtype, np.object_)
    assert np.all((t.param_sets[0] == [[[10, 50], [20, 60], [30, 70]], [[30, 70], [40, 80], [50, 90]]]))
    assert np.all((t.param_sets[1] == [[[1, 3], [2, 4], [3, 5]]]))
    assert np.all((t.parameters == [10, 50, 20, 60, 30, 70, 30, 70, 40, 80, 50, 90, 1, 3, 2, 4, 3, 5]))
    assert (t.coeff.shape == (2, 3, 2))
    assert (t.e.shape == (3, 2))
