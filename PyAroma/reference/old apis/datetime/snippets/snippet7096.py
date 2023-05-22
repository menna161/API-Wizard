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


def date_and_time_to_datetime(date, time=_datetime.time(0)):
    'Return the passed date and time as a UTC datetime. By\n       default the time is midnight (first second of the day)\n\n       Args:\n            date (datetime): Date (may be any timezone)\n            time (default=_datetime.time(0)): Time of day, default midnight\n       Returns:\n            datetime: UTC datetime\n    '
    return datetime_to_datetime(_datetime.datetime.combine(date, time))
