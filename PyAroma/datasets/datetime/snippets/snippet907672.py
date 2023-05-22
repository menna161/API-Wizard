import bisect
import collections
import datetime
import warnings
from dateutil.parser import parse as _dateutil_parse


def isholiday(self, date):
    '\n        Check if a given date is a holiday.\n\n        Args:\n            date (date, datetime or str): Date to be checked.\n\n        Returns:\n            bool: True if the date is a holiday, False otherwise.\n        '
    date = parsefun(date)
    if self.holidays:
        i = bisect.bisect_left(self.holidays, date)
        if ((i == 0) and (date < self.holidays[0])):
            warn(('Holiday list exhausted at start, isholiday(%s) output may be incorrect.' % date))
        elif (i == len(self.holidays)):
            warn(('Holiday list exhausted at end, isholiday(%s) output may be incorrect.' % date))
        elif (self.holidays[i] == date):
            return True
    return False
