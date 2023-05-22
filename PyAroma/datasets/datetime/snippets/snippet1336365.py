from datetime import datetime
import pytest
from numpy.testing import assert_equal, assert_allclose
from astropy.table import Table, Column
from astropy.time import Time, TimeDelta
from astropy import units as u
from astropy.units import Quantity
from astropy.utils.data import get_pkg_data_filename
from astropy.tests.helper import assert_quantity_allclose
from astropy.timeseries.periodograms import BoxLeastSquares, LombScargle
from astropy.timeseries.sampled import TimeSeries


def test_initialization_with_time_delta():
    ts = TimeSeries(time_start=datetime(2018, 7, 1, 10, 10, 10), time_delta=TimeDelta(3, format='sec'), data=[[10, 2, 3], [4, 5, 6]], names=['a', 'b'])
    assert_equal(ts.time.isot, ['2018-07-01T10:10:10.000', '2018-07-01T10:10:13.000', '2018-07-01T10:10:16.000'])
