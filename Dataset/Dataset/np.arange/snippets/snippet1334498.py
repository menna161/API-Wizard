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


def setup_class(self):
    self.initial_values = [100, 5, 1]
    self.xdata = np.arange(0, 10, 0.1)
    sigma = (4.0 * np.ones_like(self.xdata))
    with NumpyRNGContext(_RANDOM_SEED):
        yerror = np.random.normal(0, sigma)

    def func(p, x):
        return (p[0] * np.exp((((- 0.5) / (p[2] ** 2)) * ((x - p[1]) ** 2))))
    self.ydata = (func(self.initial_values, self.xdata) + yerror)
    self.gauss = models.Gaussian1D(100, 5, stddev=1)
