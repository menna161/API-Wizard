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
@pytest.mark.filterwarnings('ignore:The fit may be unsuccessful')
def test_fitters_interface():
    '\n    Test that **kwargs work with all optimizers.\n    This is a basic smoke test.\n    '
    levmar = LevMarLSQFitter()
    slsqp = SLSQPLSQFitter()
    simplex = SimplexLSQFitter()
    kwargs = {'maxiter': 77, 'verblevel': 1, 'epsilon': 0.01, 'acc': 1e-06}
    simplex_kwargs = {'maxiter': 77, 'verblevel': 1, 'acc': 1e-06}
    model = models.Gaussian1D(10, 4, 0.3)
    x = np.arange(21)
    y = model(x)
    _ = slsqp(model, x, y, **kwargs)
    _ = simplex(model, x, y, **simplex_kwargs)
    kwargs.pop('verblevel')
    _ = levmar(model, x, y, **kwargs)
