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


def get_datetime_now_to_string():
    'Convenience function that returns the result of get_datetime_now\n       as a string converted via datetime_to_string\n\n       Returns:\n            str: Current datetime as string\n    '
    return datetime_to_string(get_datetime_now())
