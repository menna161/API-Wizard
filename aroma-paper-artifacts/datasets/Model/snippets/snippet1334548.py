import pytest
import numpy as np
from numpy.testing import assert_allclose, assert_array_equal, assert_array_less
from astropy.modeling import models, InputParameterError
from astropy.coordinates import Angle
from astropy.modeling import fitting
from astropy.utils.exceptions import AstropyDeprecationWarning, AstropyUserWarning
from scipy import optimize
from astropy.stats.funcs import gaussian_sigma_to_fwhm
from astropy.modeling.functional_models import GAUSSIAN_SIGMA_TO_FWHM


def test_RedshiftScaleFactor():
    'Like ``test_ScaleModel()``.'
    m = models.RedshiftScaleFactor(0.4)
    assert (m(0) == 0)
    assert_array_equal(m([1, 2]), [1.4, 2.8])
    assert_allclose(m.inverse(m([1, 2])), [1, 2])
    m = models.RedshiftScaleFactor([(- 0.5), 0, 0.5], n_models=3)
    assert_array_equal(m(0), 0)
    assert_array_equal(m([1, 2], model_set_axis=False), [[0.5, 1], [1, 2], [1.5, 3]])
    assert_allclose(m.inverse(m([1, 2], model_set_axis=False)), [[1, 2], [1, 2], [1, 2]])
