import bisect
import collections
import datetime
import warnings
from dateutil.parser import parse as _dateutil_parse


def busdaycount(self, date1, date2):
    '\n        Count business days between two dates (private), taking holidays into\n        consideration.\n\n        Args:\n            date1 (date, datetime or str): Date start of interval.\n            date2 (date, datetime or str): Date end of interval.\n\n        Note:\n            The adopted notation is COB to COB, so effectively date1 is not\n            included in the calculation result.\n\n        Example:\n            >>> cal = Calendar()\n            >>> date1 = datetime.datetime.today()\n            >>> date2 = cal.addbusdays(date1, 1)\n            >>> cal.busdaycount(date1, date2)\n            1\n\n        Returns:\n            int: Number of business days between the two dates. If the dates\n                are equal the result is zero. If date1 > date2 the result is\n                negative.\n        '
    date1 = parsefun(date1)
    date2 = parsefun(date2)
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        (date1, date2) = (date2, date1)
        direction = (- 1)
    else:
        direction = 1
    ndays = self._workdaycount(date1, date2)
    if self.holidays:
        holidays = self.holidays
        if (date1 > holidays[(- 1)]):
            warn(('Holiday list exhausted at end, busdaycount(%s,%s) output may be incorrect.' % (date1, date2)))
        elif (date2 < holidays[0]):
            warn(('Holiday list exhausted at start, busdaycount(%s,%s) output may be incorrect.' % (date1, date2)))
        else:
            if (date1 < holidays[0]):
                warn(('Holiday list exhausted at start, busdaycount(%s,%s) output may be incorrect.' % (date1, date2)))
            if (date2 > holidays[(- 1)]):
                warn(('Holiday list exhausted at end, busdaycount(%s,%s) output may be incorrect.' % (date1, date2)))
            i = bisect.bisect_right(holidays, date1)
            while (holidays[i] <= date2):
                ndays -= 1
                i += 1
                if (i == len(holidays)):
                    break
    return (ndays * direction)
