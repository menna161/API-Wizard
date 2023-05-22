import time
import datetime
import calendar


def addDaysByFormatter(self, adddays, dateFormat):
    afteraddtime = (datetime.datetime.now() + datetime.timedelta(days=adddays))
    return time.strftime(afteraddtime, dateFormat)
