from datetime import timedelta, datetime, date
import nose
from infinity import inf
import traces.utils as utils


def test_datetime_floor():
    nose.tools.eq_(utils.datetime_floor(date(2016, 5, 6), 'years'), datetime(2016, 1, 1))
    nose.tools.eq_(utils.datetime_floor(inf), inf)
    test_dt = datetime(2016, 5, 6, 11, 45, 6)
    nose.tools.eq_(utils.datetime_floor(test_dt, 'months', n_units=3), datetime(2016, 4, 1))
    nose.tools.eq_(utils.datetime_floor(test_dt, 'weeks', n_units=3), datetime(2016, 4, 18))
    nose.tools.eq_(utils.datetime_floor(test_dt, 'hours', n_units=10), datetime(2016, 5, 6, 10))
    nose.tools.eq_(utils.datetime_floor(test_dt, 'minutes', n_units=15), datetime(2016, 5, 6, 11, 45))
    nose.tools.eq_(utils.datetime_floor(test_dt, 'seconds', n_units=30), datetime(2016, 5, 6, 11, 45))
    nose.tools.assert_raises(ValueError, utils.datetime_floor, '2016-6-7')
    nose.tools.assert_raises(ValueError, utils.datetime_floor, test_dt, 'sleconds', n_units=3)
