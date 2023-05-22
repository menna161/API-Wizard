import itertools
import pytest
import numpy as np
from . import irafutil
from astropy.modeling import models, fitting
from astropy.modeling.core import Model, FittableModel
from astropy.modeling.parameters import Parameter, InputParameterError
from astropy.utils.data import get_pkg_data_filename


def test_single_model_scalar_and_array_parameters(self):
    t = TParModel(10, [1, 2])
    assert (len(t) == 1)
    assert (t.model_set_axis is False)
    assert np.issubdtype(t.param_sets.dtype, np.object_)
    assert (len(t.param_sets) == 2)
    assert np.all((t.param_sets[0] == [10]))
    assert np.all((t.param_sets[1] == [[1, 2]]))
    assert np.all((t.parameters == [10, 1, 2]))
    assert (t.coeff.shape == ())
    assert (t.e.shape == (2,))
