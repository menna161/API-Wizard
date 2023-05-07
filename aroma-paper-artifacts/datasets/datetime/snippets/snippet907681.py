import bisect
import collections
import datetime
import warnings
from dateutil.parser import parse as _dateutil_parse


def buseom(self, date):
    '\n        Adjust date to last business day of the month, taking holidays into\n        consideration.\n\n        Args:\n            date (date, datetime or str): Date to be adjusted.\n\n        Returns:\n            datetime: Adjusted date.\n        '
    return self.adjust(self.caleom(date), PREVIOUS)
