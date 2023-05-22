import datetime
import os
import sys


def extract_datetime_from_line(line, year):
    line = line.strip().split()
    month = int(line[0][1:3])
    day = int(line[0][3:])
    timestamp = line[1]
    pos = timestamp.rfind('.')
    ts = [int(x) for x in timestamp[:pos].split(':')]
    hour = ts[0]
    minute = ts[1]
    second = ts[2]
    microsecond = int(timestamp[(pos + 1):])
    dt = datetime.datetime(year, month, day, hour, minute, second, microsecond)
    return dt
