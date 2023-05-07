from datetime import timedelta, datetime, date
import nose
from infinity import inf
import traces.utils as utils


def test_datetime_range():
    dt_range = list(utils.datetime_range(datetime(2016, 1, 1), datetime(2016, 2, 1), 'days'))
    assert (dt_range[0] == datetime(2016, 1, 1))
    assert (dt_range[(- 1)] == datetime(2016, 1, 31))
    assert (dt_range[10] == datetime(2016, 1, 11))
    dt_range = list(utils.datetime_range(datetime(2016, 1, 2), datetime(2016, 2, 1), 'days', n_units=2, inclusive_end=True))
    assert (dt_range[0] == datetime(2016, 1, 2))
    assert (dt_range[(- 1)] == datetime(2016, 2, 1))
    assert (dt_range[10] == datetime(2016, 1, 22))
    dt_range = list(utils.datetime_range(datetime(2016, 1, 1), datetime(2016, 2, 1), 'hours'))
    assert ((dt_range[1] - dt_range[0]) == timedelta(hours=1))
    dt_range = list(utils.datetime_range(datetime(2016, 1, 1), datetime(2016, 2, 1), 'minutes', n_units=10))
    assert ((dt_range[1] - dt_range[0]) == timedelta(minutes=10))
    dt_range = list(utils.datetime_range(datetime(2016, 2, 1), datetime(2016, 1, 1), 'days'))
    assert (dt_range == [])
