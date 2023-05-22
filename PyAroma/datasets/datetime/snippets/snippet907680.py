import bisect
import collections
import datetime
import warnings
from dateutil.parser import parse as _dateutil_parse


@staticmethod
def caleom(date):
    '\n        Adjust date to last day of the month, regardless of work days.\n\n        Args:\n            date (date, datetime or str): Date to be adjusted.\n\n        Returns:\n            datetime: Adjusted date.\n        '
    date = parsefun(date)
    date += datetime.timedelta(days=(32 - date.day))
    date -= datetime.timedelta(days=date.day)
    return date
