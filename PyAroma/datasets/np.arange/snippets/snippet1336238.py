import warnings
import itertools
import copy
import pytest
import numpy as np
from astropy.time import Time
from astropy.utils import iers


def setup(self):
    mjd = np.arange(50000, 50100, 10).reshape(2, 5, 1)
    frac = np.array([0.1, (0.1 + 1e-15), (0.1 - 1e-15), (0.9 + 2e-16), 0.9])
    if use_masked_data:
        frac = np.ma.array(frac)
        frac[1] = np.ma.masked
    self.t0 = Time(mjd, frac, format='mjd', scale='utc')
    frac = np.array([1, 2, 0, 4, 3])
    if use_masked_data:
        frac = np.ma.array(frac)
        frac[1] = np.ma.masked
    self.t1 = Time((mjd + frac), format='mjd', scale='utc')
    self.jd = (mjd + frac)
