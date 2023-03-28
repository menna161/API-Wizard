import time
import datetime
import calendar


def formated_time(self, format_time):
    return datetime.datetime.now().strftime(format_time)
