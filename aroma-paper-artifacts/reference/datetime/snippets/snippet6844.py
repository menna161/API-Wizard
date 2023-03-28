from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
from Acquire.ObjectStore import create_uuid as _create_uuid
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
from Acquire.Service import get_trusted_service as _get_trusted_service
from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
from Acquire.Crypto import PublicKey as _PublicKey
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.ObjectStore import get_datetime_now_to_string as _get_datetime_now_to_string
from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
import datetime as _datetime
from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
from Acquire.ObjectStore import bytes_to_string as _bytes_to_string
from Acquire.Client import User as _User
from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
from Acquire.ObjectStore import string_to_bytes as _string_to_bytes


def is_stale(self, stale_time=7200):
    "Return whether or not this authorisation is stale.\n           'stale_time' is the number of seconds after which\n           the authorisation is considered stale (and thus\n           no longer valid)\n        "
    stale_time = self._fix_integer(stale_time, ((365 * 24) * 7200))
    from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
    now = _get_datetime_now()
    if (now >= self._auth_datetime):
        return ((now - self._auth_datetime).seconds > stale_time)
    else:
        leeway_seconds = 30
        return ((self._auth_datetime - now).seconds > leeway_seconds)
