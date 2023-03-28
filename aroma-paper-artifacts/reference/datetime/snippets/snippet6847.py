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


def is_verified(self, refresh_time=3600, stale_time=7200):
    "Return whether or not this authorisation has been verified. Note\n           that this will cache any verification for 'refresh_time' (in\n           seconds)\n\n           'stale_time' gives the time (in seconds) beyond which the\n           authorisation will be considered stale (and thus not valid).\n           By default this is 7200 seconds (2 hours), meaning that the\n           authorisation must be used within 2 hours to be valid.\n        "
    refresh_time = self._fix_integer(refresh_time, (24 * 3600))
    from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
    now = _get_datetime_now()
    if (self._last_validated_datetime is not None):
        if ((now - self._last_validated_datetime).seconds < refresh_time):
            return (not self.is_stale(stale_time))
    return False
