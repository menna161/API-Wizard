import json as _json
import base64 as _base64
import datetime as _datetime
import uuid as _uuid
import os as _os
import sys as _sys
import re as _re
from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
from Acquire.Accounting import create_decimal as _create_decimal
from os.path import split as _split
from backports.datetime_fromisoformat import MonkeyPatch as _MonkeyPatch
from Acquire.ObjectStore import EncodingError


def get_datetime_future(weeks=0, days=0, hours=0, minutes=0, seconds=0, timedelta=None):
    'Return the datetime that is the supplied time in the future.\n       This will raise an exception if the time is not in the future!\n\n       Args:\n            weeks (int, default=0): Number of weeks in future\n            days (int, default=0): Number of days in future\n            hours (int, default=0): Number of hours in future\n            minutes (int, default=0): Number of minutes in future\n            seconds (int, default=0): Number of seconds in future\n            timedelta (datetime.timedelta, default=0): Timedelta from now\n    '
    delta = _datetime.timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds)
    if (timedelta is not None):
        if (not isinstance(timedelta, _datetime.timedelta)):
            raise TypeError('The delta must be a datetime.timedelta object')
        delta += timedelta
    if (delta.total_seconds() < 5):
        raise ValueError(('The requested delta (%s) is not sufficiently far enough into the future!' % str(delta)))
    return (get_datetime_now() + delta)
