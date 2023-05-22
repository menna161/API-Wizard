import datetime
import calendar
import operator
from math import copysign
from six import integer_types
from warnings import warn


def __init__(self, dt1=None, dt2=None, years=0, months=0, days=0, leapdays=0, weeks=0, hours=0, minutes=0, seconds=0, microseconds=0, year=None, month=None, day=None, weekday=None, yearday=None, nlyearday=None, hour=None, minute=None, second=None, microsecond=None):
    if any((((x is not None) and (x != int(x))) for x in (years, months))):
        raise ValueError('Non-integer years and months are ambiguous and not currently supported.')
    if (dt1 and dt2):
        if (not (isinstance(dt1, datetime.date) and isinstance(dt2, datetime.date))):
            raise TypeError('relativedelta only diffs datetime/date')
        if (isinstance(dt1, datetime.datetime) != isinstance(dt2, datetime.datetime)):
            if (not isinstance(dt1, datetime.datetime)):
                dt1 = datetime.datetime.fromordinal(dt1.toordinal())
            elif (not isinstance(dt2, datetime.datetime)):
                dt2 = datetime.datetime.fromordinal(dt2.toordinal())
        self.years = 0
        self.months = 0
        self.days = 0
        self.leapdays = 0
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.microseconds = 0
        self.year = None
        self.month = None
        self.day = None
        self.weekday = None
        self.hour = None
        self.minute = None
        self.second = None
        self.microsecond = None
        self._has_time = 0
        months = (((dt1.year - dt2.year) * 12) + (dt1.month - dt2.month))
        self._set_months(months)
        dtm = self.__radd__(dt2)
        if (dt1 < dt2):
            compare = operator.gt
            increment = 1
        else:
            compare = operator.lt
            increment = (- 1)
        while compare(dt1, dtm):
            months += increment
            self._set_months(months)
            dtm = self.__radd__(dt2)
        delta = (dt1 - dtm)
        self.seconds = (delta.seconds + (delta.days * 86400))
        self.microseconds = delta.microseconds
    else:
        self.years = years
        self.months = months
        self.days = (days + (weeks * 7))
        self.leapdays = leapdays
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.microseconds = microseconds
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.microsecond = microsecond
        if any((((x is not None) and (int(x) != x)) for x in (year, month, day, hour, minute, second, microsecond))):
            warn((('Non-integer value passed as absolute information. ' + 'This is not a well-defined condition and will raise ') + 'errors in future versions.'), DeprecationWarning)
        if isinstance(weekday, integer_types):
            self.weekday = weekdays[weekday]
        else:
            self.weekday = weekday
        yday = 0
        if nlyearday:
            yday = nlyearday
        elif yearday:
            yday = yearday
            if (yearday > 59):
                self.leapdays = (- 1)
        if yday:
            ydayidx = [31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 366]
            for (idx, ydays) in enumerate(ydayidx):
                if (yday <= ydays):
                    self.month = (idx + 1)
                    if (idx == 0):
                        self.day = yday
                    else:
                        self.day = (yday - ydayidx[(idx - 1)])
                    break
            else:
                raise ValueError(('invalid year day (%d)' % yday))
    self._fix()
