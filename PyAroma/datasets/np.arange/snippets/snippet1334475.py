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
def test_fitters_with_weights():
    'Issue #5737 '
    (Xin, Yin) = np.mgrid[(0:21, 0:21)]
    fitter = LevMarLSQFitter()
    with NumpyRNGContext(_RANDOM_SEED):
        zsig = np.random.normal(0, 0.01, size=Xin.shape)
    g2 = models.Gaussian2D(10, 10, 9, 2, 3)
    z = g2(Xin, Yin)
    gmod = fitter(models.Gaussian2D(15, 7, 8, 1.3, 1.2), Xin, Yin, (z + zsig))
    assert_allclose(gmod.parameters, g2.parameters, atol=(10 ** (- 2)))
    p2 = models.Polynomial2D(3)
    p2.parameters = (np.arange(10) / 1.2)
    z = p2(Xin, Yin)
    with pytest.warns(AstropyUserWarning, match='Model is linear in parameters'):
        pmod = fitter(models.Polynomial2D(3), Xin, Yin, (z + zsig))
    assert_allclose(pmod.parameters, p2.parameters, atol=(10 ** (- 2)))
