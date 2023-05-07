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
def test_bounding_box_with_units():
    points = (np.arange(5) * u.pix)
    lt = (np.arange(5) * u.AA)
    t = Tabular1D(points, lt)
    assert (t((1 * u.pix), with_bounding_box=True) == (1.0 * u.AA))
