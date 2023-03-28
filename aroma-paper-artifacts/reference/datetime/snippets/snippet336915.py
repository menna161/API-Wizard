import time
import datetime
import calendar


def getTime(self):
    return datetime.datetime.now().strftime('%H%M%S%f')
