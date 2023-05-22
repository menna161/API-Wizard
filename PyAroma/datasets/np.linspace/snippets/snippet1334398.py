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


@pytest.mark.parametrize('poly', [Chebyshev1D(5), Legendre1D(5), Polynomial1D(5)])
def test_compound_with_polynomials_1d(poly):
    '\n    Tests that polynomials are offset when used in compound models.\n    Issue #3699\n    '
    poly.parameters = [1, 2, 3, 4, 1, 2]
    shift = Shift(3)
    model = (poly | shift)
    x = np.linspace((- 5), 5, 10)
    result_compound = model(x)
    result = shift(poly(x))
    assert_allclose(result, result_compound)
    assert (model.param_names == ('c0_0', 'c1_0', 'c2_0', 'c3_0', 'c4_0', 'c5_0', 'offset_1'))
