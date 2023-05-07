import bisect
import collections
import datetime
import warnings
from dateutil.parser import parse as _dateutil_parse


def isworkday(self, date):
    '\n        Check if a given date is a work date, ignoring holidays.\n\n        Args:\n            date (date, datetime or str): Date to be checked.\n\n        Returns:\n            bool: True if the date is a work date, False otherwise.\n        '
    date = parsefun(date)
    return self.weekdaymap[date.weekday()].isworkday
