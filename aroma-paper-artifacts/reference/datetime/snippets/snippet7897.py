from enum import Enum as _Enum
from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
from Acquire.Accounting import create_decimal as _create_decimal
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
import copy as _copy
from Acquire.Accounting import create_decimal as _create_decimal


def __init__(self, key=None):
    'Construct, optionally from the passed key'
    if (key is not None):
        t = TransactionInfo.from_key(key)
        import copy as _copy
        self.__dict__ = _copy.copy(t.__dict__)
    else:
        from Acquire.Accounting import create_decimal as _create_decimal
        self._value = _create_decimal(0)
        self._receipted_value = _create_decimal(0)
        self._code = None
        self._datetime = None
        self._uid = None
