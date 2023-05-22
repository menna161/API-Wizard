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


def test_param_cov(self):
    "\n        Tests that the 'param_cov' fit_info entry gets the right answer for\n        *linear* least squares, where the answer is exact\n        "
    a = 2
    b = 100
    with NumpyRNGContext(_RANDOM_SEED):
        x = np.linspace(0, 1, 100)
        y = (((x * a) + b) + np.random.randn(len(x)))
    X = np.vstack([x, np.ones(len(x))]).T
    beta = np.matmul(np.matmul(np.linalg.inv(np.matmul(X.T, X)), X.T), y.T)
    s2 = (np.sum(((y - np.matmul(X, beta).ravel()) ** 2)) / (len(y) - len(beta)))
    olscov = (np.linalg.inv(np.matmul(X.T, X)) * s2)
    mod = models.Linear1D(a, b)
    fitter = LevMarLSQFitter()
    with pytest.warns(AstropyUserWarning, match='Model is linear in parameters'):
        fmod = fitter(mod, x, y)
    assert_allclose(fmod.parameters, beta.ravel())
    assert_allclose(olscov, fitter.fit_info['param_cov'])
