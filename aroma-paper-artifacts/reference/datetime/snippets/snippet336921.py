import time
import datetime
import calendar


def firstDayOfMonth(self, year, month, dateFormat):
    return datetime.datetime(year, month, 1).strftime(dateFormat)
