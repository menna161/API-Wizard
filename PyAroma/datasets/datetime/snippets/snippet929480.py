import datetime
import nose
from traces import TimeSeries
from traces.decorators import ignorant, strict


def test_sum():
    a = TimeSeries()
    a.set(datetime.datetime(2015, 3, 1), 1)
    a.set(datetime.datetime(2015, 3, 2), 0)
    a.set(datetime.datetime(2015, 3, 3), 1)
    a.set(datetime.datetime(2015, 3, 4), 0)
    b = TimeSeries()
    b.set(datetime.datetime(2015, 3, 1), 0)
    b.set(datetime.datetime(2015, 3, 1, 12), 1)
    b.set(datetime.datetime(2015, 3, 2), 0)
    b.set(datetime.datetime(2015, 3, 2, 12), 1)
    b.set(datetime.datetime(2015, 3, 3), 0)
    c = TimeSeries()
    c.set(datetime.datetime(2015, 3, 1), 0)
    c.set(datetime.datetime(2015, 3, 1, 18), 1)
    c.set(datetime.datetime(2015, 3, 5), 0)
    ts_sum = TimeSeries.merge([a, b, c], operation=ignorant(sum))
    assert (ts_sum[datetime.datetime(2015, 2, 24)] == 0)
    assert (ts_sum[datetime.datetime(2015, 3, 1)] == 1)
    assert (ts_sum[datetime.datetime(2015, 3, 1, 6)] == 1)
    assert (ts_sum[datetime.datetime(2015, 3, 1, 12)] == 2)
    assert (ts_sum[datetime.datetime(2015, 3, 1, 13)] == 2)
    assert (ts_sum[datetime.datetime(2015, 3, 1, 17)] == 2)
    assert (ts_sum[datetime.datetime(2015, 3, 1, 18)] == 3)
    assert (ts_sum[datetime.datetime(2015, 3, 1, 19)] == 3)
    assert (ts_sum[datetime.datetime(2015, 3, 3)] == 2)
    assert (ts_sum[datetime.datetime(2015, 3, 4)] == 1)
    assert (ts_sum[datetime.datetime(2015, 3, 4, 18)] == 1)
    assert (ts_sum[datetime.datetime(2015, 3, 5)] == 0)
    assert (ts_sum[datetime.datetime(2015, 3, 6)] == 0)
    assert (((0 + a) + b) == (a + b))
