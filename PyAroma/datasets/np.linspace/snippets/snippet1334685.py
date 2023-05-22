from collections import OrderedDict
import pytest
import numpy as np
from astropy import units as u
from astropy.tests.helper import assert_quantity_allclose
from astropy.modeling.functional_models import Gaussian1D, Sersic1D, Sine1D, Linear1D, Lorentz1D, Voigt1D, Const1D, Box1D, Trapezoid1D, RickerWavelet1D, Moffat1D, Gaussian2D, Const2D, Ellipse2D, Disk2D, Ring2D, Box2D, TrapezoidDisk2D, RickerWavelet2D, AiryDisk2D, Moffat2D, Sersic2D, KingProjectedAnalytic1D
from astropy.modeling.powerlaws import PowerLaw1D, BrokenPowerLaw1D, SmoothlyBrokenPowerLaw1D, ExponentialCutoffPowerLaw1D, LogParabola1D
from astropy.modeling.polynomial import Polynomial1D, Polynomial2D
from astropy.modeling.fitting import LevMarLSQFitter
from scipy import optimize


@pytest.mark.skipif('not HAS_SCIPY')
@pytest.mark.filterwarnings('ignore:.*:RuntimeWarning')
@pytest.mark.filterwarnings('ignore:Model is linear in parameters.*')
@pytest.mark.filterwarnings('ignore:The fit may be unsuccessful.*')
@pytest.mark.parametrize('model', MODELS)
def test_models_fitting(model):
    m = model['class'](**model['parameters'])
    if (len(model['evaluation'][0]) == 2):
        x = (np.linspace(1, 3, 100) * model['evaluation'][0][0].unit)
        y = (np.exp((- (x.value ** 2))) * model['evaluation'][0][1].unit)
        args = [x, y]
    else:
        x = (np.linspace(1, 3, 100) * model['evaluation'][0][0].unit)
        y = (np.linspace(1, 3, 100) * model['evaluation'][0][1].unit)
        z = (np.exp(((- (x.value ** 2)) - (y.value ** 2))) * model['evaluation'][0][2].unit)
        args = [x, y, z]
    fitter = LevMarLSQFitter()
    m_new = fitter(m, *args)
    for param_name in m.param_names:
        par_bef = getattr(m, param_name)
        par_aft = getattr(m_new, param_name)
        if (par_bef.unit is None):
            assert ((par_aft.unit is None) or (par_aft.unit is u.rad))
        else:
            assert par_aft.unit.is_equivalent(par_bef.unit)
