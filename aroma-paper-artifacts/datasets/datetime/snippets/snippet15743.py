import json
import os
from sap.cf_logging.defaults import UNIX_EPOCH


def time_delta_ms(start, end):
    ' Returns the delta time between to datetime objects '
    time_delta = (end - start)
    return ((int(time_delta.total_seconds()) * 1000) + int((time_delta.microseconds / 1000)))
