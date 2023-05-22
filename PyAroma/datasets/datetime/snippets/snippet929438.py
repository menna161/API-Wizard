import datetime
import nose
from traces import TimeSeries, Histogram


def test_distribution():
    start = datetime.datetime(2015, 3, 1)
    a = TimeSeries()
    a.set(start, 1)
    a.set(datetime.datetime(2015, 3, 2), 0)
    a.set(datetime.datetime(2015, 3, 3), 1)
    a.set(datetime.datetime(2015, 3, 4), 0)
    end = datetime.datetime(2015, 3, 5)
    distribution = a.distribution(start=start, end=end, normalized=False)
    assert (distribution[0] == (((24 * 60) * 60) * 2))
    assert (distribution[1] == (((24 * 60) * 60) * 2))
    distribution = a.distribution(start=start, end=end)
    assert (distribution[0] == 0.5)
    assert (distribution[1] == 0.5)
