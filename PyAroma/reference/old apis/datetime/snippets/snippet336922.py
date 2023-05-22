import time
import datetime
import calendar


def firstDayOfMonthThisYear(self, month, dateFormat):
    d = datetime.datetime.now()
    year = d.year
    return datetime.datetime(year, month, 1).strftime(dateFormat)
