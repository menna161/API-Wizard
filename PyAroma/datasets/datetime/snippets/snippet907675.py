import bisect
import collections
import datetime
import warnings
from dateutil.parser import parse as _dateutil_parse


def addworkdays(self, date, offset):
    '\n        Add work days to a given date, ignoring holidays.\n\n        Note:\n            By definition, a zero offset causes the function to return the\n            initial date, even it is not a work date. An offset of 1\n            represents the next work date, regardless of date being a work\n            date or not.\n\n        Args:\n            date (date, datetime or str): Date to be incremented.\n            offset (integer): Number of work days to add. Positive values move\n                the date forward and negative values move the date back.\n\n        Returns:\n            datetime: New incremented date.\n        '
    date = parsefun(date)
    if (offset == 0):
        return date
    if (offset > 0):
        direction = 1
        idx_offset = Calendar._idx_offsetnext
        idx_next = Calendar._idx_nextworkday
        idx_offset_other = Calendar._idx_offsetprev
        idx_next_other = Calendar._idx_prevworkday
    else:
        direction = (- 1)
        idx_offset = Calendar._idx_offsetprev
        idx_next = Calendar._idx_prevworkday
        idx_offset_other = Calendar._idx_offsetnext
        idx_next_other = Calendar._idx_nextworkday
    weekdaymap = self.weekdaymap
    datewk = date.weekday()
    if (not weekdaymap[datewk].isworkday):
        date += datetime.timedelta(days=weekdaymap[datewk][idx_offset_other])
        datewk = weekdaymap[datewk][idx_next_other]
    (nw, nd) = divmod(abs(offset), len(self.workdays))
    ndays = (nw * 7)
    while (nd > 0):
        ndays += abs(weekdaymap[datewk][idx_offset])
        datewk = weekdaymap[datewk][idx_next]
        nd -= 1
    date += datetime.timedelta(days=(ndays * direction))
    return date
