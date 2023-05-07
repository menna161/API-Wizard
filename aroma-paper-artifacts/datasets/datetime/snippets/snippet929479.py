import datetime
import nose
from traces import TimeSeries
from traces.decorators import ignorant, strict


def test_scalar_ops():
    a = TimeSeries()
    a.set(datetime.datetime(2015, 3, 1), 1)
    a.set(datetime.datetime(2015, 3, 2), 0)
    a.set(datetime.datetime(2015, 3, 3), 3)
    a.set(datetime.datetime(2015, 3, 4), 2)
    ts_half = a.multiply(0.5)
    ts_bool = a.to_bool(invert=False)
    ts_threshold = a.threshold(value=1.1)
    assert (ts_half[datetime.datetime(2015, 2, 24)] is None)
    assert (ts_bool[datetime.datetime(2015, 2, 24)] is None)
    assert (ts_threshold[datetime.datetime(2015, 2, 24)] is None)
    assert (ts_half[datetime.datetime(2015, 3, 1, 6)] == 0.5)
    assert (ts_bool[datetime.datetime(2015, 3, 1, 6)] is True)
    assert (ts_threshold[datetime.datetime(2015, 3, 1, 6)] is False)
    assert (ts_half[datetime.datetime(2015, 3, 2, 6)] == 0)
    assert (ts_bool[datetime.datetime(2015, 3, 2, 6)] is False)
    assert (ts_threshold[datetime.datetime(2015, 3, 2, 6)] is False)
    assert (ts_half[datetime.datetime(2015, 3, 3, 6)] == 1.5)
    assert (ts_bool[datetime.datetime(2015, 3, 3, 6)] is True)
    assert (ts_threshold[datetime.datetime(2015, 3, 3, 6)] is True)
    assert (ts_half[datetime.datetime(2015, 3, 4, 18)] == 1)
    assert (ts_bool[datetime.datetime(2015, 3, 4, 18)] is True)
    assert (ts_threshold[datetime.datetime(2015, 3, 4, 18)] is True)
