import itertools
import pytest
import numpy as np
from . import irafutil
from astropy.modeling import models, fitting
from astropy.modeling.core import Model, FittableModel
from astropy.modeling.parameters import Parameter, InputParameterError
from astropy.utils.data import get_pkg_data_filename


def test_setter():
    pars = np.random.rand(20).reshape((10, 2))
    model = SetterModel(xc=(- 1), yc=3, p=np.pi)
    for (x, y) in pars:
        np.testing.assert_almost_equal(model(x, y), (((x + 1) ** 2) + ((y - (np.pi * 3)) ** 2)))
