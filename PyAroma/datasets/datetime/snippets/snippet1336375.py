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


def test_pandas():
    pandas = pytest.importorskip('pandas')
    df1 = pandas.DataFrame()
    df1['a'] = [1, 2, 3]
    df1.set_index(pandas.DatetimeIndex(INPUT_TIME.datetime64), inplace=True)
    ts = TimeSeries.from_pandas(df1)
    assert_equal(ts.time.isot, INPUT_TIME.isot)
    assert (ts.colnames == ['time', 'a'])
    assert (len(ts.indices) == 1)
    assert (ts.indices['time'].columns[0] == INPUT_TIME).all()
    ts_tcb = TimeSeries.from_pandas(df1, time_scale='tcb')
    assert (ts_tcb.time.scale == 'tcb')
    df2 = ts.to_pandas()
    assert (df2.index.values == pandas.Index(INPUT_TIME.datetime64).values).all()
    assert (df2.columns == pandas.Index(['a']))
    assert (df1['a'] == df2['a']).all()
    with pytest.raises(TypeError) as exc:
        TimeSeries.from_pandas(None)
    assert (exc.value.args[0] == 'Input should be a pandas DataFrame')
    df4 = pandas.DataFrame()
    df4['a'] = [1, 2, 3]
    with pytest.raises(TypeError) as exc:
        TimeSeries.from_pandas(df4)
    assert (exc.value.args[0] == 'DataFrame does not have a DatetimeIndex')
