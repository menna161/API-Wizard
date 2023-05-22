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
    '\n        Create 2 gaussian models and some data with noise.\n        Create a fitter for the two models keeping the amplitude parameter\n        common for the two models.\n        '
    self.g1 = models.Gaussian1D(10, mean=14.9, stddev=0.3)
    self.g2 = models.Gaussian1D(10, mean=13, stddev=0.4)
    self.jf = JointFitter([self.g1, self.g2], {self.g1: ['amplitude'], self.g2: ['amplitude']}, [9.8])
    self.x = np.arange(10, 20, 0.1)
    y1 = self.g1(self.x)
    y2 = self.g2(self.x)
    with NumpyRNGContext(_RANDOM_SEED):
        n = np.random.randn(100)
    self.ny1 = (y1 + (2 * n))
    self.ny2 = (y2 + (2 * n))
    self.jf(self.x, self.ny1, self.x, self.ny2)
