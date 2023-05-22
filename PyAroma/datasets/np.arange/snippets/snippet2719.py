import os
import sys
import numpy as np
import pytest
from fsps import StellarPopulation, filters
from numpy.testing import assert_allclose
import os
import os


def test_smooth_lsf(pop_and_params):
    (pop, params) = pop_and_params
    _reset_default_params(pop, params)
    tmax = 1.0
    wave_lsf = np.arange(4000, 7000.0, 10)
    x = ((wave_lsf - 5500) / 1500.0)
    sigma_lsf = (50 * ((1.0 + (0.4 * x)) + (0.6 * (x ** 2))))
    (w, spec) = pop.get_spectrum(tage=tmax)
    pop.params['smooth_lsf'] = True
    assert (pop.params.dirtiness == 2)
    pop.set_lsf(wave_lsf, sigma_lsf)
    (w, smspec) = pop.get_spectrum(tage=tmax)
    hi = (w > 7100)
    sm = ((w < 7000) & (w > 3000))
    assert np.allclose(((spec[hi] / smspec[hi]) - 1.0), 0.0)
    assert (not np.allclose(((spec[sm] / smspec[sm]) - 1.0), 0.0))
    pop.set_lsf(wave_lsf, (sigma_lsf * 2))
    assert (pop.params.dirtiness == 2)
