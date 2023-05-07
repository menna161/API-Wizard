import bisect
import collections
import datetime
import warnings
from dateutil.parser import parse as _dateutil_parse


def isbusday(self, date):
    '\n        Check if a given date is a business date, taking into consideration\n        the work days and holidays.\n\n        Args:\n            date (date, datetime or str): Date to be checked.\n\n        Returns:\n            bool: True if the date is a business date, False otherwise.\n        '
    return (self.isworkday(date) and (not self.isholiday(date)))
