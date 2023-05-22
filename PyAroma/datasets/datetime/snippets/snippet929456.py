import datetime
import random
import sys
import pprint
from infinity import inf
import nose
from traces import TimeSeries


def test_iterintervals():
    ts = TimeSeries()
    ts.set(datetime.datetime(2015, 3, 1), 1)
    ts.set(datetime.datetime(2015, 3, 2), 0)
    ts.set(datetime.datetime(2015, 3, 3), 1)
    ts.set(datetime.datetime(2015, 3, 4), 2)
    answer = [(1, 0), (0, 1), (1, 2)]
    result = []
    for ((t0, v0), (t1, v1)) in ts.iterintervals():
        result.append((v0, v1))
    assert (answer == result)
