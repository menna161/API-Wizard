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


def fully_unlock(self):
    'This fully unlocks the mutex, removing all levels\n           of recursion\n\n           Returns:\n                None\n        '
    if (self._is_locked == 0):
        return
    from Acquire.ObjectStore import ObjectStore as _ObjectStore
    from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
    try:
        holder = _ObjectStore.get_string_object(self._bucket, self._key)
    except:
        holder = None
    if (holder == self._lockstring):
        _ObjectStore.delete_object(self._bucket, self._key)
    self._lockstring = None
    self._is_locked = 0
    if (self._end_lease < _get_datetime_now()):
        self._end_lease = None
        from Acquire.ObjectStore import MutexTimeoutError
        raise MutexTimeoutError('The lease on this mutex expired before this mutex was unlocked!')
    else:
        self._end_lease = None
