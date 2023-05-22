import datetime
import nose
from traces import TimeSeries, Histogram


def test_default_values():
    a = TimeSeries()
    a.set(datetime.datetime(2015, 3, 1), 1)
    a.set(datetime.datetime(2015, 3, 2), 0)
    a.set(datetime.datetime(2015, 3, 3), 1)
    a.set(datetime.datetime(2015, 3, 4), 0)
    start = datetime.datetime(2015, 3, 1)
    end = datetime.datetime(2015, 3, 4)
    default = a.distribution()
    distribution = a.distribution(start=start, end=end)
    assert (default == distribution)
    assert (distribution[0] == (1.0 / 3))
    assert (distribution[1] == (2.0 / 3))
