from enum import Enum as _Enum
from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
from Acquire.Accounting import create_decimal as _create_decimal
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
import copy as _copy
from Acquire.Accounting import create_decimal as _create_decimal


def to_key(self):
    'Return this transaction encoded to a key'
    from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
    return ('%s/%s/%s' % (_datetime_to_string(self._datetime), self._uid, TransactionInfo.encode(code=self._code, value=self._value, receipted_value=self._receipted_value)))
