import bisect
import collections
import datetime
import warnings
from dateutil.parser import parse as _dateutil_parse


def addbusdays(self, date, offset):
    '\n        Add business days to a given date, taking holidays into consideration.\n\n        Note:\n            By definition, a zero offset causes the function to return the\n            initial date, even it is not a business date. An offset of 1\n            represents the next business date, regardless of date being a\n            business date or not.\n\n        Args:\n            date (date, datetime or str): Date to be incremented.\n            offset (integer): Number of business days to add. Positive values\n                move the date forward and negative values move the date back.\n\n        Returns:\n            datetime: New incremented date.\n        '
    date = parsefun(date)
    if (offset == 0):
        return date
    dateoffset = self.addworkdays(date, offset)
    holidays = self.holidays
    if (not holidays):
        return dateoffset
    weekdaymap = self.weekdaymap
    datewk = dateoffset.weekday()
    if (offset > 0):
        i = bisect.bisect_right(holidays, date)
        if (i == len(holidays)):
            warn(('Holiday list exhausted at end, addbusday(%s,%s) output may be incorrect.' % (date, offset)))
        else:
            while (holidays[i] <= dateoffset):
                dateoffset += datetime.timedelta(days=weekdaymap[datewk].offsetnext)
                datewk = weekdaymap[datewk].nextworkday
                i += 1
                if (i == len(holidays)):
                    warn(('Holiday list exhausted at end, addbusday(%s,%s) output may be incorrect.' % (date, offset)))
                    break
    else:
        i = (bisect.bisect_left(holidays, date) - 1)
        if (i == (- 1)):
            warn(('Holiday list exhausted at start, addbusday(%s,%s) output may be incorrect.' % (date, offset)))
        else:
            while (holidays[i] >= dateoffset):
                dateoffset += datetime.timedelta(days=weekdaymap[datewk].offsetprev)
                datewk = weekdaymap[datewk].prevworkday
                i -= 1
                if (i == (- 1)):
                    warn(('Holiday list exhausted at start, addbusday(%s,%s) output may be incorrect.' % (date, offset)))
                    break
    return dateoffset
