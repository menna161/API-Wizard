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


def string_to_date(s):
    "Return a date from the string that has been encoded using\n       'date_to_string'. This is only guaranteed to work for strings\n       that were created using that function\n\n       Args:\n            s (str): String from date_to_string function\n       Returns:\n            datetime: Datetime created from string\n    "
    d = _datetime.date.fromisoformat(s)
    return d
