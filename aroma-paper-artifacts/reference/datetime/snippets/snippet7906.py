from enum import Enum as _Enum
from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
from Acquire.Accounting import create_decimal as _create_decimal
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
import copy as _copy
from Acquire.Accounting import create_decimal as _create_decimal


def dated_uid(self):
    'Return the full dated uid of the transaction. This\n           is isoformat(datetime)/uid\n        '
    return ('%s/%s' % (self._datetime.isoformat(), self._uid))
