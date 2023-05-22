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


@pytest.mark.parametrize('Model', (models.Scale, models.Multiply))
def test_Scale_model_set_linear_fit(Model):
    'Test linear fitting of Scale model (#6103).'
    init_model = Model(factor=[0, 0], n_models=2)
    x = np.arange((- 3), 7)
    yy = np.array([(1.15 * x), (0.96 * x)])
    fitter = fitting.LinearLSQFitter()
    fitted_model = fitter(init_model, x, yy)
    assert_allclose(fitted_model.parameters, [1.15, 0.96], atol=1e-15)
