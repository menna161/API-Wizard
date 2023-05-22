import operator
import pytest
import numpy as np
from astropy.time import Time, TimeDelta


def setup(self):
    self.t1 = Time(np.arange(49995, 50005), format='mjd', scale='utc')
    self.t2 = Time(np.arange(49000, 51000, 200), format='mjd', scale='utc')
