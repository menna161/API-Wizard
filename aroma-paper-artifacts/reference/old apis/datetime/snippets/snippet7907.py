from enum import Enum as _Enum
from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
from Acquire.Accounting import create_decimal as _create_decimal
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
import copy as _copy
from Acquire.Accounting import create_decimal as _create_decimal


def datetime(self):
    'Return the datetime of this transaction'
    return self._datetime
