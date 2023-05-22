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


def test_compound_model_raises_error(self):
    'Test that if an user tries to use a compound model, raises an error'
    with pytest.raises(ValueError) as excinfo:
        init_model1 = models.Polynomial1D(degree=2, c0=[1, 1], n_models=2)
        init_model2 = models.Polynomial1D(degree=2, c0=[1, 1], n_models=2)
        init_model_comp = (init_model1 + init_model2)
        x = np.arange(10)
        y = init_model_comp(x, model_set_axis=False)
        fitter = LinearLSQFitter()
        _ = fitter(init_model_comp, x, y)
    assert ('Model must be simple, not compound' in str(excinfo.value))
