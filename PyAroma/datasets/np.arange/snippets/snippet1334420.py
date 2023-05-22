import types
import pytest
import numpy as np
from numpy.testing import assert_allclose
from numpy.random import RandomState
from astropy.modeling.core import Fittable1DModel
from astropy.modeling.parameters import Parameter
from astropy.modeling import models
from astropy.modeling import fitting
from astropy.utils.exceptions import AstropyUserWarning
from .utils import ignore_non_integer_warning
from scipy import optimize
from astropy.utils import NumpyRNGContext


@pytest.mark.skipif('not HAS_SCIPY')
def test_joint_fitter(self):
    g1 = models.Gaussian1D(10, 14.9, stddev=0.3)
    g2 = models.Gaussian1D(10, 13, stddev=0.4)
    jf = fitting.JointFitter([g1, g2], {g1: ['amplitude'], g2: ['amplitude']}, [9.8])
    x = np.arange(10, 20, 0.1)
    y1 = g1(x)
    y2 = g2(x)
    n = np.random.randn(100)
    ny1 = (y1 + (2 * n))
    ny2 = (y2 + (2 * n))
    jf(x, ny1, x, ny2)
    p1 = [14.9, 0.3]
    p2 = [13, 0.4]
    A = 9.8
    p = np.r_[(A, p1, p2)]

    def compmodel(A, p, x):
        return (A * np.exp((((- 0.5) / (p[1] ** 2)) * ((x - p[0]) ** 2))))

    def errf(p, x1, y1, x2, y2):
        return np.ravel(np.r_[((compmodel(p[0], p[1:3], x1) - y1), (compmodel(p[0], p[3:], x2) - y2))])
    (fitparams, _) = optimize.leastsq(errf, p, args=(x, ny1, x, ny2))
    assert_allclose(jf.fitparams, fitparams, rtol=(10 ** (- 5)))
    assert_allclose(g1.amplitude.value, g2.amplitude.value)
