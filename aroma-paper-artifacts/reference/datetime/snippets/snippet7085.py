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


def validate_is_uid(uid):
    "Validate that the passed 'uid' is actually a UID. This checks\n       that the string is not something weird that is trying to\n       break the system\n    "
    if (uid is None):
        raise TypeError("'None' is not a valid UID!")
    uid = str(uid)
    len_uid = len(uid)
    import re as _re
    from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
    if (len_uid == 8):
        if _re.match('[a-f0-9]{8}', uid):
            return
    elif (len_uid == 35):
        parts = uid.split('/')
        try:
            dt = _string_to_datetime(parts[0])
            if _re.match('[a-f0-9]{8}', parts[1]):
                return
        except Exception as e:
            print(e)
            pass
    elif (len_uid == 36):
        if _re.match('[a-f0-9]{8}\\-[a-f0-9]{4}\\-[a-f0-9]{4}\\-[a-f0-9]{4}\\-[a-f0-9]{12}', uid):
            return
    elif (len_uid == 63):
        parts = uid.split('/')
        try:
            dt = _string_to_datetime(parts[0])
            if _re.match('[a-f0-9]{8}\\-[a-f0-9]{4}\\-[a-f0-9]{4}\\-[a-f0-9]{4}\\-[a-f0-9]{12}', parts[1]):
                return
        except:
            pass
    raise TypeError(("'%s' is not a valid UID!" % uid))
