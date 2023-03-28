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


def lock(self, timeout=None, lease_time=None):
    "Lock the mutex, blocking until the mutex is held, or until\n           'timeout' seconds have passed. If we time out, then an exception is\n           raised. The lock is held for a maximum of 'lease_time' seconds.\n\n           Args:\n                timeout (int): Number of seconds to block\n                lease_time (int): Number of seconds to hold the lock\n           Returns:\n                None\n        "
    if (timeout is None):
        timeout = 10.0
    else:
        timeout = float(timeout)
    if (lease_time is None):
        lease_time = 10.0
    else:
        lease_time = float(lease_time)
    from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
    from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
    from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
    from Acquire.ObjectStore import ObjectStore as _ObjectStore
    if self.is_locked():
        now = _get_datetime_now()
        if ((now > self._end_lease) or ((now - self._end_lease).seconds < 1)):
            self.fully_unlock()
            self.lock(timeout, lease_time)
        else:
            self._end_lease = (now + _datetime.timedelta(seconds=lease_time))
            self._lockstring = ('%s{}%s' % (self._secret, _datetime_to_string(self._end_lease)))
            _ObjectStore.set_string_object(self._bucket, self._key, self._lockstring)
            self._is_locked += 1
        return
    now = _get_datetime_now()
    endtime = (now + _datetime.timedelta(seconds=timeout))
    while (now < endtime):
        try:
            holder = _ObjectStore.get_string_object(self._bucket, self._key)
        except:
            holder = None
        is_held = True
        if (holder is None):
            is_held = False
        else:
            end_lease = _string_to_datetime(holder.split('{}')[(- 1)])
            if (now > end_lease):
                is_held = False
        if (not is_held):
            self._end_lease = (now + _datetime.timedelta(seconds=lease_time))
            self._lockstring = ('%s{}%s' % (self._secret, _datetime_to_string(self._end_lease)))
            _ObjectStore.set_string_object(self._bucket, self._key, self._lockstring)
            holder = _ObjectStore.get_string_object(self._bucket, self._key)
        else:
            self._lockstring = None
        if (holder == self._lockstring):
            holder = _ObjectStore.get_string_object(self._bucket, self._key)
            if (holder == self._lockstring):
                _ObjectStore.set_string_object(self._bucket, self._key, self._lockstring)
                holder = _ObjectStore.get_string_object(self._bucket, self._key)
        if (holder == self._lockstring):
            self._is_locked = 1
            return
        _time.sleep(0.25)
        now = _get_datetime_now()
    from Acquire.ObjectStore import MutexTimeoutError
    raise MutexTimeoutError(("Cannot acquire a mutex lock on the key '%s'" % self._key))
