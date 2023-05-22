import datetime
import nose
from traces import TimeSeries, Histogram


def test_mask():
    start = datetime.datetime(2015, 3, 1)
    a = TimeSeries()
    a.set(start, 1)
    a.set(datetime.datetime(2015, 4, 2), 0)
    a.set(datetime.datetime(2015, 4, 3), 1)
    a.set(datetime.datetime(2015, 4, 4), 0)
    end = datetime.datetime(2015, 4, 5)
    mask = TimeSeries(default=False)
    mask[datetime.datetime(2015, 4, 1)] = True
    mask[datetime.datetime(2015, 4, 3)] = False
    distribution = a.distribution(start=start, end=end, normalized=False, mask=mask)
    assert (distribution[0] == ((24 * 60) * 60))
    assert (distribution[1] == ((24 * 60) * 60))
    distribution = a.distribution(start=start, end=end, mask=mask)
    assert (distribution[0] == 0.5)
    assert (distribution[1] == 0.5)
