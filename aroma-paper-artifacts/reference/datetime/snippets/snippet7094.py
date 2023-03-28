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


def datetime_to_string(d):
    'Return the passed datetime encoded to a string. This will be a\n       standard iso-formatted time in the UTC timezone (converting\n       to UTC if the passed datetime is for another timezone)\n\n       Args:\n            d (datetime): Datetime to convert to string\n       Returns:\n            str: Datetime as a string\n\n    '
    if (d.tzinfo is None):
        d = d.replace(tzinfo=_datetime.timezone.utc)
    else:
        d = d.astimezone(_datetime.timezone.utc)
    return d.replace(tzinfo=None).isoformat()
