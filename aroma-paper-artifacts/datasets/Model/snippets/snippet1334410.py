import types
import pytest
import numpy as np
from numpy.testing import assert_allclose
from numpy.random import RandomState
from astropy.modeling.core import Fittable1DModel
from astropy.modeling.parameters import Parameter
from astropy.modeling import models
from astropy.modeling import fitting
from astropy.utils.exceptions import AstropyUserWarning
from .utils import ignore_non_integer_warning
from scipy import optimize
from astropy.utils import NumpyRNGContext


def test_default_constraints():
    'Regression test for https://github.com/astropy/astropy/issues/2396\n\n    Ensure that default constraints defined on parameters are carried through\n    to instances of the models those parameters are defined for.\n    '

    class MyModel(Fittable1DModel):
        a = Parameter(default=1)
        b = Parameter(default=0, min=0, fixed=True)

        @staticmethod
        def evaluate(x, a, b):
            return ((x * a) + b)
    assert (MyModel.a.default == 1)
    assert (MyModel.b.default == 0)
    assert (MyModel.b.min == 0)
    assert (MyModel.b.bounds == (0, None))
    assert (MyModel.b.fixed is True)
    m = MyModel()
    assert (m.a.value == 1)
    assert (m.b.value == 0)
    assert (m.b.min == 0)
    assert (m.b.bounds == (0, None))
    assert (m.b.fixed is True)
    assert (m.bounds == {'a': (None, None), 'b': (0, None)})
    assert (m.fixed == {'a': False, 'b': True})
    m = MyModel(3, 4, bounds={'a': (1, None), 'b': (2, None)}, fixed={'a': True, 'b': False})
    assert (m.a.value == 3)
    assert (m.b.value == 4)
    assert (m.a.min == 1)
    assert (m.b.min == 2)
    assert (m.a.bounds == (1, None))
    assert (m.b.bounds == (2, None))
    assert (m.a.fixed is True)
    assert (m.b.fixed is False)
    assert (m.bounds == {'a': (1, None), 'b': (2, None)})
    assert (m.fixed == {'a': True, 'b': False})
