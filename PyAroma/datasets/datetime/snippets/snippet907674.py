import bisect
import collections
import datetime
import warnings
from dateutil.parser import parse as _dateutil_parse


def adjust(self, date, mode):
    '\n        Adjust the date to the closest work date.\n\n        Args:\n            date (date, datetime or str): Date to be adjusted.\n            mode (integer): FOLLOWING, PREVIOUS or MODIFIEDFOLLOWING.\n\n        Note:\n            If date is already a business date than it is returned unchanged.\n            How to use the adjustment constants:\n\n            **FOLLOWING**:\n                Adjust to the next business date.\n            **PREVIOUS**:\n                Adjust to the previous business date.\n            **MODIFIEDFOLLOWING**:\n                Adjust to the next business date unless it falls on a\n                different month, in which case adjust to the previous business\n                date.\n\n        Returns:\n            datetime: Adjusted date.\n        '
    date = parsefun(date)
    if self.isbusday(date):
        return date
    if (mode == FOLLOWING):
        dateadj = self.addbusdays(date, 1)
    elif (mode == PREVIOUS):
        dateadj = self.addbusdays(date, (- 1))
    elif (mode == MODIFIEDFOLLOWING):
        dateadj = self.addbusdays(date, 1)
        if (dateadj.month != date.month):
            dateadj = self.addbusdays(dateadj, (- 1))
    else:
        raise ValueError(('Invalid mode %s' % mode))
    return dateadj
