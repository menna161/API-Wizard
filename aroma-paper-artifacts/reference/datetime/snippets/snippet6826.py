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


def _get_message(self, resource=None, matched_resource=False):
    "Internal function that is used to generate the message for\n           the resource that is signed. This message\n           encodes information about the user and identity service that\n           signed the message, as well as the resource. This helps\n           prevent tamporing with the data in this authorisation.\n\n           If 'matched_resource' is True then this will return the\n           message based on the previously-verified resource\n           (as we have already determined that the user knows what\n           the resource is)\n        "
    from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
    if matched_resource:
        resource = self._last_verified_resource
    if (resource is None):
        return ('%s|%s|%s|%s' % (self._user_uid, self._session_uid, self._identity_uid, _datetime_to_string(self._auth_datetime)))
    else:
        return ('%s|%s|%s|%s|%s' % (self._user_uid, self._session_uid, self._identity_uid, str(resource), _datetime_to_string(self._auth_datetime)))
