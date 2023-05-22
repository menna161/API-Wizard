import warnings
import itertools
import copy
import pytest
import numpy as np
from astropy.time import Time
from astropy.utils import iers


def setup(self):
    mjd = np.arange(50000, 50010)
    frac = np.arange(0.0, 0.999, 0.2)
    if use_masked_data:
        frac = np.ma.array(frac)
        frac[1] = np.ma.masked
    self.t0 = Time((mjd[(:, np.newaxis)] + frac), format='mjd', scale='utc')
    self.t1 = Time((mjd[(:, np.newaxis)] + frac), format='mjd', scale='utc', location=('45d', '50d'))
    self.t2 = Time((mjd[(:, np.newaxis)] + frac), format='mjd', scale='utc', location=(np.arange(len(frac)), np.arange(len(frac))))
    self.t2 = Time((mjd[(:, np.newaxis)] + frac), format='mjd', scale='utc', location=(np.arange(len(frac)), np.arange(len(frac))))
