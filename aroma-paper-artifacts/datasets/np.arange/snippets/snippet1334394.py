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


@pytest.mark.skipif('not HAS_SCIPY_14')
def test_tabular_in_compound():
    '\n    Issue #7411 - evaluate should not change the shape of the output.\n    '
    t = Tabular1D(points=([1, 5, 7],), lookup_table=[12, 15, 19], bounds_error=False)
    rot = Rotation2D(2)
    p = Polynomial1D(1)
    x = np.arange(12).reshape((3, 4))
    model = ((p & t) | rot)
    (x1, y1) = model(x, x)
    assert (x1.ndim == 2)
    assert (y1.ndim == 2)
