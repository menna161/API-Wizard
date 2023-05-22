import datetime
from infinity import inf


def datetime_range(start_dt, end_dt, unit, n_units=1, inclusive_end=False):
    'A range of datetimes/dates.'

    def done(a, b, inclusive_end):
        if inclusive_end:
            return (a <= b)
        else:
            return (a < b)
    current = start_dt
    while done(current, end_dt, inclusive_end):
        (yield current)
        current += datetime.timedelta(**{unit: n_units})
