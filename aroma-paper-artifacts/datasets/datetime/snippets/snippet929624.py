import datetime
from infinity import inf


def datetime_floor(value, unit='days', n_units=1):
    if (type(value) is datetime.date):
        value = datetime.datetime.combine(value, datetime.time())
    if isinstance(value, datetime.datetime):
        return floor_datetime(value, unit, n_units)
    elif (value == (- inf)):
        return (- inf)
    elif (value == inf):
        return inf
    else:
        msg = 'must be date, datetime, or inf; got {}'.format(value)
        raise ValueError(msg)
