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


def string_to_datetime(s):
    "Return the datetime that had been encoded to the passed string\n       via datetime_to_string. This string must have been created\n       via 'datetime_to_string'\n\n       Args:\n            s (str): String to convert\n       Returns:\n            datetime: Datetime version of string\n    "
    if isinstance(s, _datetime.datetime):
        return s
    else:
        d = _datetime.datetime.fromisoformat(s)
        return datetime_to_datetime(d)
