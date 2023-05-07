from datetime import datetime
import pickle
import nose
from traces import TimeSeries
import csv
import os


def test_set_interval_datetime():
    ts = TimeSeries(default=400)
    ts[datetime(2012, 1, 4, 12)] = 5
    ts[datetime(2012, 1, 9, 18)] = 10
    ts[datetime(2012, 1, 8):datetime(2012, 1, 10)] = 100
    assert (list(ts.items()) == [(datetime(2012, 1, 4, 12, 0), 5), (datetime(2012, 1, 8, 0, 0), 100), (datetime(2012, 1, 10, 0, 0), 10)])
