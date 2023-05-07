import bisect
import collections
import datetime
import warnings
from dateutil.parser import parse as _dateutil_parse


def _workdaycount(self, date1, date2):
    '\n        (PRIVATE) Count work days between two dates, ignoring holidays.\n        '
    assert (date2 >= date1)
    date1wd = date1.weekday()
    date2wd = date2.weekday()
    if (not self.weekdaymap[date2wd].isworkday):
        date2 += datetime.timedelta(days=self.weekdaymap[date2wd].offsetprev)
        date2wd = self.weekdaymap[date2wd].prevworkday
    if (date2 <= date1):
        return 0
    (nw, nd) = divmod((date2 - date1).days, 7)
    ndays = (nw * len(self.workdays))
    if (nd > 0):
        date1wd = date1.weekday()
        date2wd = date2.weekday()
        while (date1wd != date2wd):
            ndays += 1
            date1wd = self.weekdaymap[date1wd].nextworkday
    return ndays
