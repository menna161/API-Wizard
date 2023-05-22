import time
import datetime
import calendar


def addYearsByFormatter(self, years, dateFormat):
    d = datetime.datetime.now()
    c = calendar.Calendar()
    year = (d.year + years)
    month = d.month
    today = d.day
    days = calendar.monthrange(year, month)[1]
    if (today > days):
        afterday = days
    else:
        afterday = today
    return datetime.datetime(year, month, afterday).strftime(dateFormat)
