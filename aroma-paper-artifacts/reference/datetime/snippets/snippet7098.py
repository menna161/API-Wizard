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


def get_datetime_now():
    'Return the current time in the UTC timezone. This creates an\n       object that will be properly stored using datetime_to_string\n       and string_to_datetime\n\n       Returns:\n            datetime: Current datetime\n    '
    return datetime_to_datetime(_datetime.datetime.now(_datetime.timezone.utc))
