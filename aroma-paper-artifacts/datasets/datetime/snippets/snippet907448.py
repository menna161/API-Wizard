from datetime import datetime, timedelta
import time


def __init__(self, time_object=None):
    self._datetime = None
    if (not time_object):
        time_object = datetime.now()
    time_object = str(time_object)
    try:
        time_object = float(time_object)
        self._parse_timestamp(time_object)
    except ValueError:
        self._parse_time_str(time_object)
