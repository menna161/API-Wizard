import datetime
import nose
import traces
import pandas as pd
import numpy as np


def test_sample():
    time_list = [datetime.datetime(2016, 1, 1, 1, 1, 2), datetime.datetime(2016, 1, 1, 1, 1, 3), datetime.datetime(2016, 1, 1, 1, 1, 8), datetime.datetime(2016, 1, 1, 1, 1, 10)]
    ts = _make_ts(int, time_list, [1, 2, 3, 0])

    def curr_time(i):
        return datetime.datetime(2016, 1, 1, 1, 1, i)
    assert (dict(ts.sample(1, time_list[0], time_list[(- 1)])) == {curr_time(i): ts[curr_time(i)] for i in range(2, 11)})
    assert (dict(ts.sample(2, time_list[0], time_list[(- 1)])) == {curr_time(i): ts[curr_time(i)] for i in range(2, 11, 2)})
    nose.tools.assert_raises(ValueError, ts.sample, (- 1), time_list[0], time_list[(- 1)])
    nose.tools.assert_raises(ValueError, ts.sample, 20, time_list[0], time_list[(- 1)])
    nose.tools.assert_raises(ValueError, ts.sample, 1, time_list[3], time_list[0])
    assert (dict(ts.sample(1, curr_time(5), curr_time(10))) == {curr_time(i): ts[curr_time(i)] for i in range(5, 11)})
    assert (dict(ts.sample(1, curr_time(2), curr_time(5))) == {curr_time(i): ts[curr_time(i)] for i in range(2, 6)})
    assert (dict(ts.sample(1, curr_time(0), curr_time(13))) == {curr_time(i): ts[curr_time(i)] for i in range(0, 14)})
    ts = traces.TimeSeries([[1, 2], [2, 3], [6, 1], [8, 4]])
    assert (dict(ts.sample(1, 1, 8)) == {i: ts[i] for i in range(1, 9)})
    assert (dict(ts.sample(0.5, 1, 8)) == {(1 + (i / 2.0)): ts[(1 + (i / 2.0))] for i in range(0, 15)})
    nose.tools.assert_raises(ValueError, ts.sample, 0.5, (- traces.inf), 8)
    nose.tools.assert_raises(ValueError, ts.sample, 0.5, 1, traces.inf)
    pd_ts = pd.Series(dict(ts.sample(1, 1, 8)))
    assert all(((pd_ts.index[(i - 1)] == i) for i in range(1, 9)))
    assert all(((pd_ts.values[(i - 1)] == ts[i]) for i in range(1, 9)))
