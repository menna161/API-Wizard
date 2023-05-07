import bisect
import collections
import datetime
import warnings
from dateutil.parser import parse as _dateutil_parse


def workdaycount(self, date1, date2):
    '\n        Count work days between two dates, ignoring holidays.\n\n        Args:\n            date1 (date, datetime or str): Date start of interval.\n            date2 (date, datetime or str): Date end of interval.\n\n        Note:\n            The adopted notation is COB to COB, so effectively date1 is not\n            included in the calculation result.\n\n        Example:\n            >>> cal = Calendar()\n            >>> date1 = datetime.datetime.today()\n            >>> date2 = cal.addworkdays(date1, 1)\n            >>> cal.workdaycount(date1, date2)\n            1\n\n        Returns:\n            int: Number of work days between the two dates. If the dates\n                are equal the result is zero. If date1 > date2 the result is\n                negative.\n        '
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
    return (ndays * direction)
