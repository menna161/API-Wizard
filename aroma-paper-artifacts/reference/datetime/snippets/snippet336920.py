import time
import datetime
import calendar


def firstDayOfNextMonth(self, dateFormat):
    d = datetime.datetime.now()
    year = d.year
    month = d.month
    if ((month + 1) > 12):
        month = 1
        year += 1
    else:
        month += 1
    return datetime.datetime(year, month, 1).strftime(dateFormat)
