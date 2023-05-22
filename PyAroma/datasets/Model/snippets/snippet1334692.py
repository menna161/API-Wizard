import itertools
import pytest
import numpy as np
from . import irafutil
from astropy.modeling import models, fitting
from astropy.modeling.core import Model, FittableModel
from astropy.modeling.parameters import Parameter, InputParameterError
from astropy.utils.data import get_pkg_data_filename


def test_non_broadcasting_parameters():
    '\n    Tests that in a model with 3 parameters that do not all mutually broadcast,\n    this is determined correctly regardless of what order the parameters are\n    in.\n    '
    a = 3
    b = np.array([[1, 2, 3], [4, 5, 6]])
    c = np.array([[1, 2, 3, 4], [1, 2, 3, 4]])

    class TestModel(Model):
        p1 = Parameter()
        p2 = Parameter()
        p3 = Parameter()

        def evaluate(self, *args):
            return
    for args in itertools.permutations((a, b, c)):
        with pytest.raises(InputParameterError):
            TestModel(*args)
