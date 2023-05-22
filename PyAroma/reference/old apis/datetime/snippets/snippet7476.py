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


def seconds_remaining_on_lease(self):
    'Return the number of seconds remaining on this lease. You must\n           unlock the mutex before the lease expires, or else an exception\n           will be raised when you unlock, and you will likely have\n           a race condition\n\n           Returns:\n                datetime: Time remaining on lease\n        '
    if self.is_locked():
        from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
        now = _get_datetime_now()
        if (self._end_lease > now):
            return (self._end_lease - now).seconds
        else:
            return 0
    else:
        return 0
