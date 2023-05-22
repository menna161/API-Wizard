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


def test_linear_fit_2d_model_set(self):
    'Tests fitted multiple 2-D models simultaneously.'
    init_model = models.Polynomial2D(degree=2, c0_0=[1, 1], n_models=2)
    x = np.arange(10)
    y = np.arange(10)
    z_expected = init_model(x, y, model_set_axis=False)
    assert (z_expected.shape == (2, 10))
    with NumpyRNGContext(_RANDOM_SEED):
        z = (z_expected + np.random.normal(0, 0.01, size=z_expected.shape))
    fitter = LinearLSQFitter()
    with pytest.warns(AstropyUserWarning, match='The fit may be poorly conditioned'):
        fitted_model = fitter(init_model, x, y, z)
    assert_allclose(fitted_model(x, y, model_set_axis=False), z_expected, rtol=0.1)
