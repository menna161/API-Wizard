import datetime
from infinity import inf


def time_midpoint(t0, t1):
    'Return the midpoint between two time values.'
    duration = (t1 - t0)
    if isinstance(duration, (datetime.timedelta,)):
        half = (duration.total_seconds() / 2.0)
        return (t0 + datetime.timedelta(seconds=half))
    else:
        return (t0 + (duration / 2.0))
