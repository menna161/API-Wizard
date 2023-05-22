import functools
import itertools
import operator
from decimal import Decimal
from datetime import timedelta
import pytest
import numpy as np
from astropy.time import Time, TimeDelta, OperandTypeError, ScaleValueError, TIME_SCALES, STANDARD_TIME_SCALES, TIME_DELTA_SCALES
from astropy.utils import iers
from astropy import units as u


def setup(self):
    self.t = Time('2010-01-01', scale='utc')
    self.t2 = Time('2010-01-02 00:00:01', scale='utc')
    self.t3 = Time('2010-01-03 01:02:03', scale='utc', precision=9, in_subfmt='date_hms', out_subfmt='date_hm', location=(((- 75.0) * u.degree), (30.0 * u.degree), (500 * u.m)))
    self.t4 = Time('2010-01-01', scale='local')
    self.dt = TimeDelta(100.0, format='sec')
    self.dt_array = TimeDelta(np.arange(100, 1000, 100), format='sec')
