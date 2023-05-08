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


def __init__(self, username=None, public_key=None, public_cert=None, ipaddr=None, hostname=None, login_message=None, scope=None, permissions=None):
    'Start a new login session for the user with specified\n           username, passing in the additional data needed to\n           request a login\n        '
    if (public_key is not None):
        from Acquire.Crypto import PublicKey as _PublicKey
        if (not isinstance(public_key, _PublicKey)):
            raise TypeError('The public key must be of type PublicKey')
        if (not isinstance(public_cert, _PublicKey)):
            raise TypeError('The public certificate must be of type PublicKey')
        if ((username is None) or (len(username) == 0)):
            raise PermissionError('You must supply a valid username!')
        self._username = username
        self._pubkey = public_key
        self._pubcert = public_cert
        from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
        from Acquire.ObjectStore import create_uuid as _create_uuid
        self._uid = _create_uuid()
        self._request_datetime = _get_datetime_now()
        self._status = None
        self._ipaddr = ipaddr
        self._hostname = hostname
        self._login_message = login_message
        self._scope = scope
        self._permissions = permissions
        self._set_status('pending')
    else:
        self._uid = None
