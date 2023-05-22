import os.path
import pytest
import numpy as np
from numpy import linalg
from numpy.testing import assert_allclose, assert_almost_equal
from unittest import mock
from . import irafutil
from astropy.modeling import models
from astropy.modeling.core import Fittable2DModel, Parameter
from astropy.modeling.fitting import SimplexLSQFitter, SLSQPLSQFitter, LinearLSQFitter, LevMarLSQFitter, JointFitter, Fitter, FittingWithOutlierRemoval
from astropy.utils import NumpyRNGContext
from astropy.utils.data import get_pkg_data_filename
from .utils import ignore_non_integer_warning
from astropy.stats import sigma_clip
from astropy.utils.exceptions import AstropyUserWarning
from astropy.modeling.fitting import populate_entry_points
import warnings
from scipy import optimize
from pkg_resources import EntryPoint
import scipy.stats as stats
import scipy.stats as stats


@pytest.mark.skipif('not HAS_SCIPY')
def test_chebyshev2D_nonlinear_fitting_with_weights(self):
    cheb2d = models.Chebyshev2D(2, 2)
    cheb2d.parameters = np.arange(9)
    z = cheb2d(self.x, self.y)
    cheb2d.parameters = [0.1, 0.6, 1.8, 2.9, 3.7, 4.9, 6.7, 7.5, 8.9]
    nlfitter = LevMarLSQFitter()
    weights = np.ones_like(self.y)
    with pytest.warns(AstropyUserWarning, match='Model is linear in parameters'):
        model = nlfitter(cheb2d, self.x, self.y, z, weights=weights)
    assert_allclose(model.parameters, [0, 1, 2, 3, 4, 5, 6, 7, 8], atol=(10 ** (- 9)))
