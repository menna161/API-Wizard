import itertools
import pytest
import numpy as np
from . import irafutil
from astropy.modeling import models, fitting
from astropy.modeling.core import Model, FittableModel
from astropy.modeling.parameters import Parameter, InputParameterError
from astropy.utils.data import get_pkg_data_filename


def test_array_parameter4(self):
    '\n        Test multiple parameter model with array-valued parameters of the same\n        size as the number of parameter sets.\n        '
    t4 = TParModel([[1, 2], [3, 4]], [5, 6], model_set_axis=False)
    assert (len(t4) == 1)
    assert (t4.coeff.shape == (2, 2))
    assert (t4.e.shape == (2,))
    assert np.issubdtype(t4.param_sets.dtype, np.object_)
    assert np.all((t4.param_sets[0] == [[1, 2], [3, 4]]))
    assert np.all((t4.param_sets[1] == [5, 6]))
