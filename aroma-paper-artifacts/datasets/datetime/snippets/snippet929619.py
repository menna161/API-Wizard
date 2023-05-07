import datetime
from infinity import inf


def duration_to_number(duration, units='seconds'):
    'If duration is already a numeric type, then just return\n    duration. If duration is a timedelta, return a duration in\n    seconds.\n\n    TODO: allow for multiple types of units.\n\n    '
    if isinstance(duration, (int, float)):
        return duration
    elif isinstance(duration, (datetime.timedelta,)):
        if (units == 'seconds'):
            return duration.total_seconds()
        else:
            msg = ('unit "%s" is not supported' % units)
            raise NotImplementedError(msg)
    elif (duration in (inf, (- inf))):
        msg = "Can't convert infinite duration to number"
        raise ValueError(msg)
    else:
        msg = ('duration is an unknown type (%s)' % duration)
        raise TypeError(msg)
