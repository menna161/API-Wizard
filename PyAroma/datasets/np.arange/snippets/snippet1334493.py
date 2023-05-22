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


def test_linear_fit_fixed_parameter(self):
    '\n        Tests fitting a polynomial model with a fixed parameter (issue #6135).\n        '
    init_model = models.Polynomial1D(degree=2, c1=1)
    init_model.c1.fixed = True
    x = np.arange(10)
    y = ((2 + x) + ((0.5 * x) * x))
    fitter = LinearLSQFitter()
    with pytest.warns(AstropyUserWarning, match='The fit may be poorly conditioned'):
        fitted_model = fitter(init_model, x, y)
    assert_allclose(fitted_model.parameters, [2.0, 1.0, 0.5], atol=1e-14)
