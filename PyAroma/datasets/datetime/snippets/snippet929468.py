import datetime
import nose
import traces
import pandas as pd
import numpy as np


def test_moving_average():
    time_list = [datetime.datetime(2016, 1, 1, 1, 1, 2), datetime.datetime(2016, 1, 1, 1, 1, 3), datetime.datetime(2016, 1, 1, 1, 1, 8), datetime.datetime(2016, 1, 1, 1, 1, 10)]
    ts = _make_ts(int, time_list, [1, 2, 3, 0])

    def curr_time(i):
        return datetime.datetime(2016, 1, 1, 1, 1, i)

    def build_answer(step, interval):
        answer = {}
        for i in range(*interval):
            t = curr_time(i)
            try:
                answer[t] = ts.mean((t - step), (t + step))
            except TypeError as e:
                if ('NoneType' in str(e)):
                    answer[t] = None
                else:
                    raise e
        return answer
    output = dict(ts.moving_average(sampling_period=1, window_size=2, start=time_list[0], end=time_list[(- 1)]))
    assert (output == build_answer(datetime.timedelta(seconds=1), (2, 11)))
    output = dict(ts.moving_average(1, 0.2, time_list[0], time_list[(- 1)]))
    assert (output == build_answer(datetime.timedelta(seconds=0.1), (2, 11)))
    nose.tools.assert_raises(ValueError, ts.moving_average, 1, (- 1), time_list[0], time_list[(- 1)])
    output = dict(ts.moving_average(2, 1, time_list[0], time_list[(- 1)]))
    assert (output == build_answer(datetime.timedelta(seconds=0.5), (2, 11, 2)))
    nose.tools.assert_raises(ValueError, ts.moving_average, (- 1), 1, time_list[0], time_list[(- 1)])
    nose.tools.assert_raises(ValueError, ts.moving_average, 20, 1, time_list[0], time_list[(- 1)])
    nose.tools.assert_raises(ValueError, ts.moving_average, 1, 1, time_list[3], time_list[0])
    output = dict(ts.moving_average(1, 2, curr_time(5), curr_time(10)))
    assert (output == build_answer(datetime.timedelta(seconds=1), (5, 11)))
    output = dict(ts.moving_average(1, 2, curr_time(2), curr_time(5)))
    assert (output == build_answer(datetime.timedelta(seconds=1), (2, 6)))
    output = dict(ts.moving_average(1, 2, curr_time(0), curr_time(13)))
    assert (output == build_answer(datetime.timedelta(seconds=1), (0, 14)))
    ts = traces.TimeSeries([[1, 2], [2, 3], [6, 1], [8, 4]])
    assert (dict(ts.moving_average(1, 2, 2, 8)) == {i: ts.mean((i - 1), (i + 1)) for i in range(2, 9)})
    assert (dict(ts.moving_average(0.5, 2, 2, 8)) == {(1 + (i / 2.0)): ts.mean(((1 + (i / 2.0)) - 1), ((1 + (i / 2.0)) + 1)) for i in range(2, 15)})
    pd_ts = pd.Series(dict(ts.moving_average(1, 2, 0, 8)))
    assert all(((pd_ts.index[i] == i) for i in range(1, 9)))
    assert np.isnan(pd_ts.values[0])
    assert all(((pd_ts.values[i] == ts.mean((i - 1), (i + 1))) for i in range(2, 9)))
    ts = _make_ts(int, time_list, [1, 2, 3, 0])
    sampling_period = datetime.timedelta(seconds=1)
    output = dict(ts.moving_average(sampling_period))
    answer = build_answer(datetime.timedelta(seconds=1), (2, 11))
    assert (output == build_answer(datetime.timedelta(seconds=1), (2, 11)))
