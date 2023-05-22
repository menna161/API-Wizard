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


def test_simplex_lsq_fitter(self):
    'A basic test for the `SimplexLSQ` fitter.'

    class Rosenbrock(Fittable2DModel):
        a = Parameter()
        b = Parameter()

        @staticmethod
        def evaluate(x, y, a, b):
            return (((a - x) ** 2) + (b * ((y - (x ** 2)) ** 2)))
    x = y = np.linspace((- 3.0), 3.0, 100)
    with NumpyRNGContext(_RANDOM_SEED):
        z = Rosenbrock.evaluate(x, y, 1.0, 100.0)
        z += np.random.normal(0.0, 0.1, size=z.shape)
    fitter = SimplexLSQFitter()
    r_i = Rosenbrock(1, 100)
    r_f = fitter(r_i, x, y, z)
    assert_allclose(r_f.parameters, [1.0, 100.0], rtol=0.01)
