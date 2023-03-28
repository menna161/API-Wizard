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


def date_to_string(d):
    'Return the date that has been encoded to a string. This will\n       write the date as a standard iso-formatted date. IF a datetime\n       is passed then this will be in the\n       UTC timezone (converting to UTC if the passed datetime\n       is for another timezone)\n\n       Args:\n            d (datetime): Datetie to convert\n       Returns:\n            str: Datetime in ISO format\n    '
    if isinstance(d, _datetime.datetime):
        return datetime_to_datetime(d).date().isoformat()
    else:
        return d.isoformat()
