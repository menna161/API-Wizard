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


def test_linear_fit_model_set(self):
    'Tests fitting multiple models simultaneously.'
    init_model = models.Polynomial1D(degree=2, c0=[1, 1], n_models=2)
    x = np.arange(10)
    y_expected = init_model(x, model_set_axis=False)
    assert (y_expected.shape == (2, 10))
    with NumpyRNGContext(_RANDOM_SEED):
        y = (y_expected + np.random.normal(0, 0.01, size=y_expected.shape))
    fitter = LinearLSQFitter()
    fitted_model = fitter(init_model, x, y)
    assert_allclose(fitted_model(x, model_set_axis=False), y_expected, rtol=0.1)
