import time
import datetime
import calendar


def addMonthsByFormatter(self, months, dateFormat):
    d = datetime.datetime.now()
    c = calendar.Calendar()
    year = d.year
    month = d.month
    today = d.day
    if ((month + months) > 12):
        month = months
        year += 1
    else:
        month += months
    days = calendar.monthrange(year, month)[1]
    if (today > days):
        afteraddday = days
    else:
        afteraddday = today
    return datetime.datetime(year, month, afteraddday).strftime(dateFormat)
