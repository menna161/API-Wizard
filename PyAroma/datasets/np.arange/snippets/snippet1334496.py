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


def test_linear_fit_model_set_masked_values(self):
    '\n        Tests model set fitting with masked value(s) (#4824, #6819).\n        '
    init_model = models.Polynomial1D(degree=1, n_models=2)
    x = np.arange(10)
    y = np.ma.masked_array([((2 * x) + 1), (x - 2)], mask=np.zeros_like([x, x]))
    y[(0, 7)] = 100.0
    y.mask[(0, 7)] = True
    y[(1, 1:3)] = (- 100.0)
    y.mask[(1, 1:3)] = True
    fitter = LinearLSQFitter()
    fitted_model = fitter(init_model, x, y)
    assert_allclose(fitted_model.c0, [1.0, (- 2.0)], atol=1e-14)
    assert_allclose(fitted_model.c1, [2.0, 1.0], atol=1e-14)
