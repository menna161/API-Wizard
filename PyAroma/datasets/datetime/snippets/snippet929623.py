import datetime
from infinity import inf


def floor_datetime(dt, unit, n_units=1):
    'Floor a datetime to nearest n units. For example, if we want to\n    floor to nearest three months, starting with 2016-05-06-yadda, it\n    will go to 2016-04-01. Or, if starting with 2016-05-06-11:45:06\n    and rounding to nearest fifteen minutes, it will result in\n    2016-05-06-11:45:00.\n    '
    if (unit == 'years'):
        new_year = (dt.year - ((dt.year - 1) % n_units))
        return datetime.datetime(new_year, 1, 1, 0, 0, 0)
    elif (unit == 'months'):
        new_month = (dt.month - ((dt.month - 1) % n_units))
        return datetime.datetime(dt.year, new_month, 1, 0, 0, 0)
    elif (unit == 'weeks'):
        (_, isoweek, _) = dt.isocalendar()
        new_week = (isoweek - ((isoweek - 1) % n_units))
        return datetime.datetime.strptime(('%d %02d 1' % (dt.year, new_week)), '%Y %W %w')
    elif (unit == 'days'):
        new_day = (dt.day - (dt.day % n_units))
        return datetime.datetime(dt.year, dt.month, new_day, 0, 0, 0)
    elif (unit == 'hours'):
        new_hour = (dt.hour - (dt.hour % n_units))
        return datetime.datetime(dt.year, dt.month, dt.day, new_hour, 0, 0)
    elif (unit == 'minutes'):
        new_minute = (dt.minute - (dt.minute % n_units))
        return datetime.datetime(dt.year, dt.month, dt.day, dt.hour, new_minute, 0)
    elif (unit == 'seconds'):
        new_second = (dt.second - (dt.second % n_units))
        return datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, new_second)
    else:
        msg = 'Unknown unit type {}'.format(unit)
        raise ValueError(msg)
