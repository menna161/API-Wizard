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


def datetime_to_datetime(d):
    'Return the passed datetime as a datetime that is clean\n       and usable by Acquire. This will move the datetime to UTC,\n       adding the timezone if this is missing\n\n       Args:\n            d (datetime): datetime to convert to UTC\n       Returns:\n            datetime: UTC datetime useable by Acquire\n\n    '
    if (not isinstance(d, _datetime.datetime)):
        raise TypeError(("The passed object '%s' is not a valid datetime" % str(d)))
    if (d.tzinfo is None):
        return d.replace(tzinfo=_datetime.timezone.utc)
    else:
        return d.astimezone(_datetime.timezone.utc)
