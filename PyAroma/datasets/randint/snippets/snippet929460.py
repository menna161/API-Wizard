import datetime
import random
import sys
import pprint
from infinity import inf
import nose
from traces import TimeSeries


def test_merge():
    for n_trial in range(1000):
        ts_list = []
        for i in range(random.randint(1, 5)):
            ts_list.append(make_random_timeseries())
        method_a = list(TimeSeries.merge(ts_list, compact=False))
        method_b = list(TimeSeries.iter_merge(ts_list))
        msg = ('%s != %s' % (pprint.pformat(method_a), pprint.pformat(method_b)))
        assert (method_a == method_b), msg
