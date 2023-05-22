from Acquire.Identity import _encode_username
from Acquire.Service import get_this_service as _get_this_service
from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
from Acquire.Crypto import PublicKey as _PublicKey
from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
from Acquire.ObjectStore import create_uuid as _create_uuid
from Acquire.Identity import LoginSessionError
from Acquire.Identity import LoginSessionError
from Acquire.ObjectStore import create_uuid as _create_uuid
from Acquire.Identity import LoginSessionError
from Acquire.Identity import LoginSessionError
from Acquire.Identity import Authorisation as _Authorisation
from Acquire.Identity import LoginSessionError
from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
from Acquire.Crypto import PublicKey as _PublicKey
from Acquire.Identity import LoginSessionError


def set_approved(self, user_uid=None, device_uid=None):
    'Register that this request has been approved, optionally\n           providing data about the user who approved the session\n           and the device from which the session was approved\n        '
    if self.is_null():
        raise PermissionError('You cannot approve a null LoginSession!')
    if (self.status() != 'pending'):
        from Acquire.Identity import LoginSessionError
        raise LoginSessionError(("You cannot approve a login session that is not in the 'unapproved' state. This login session is in the '%s' state." % self.status()))
    from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
    self._login_datetime = _get_datetime_now()
    self._user_uid = user_uid
    self._device_uid = device_uid
    self._set_status('approved')
