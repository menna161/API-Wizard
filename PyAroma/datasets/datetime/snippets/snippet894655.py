import sys
import os
from datetime import datetime, timedelta
import Globals
from User import User
from Context import Context
from Enumerations import Button, Mode


def extractTimestamp(self, line):
    date_raw = line[(line.find('<date>') + 6):line.find('</date>')]
    year = date_raw[0:4]
    month = self.padMonth(date_raw)
    day = self.padDay(date_raw)
    time_raw = line[(line.find('<time>') + 6):line.find('</time>')]
    first_colon = self.find_nth(time_raw, ':', 1)
    second_colon = self.find_nth(time_raw, ':', 2)
    third_colon = self.find_nth(time_raw, ':', 3)
    hour = time_raw[0:first_colon]
    minute = None
    seconds = None
    microseconds = None
    if (second_colon > 0):
        minute = time_raw[(first_colon + 1):second_colon]
        if (third_colon > 0):
            seconds = time_raw[(second_colon + 1):third_colon]
        else:
            seconds = time_raw[(second_colon + 1):]
    else:
        minute = time_raw[(first_colon + 1):]
        seconds = '0'
    if (third_colon > 0):
        microseconds = time_raw[(third_colon + 1):]
    else:
        microseconds = '0'
    try:
        timestamp = datetime(int(year), int(month), int(day), int(hour), int(minute), int(seconds))
    except ValueError:
        return None
    return timestamp
