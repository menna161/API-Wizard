import itertools
import pytest
import numpy as np
from . import irafutil
from astropy.modeling import models, fitting
from astropy.modeling.core import Model, FittableModel
from astropy.modeling.parameters import Parameter, InputParameterError
from astropy.utils.data import get_pkg_data_filename


def test_single_model_2d_array_parameters(self):
    t = TParModel([[10, 20], [30, 40]], [[1, 2], [3, 4]])
    assert (len(t) == 1)
    assert (t.model_set_axis is False)
    assert np.all((t.param_sets == [[[[10, 20], [30, 40]]], [[[1, 2], [3, 4]]]]))
    assert np.all((t.parameters == [10, 20, 30, 40, 1, 2, 3, 4]))
    assert (t.coeff.shape == (2, 2))
    assert (t.e.shape == (2, 2))
