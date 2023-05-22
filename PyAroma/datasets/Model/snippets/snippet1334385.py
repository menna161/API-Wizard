import pytest
import pickle
from copy import deepcopy
import numpy as np
from numpy.testing import assert_allclose, assert_array_equal
from astropy.utils import minversion
from astropy.modeling.core import Model, ModelDefinitionError, CompoundModel
from astropy.modeling.parameters import Parameter
from astropy.modeling.models import Const1D, Shift, Scale, Rotation2D, Gaussian1D, Gaussian2D, Polynomial1D, Polynomial2D, Chebyshev2D, Legendre2D, Chebyshev1D, Legendre1D, Identity, Mapping, Tabular1D, fix_inputs
import astropy.units as u
from ..core import CompoundModel
import scipy


def test_fix_inputs_invalid():
    g1 = Gaussian2D(1, 0, 0, 1, 2)
    with pytest.raises(ValueError):
        fix_inputs(g1, {'x0': 0, 0: 0})
    with pytest.raises(ValueError):
        fix_inputs(g1, (0, 1))
    with pytest.raises(ValueError):
        fix_inputs(g1, {3: 2})
    with pytest.raises(ValueError):
        fix_inputs(g1, {'w': 2})
    with pytest.raises(ModelDefinitionError):
        CompoundModel('#', g1, g1)
    with pytest.raises(ValueError):
        gg1 = fix_inputs(g1, {0: 1})
        gg1(2, y=2)
