import datetime
import random
import sys
import pprint
from infinity import inf
import nose
from traces import TimeSeries


def test_iterperiods():
    ts = TimeSeries()
    with nose.tools.assert_raises(KeyError):
        next(ts.iterperiods())
    ts.set(datetime.datetime(2015, 3, 1), 1)
    ts.set(datetime.datetime(2015, 3, 2), 0)
    ts.set(datetime.datetime(2015, 3, 3), 1)
    ts.set(datetime.datetime(2015, 3, 4), 2)
    answer = [(datetime.datetime(2015, 3, 1), datetime.datetime(2015, 3, 2), 1), (datetime.datetime(2015, 3, 2), datetime.datetime(2015, 3, 3), 0), (datetime.datetime(2015, 3, 3), datetime.datetime(2015, 3, 4), 1)]
    result = []
    for (t0, t1, v0) in ts.iterperiods(start=datetime.datetime(2015, 3, 1), end=datetime.datetime(2015, 3, 4)):
        result.append((t0, t1, v0))
    assert (answer == result)
    answer = [(datetime.datetime(2015, 3, 1), datetime.datetime(2015, 3, 2), 1), (datetime.datetime(2015, 3, 3), datetime.datetime(2015, 3, 4), 1)]
    result = []
    for (t0, t1, v0) in ts.iterperiods(start=datetime.datetime(2015, 3, 1), end=datetime.datetime(2015, 3, 4), value=1):
        result.append((t0, t1, v0))
    assert (answer == result)

    def filter(t0, t1, value):
        return (True if (not value) else False)
    answer = [(datetime.datetime(2015, 3, 2), datetime.datetime(2015, 3, 3), 0)]
    result = []
    for (t0, t1, v0) in ts.iterperiods(start=datetime.datetime(2015, 3, 1), end=datetime.datetime(2015, 3, 4), value=filter):
        result.append((t0, t1, v0))
    assert (answer == result)
