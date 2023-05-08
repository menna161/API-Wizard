import uuid
import datetime as _datetime
import time as _time
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.ObjectStore import MutexTimeoutError
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
from Acquire.ObjectStore import MutexTimeoutError
from Acquire.ObjectStore import MutexTimeoutError


def expired(self):
    'Return whether or not this lock has expired\n\n           Returns:\n                bool: True if lock has expired, else False\n        '
    if (self._is_locked > 0):
        from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
        return (self._end_lease < _get_datetime_now())
    else:
        return False
