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


def create_uuid(short_uid=False, include_date=None, separator='/'):
    "Return a newly created random uuid. This is highly likely\n       to be globally unique. If 'short_uid' is True, then a shorter,\n       potentially less unique UID will be generated. If\n       'include_date' is passed, then the passed date will\n       be encoded into the UID\n\n       Returns:\n            str: Random UUID\n    "
    uid = str(_uuid.uuid4())
    if short_uid:
        uid = uid[:8]
    if ((include_date is not None) and (include_date is not False)):
        if (include_date is True):
            include_date = get_datetime_now()
        else:
            include_date = datetime_to_datetime(include_date)
        uid = ('%s%s%s' % (include_date.replace(tzinfo=None).isoformat(), separator, uid))
    return uid
