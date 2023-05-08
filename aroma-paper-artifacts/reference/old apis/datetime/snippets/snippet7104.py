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


def time_to_string(t):
    'Return the time that has been encoded to a string. This will\n       write the time as a standard iso-formatted time. If a datetime\n       is passed then this will be in the\n       UTC timezone (converting to UTC if the passed datetime\n       is for another timezone)\n\n       Args:\n            t (time): Time to convert, can be datetime\n       Returns:\n            str: String of passed time converted to UTC ISO\n            format\n    '
    if isinstance(t, _datetime.datetime):
        t = datetime_to_datetime(t)
        return t.replace(tzinfo=None).time().isoformat()
    else:
        if (t.tzinfo is None):
            t = t.replace(tzinfo=_datetime.timezone.utc)
        elif (t.tzinfo != _datetime.timezone.utc):
            from Acquire.ObjectStore import EncodingError
            raise EncodingError(("Cannot encode a time to a string as this time is not in the UTC timezone. Please convert to UTC before encoding this time to a string '%s'" % t.isoformat()))
        return t.replace(tzinfo=None).isoformat()
