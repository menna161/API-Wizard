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


def last_verification_time(self):
    'Return the last time this authorisation was verified. Note that\n           you should re-verify authorisations periodically, to ensure that\n           they identity service is still happy that the login session was\n           not suspicious\n        '
    if self.is_null():
        return None
    else:
        return self._last_validated_datetime
