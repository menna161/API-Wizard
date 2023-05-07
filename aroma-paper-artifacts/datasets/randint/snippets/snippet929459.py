import datetime
import random
import sys
import pprint
from infinity import inf
import nose
from traces import TimeSeries


def make_random_timeseries():
    length = random.randint(1, 10)
    result = TimeSeries()
    t = 0
    for i in range(length):
        t += random.randint(0, 5)
        x = random.randint(0, 5)
        result[t] = x
    return result
