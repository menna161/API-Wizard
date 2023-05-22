import pytest
import numpy as np
from numpy.testing import assert_allclose, assert_array_equal
from astropy.modeling.fitting import LevMarLSQFitter
from astropy.modeling.models import Shift, Rotation2D, Gaussian1D, Identity, Mapping
from astropy.utils import NumpyRNGContext
from scipy import optimize


@pytest.mark.skipif('not HAS_SCIPY')
def test_fittable_compound():
    m = ((Identity(1) | Mapping((0,))) | Gaussian1D(1, 5, 4))
    x = np.arange(10)
    y_real = m(x)
    dy = 0.005
    with NumpyRNGContext(1234567):
        n = np.random.normal(0.0, dy, x.shape)
    y_noisy = (y_real + n)
    pfit = LevMarLSQFitter()
    new_model = pfit(m, x, y_noisy)
    y_fit = new_model(x)
    assert_allclose(y_fit, y_real, atol=dy)
