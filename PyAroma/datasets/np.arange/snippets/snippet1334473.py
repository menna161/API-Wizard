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


def test_1d_set_fitting_with_outlier_removal():
    'Test model set fitting with outlier removal (issue #6819)'
    poly_set = models.Polynomial1D(2, n_models=2)
    fitter = FittingWithOutlierRemoval(LinearLSQFitter(), sigma_clip, sigma=2.5, niter=3, cenfunc=np.ma.mean, stdfunc=np.ma.std)
    x = np.arange(10)
    y = np.array([((2.5 * x) - 4), ((((2 * x) * x) + x) + 10)])
    y[(1, 5)] = (- 1000)
    (poly_set, filt_y) = fitter(poly_set, x, y)
    assert_allclose(poly_set.c0, [(- 4.0), 10.0], atol=1e-14)
    assert_allclose(poly_set.c1, [2.5, 1.0], atol=1e-14)
    assert_allclose(poly_set.c2, [0.0, 2.0], atol=1e-14)
