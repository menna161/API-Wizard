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


def string_to_time(s):
    "Return a time from the string that was encoded by 'time_to_string'.\n       This will only be guaranteed to produce valid output for strings\n       produced using that function\n\n       Args:\n            s (str): String to convert to time\n       Returns:\n            datetime.time: Time object created from string\n    "
    t = _datetime.time.fromisoformat(s)
    if (t.tzinfo is None):
        t = t.replace(tzinfo=_datetime.timezone.utc)
    else:
        t = t.astimezone(_datetime.timezone.utc)
    return t
