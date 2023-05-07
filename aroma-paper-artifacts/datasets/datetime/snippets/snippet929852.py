import datetime
import os
import sys


def get_start_time(line_iterable, year):
    'Find start time from group of lines\n    '
    start_datetime = None
    for line in line_iterable:
        line = line.strip()
        if (line.find('Solving') != (- 1)):
            start_datetime = extract_datetime_from_line(line, year)
            break
    return start_datetime
