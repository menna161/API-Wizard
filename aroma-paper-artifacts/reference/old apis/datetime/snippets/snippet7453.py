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


def to_data(self):
    'Return a data version (dictionary) of this LoginSession\n           that can be serialised to json\n        '
    if self.is_null():
        return {}
    from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
    data = {}
    data['uid'] = self._uid
    data['username'] = self._username
    data['request_datetime'] = _datetime_to_string(self._request_datetime)
    data['public_certificate'] = self._pubcert.to_data()
    data['status'] = self._status
    if (self._pubkey is not None):
        data['public_key'] = self._pubkey.to_data()
    try:
        data['login_datetime'] = _datetime_to_string(self._login_datetime)
    except:
        pass
    try:
        data['logout_datetime'] = _datetime_to_string(self._logout_datetime)
    except:
        pass
    try:
        data['ipaddr'] = self._ipaddr
    except:
        pass
    try:
        data['hostname'] = self._hostname
    except:
        pass
    try:
        data['login_message'] = self._login_message
    except:
        pass
    try:
        data['scope'] = self._scope
    except:
        pass
    try:
        data['permissions'] = self._permissions
    except:
        pass
    try:
        data['user_uid'] = self._user_uid
    except:
        pass
    try:
        data['device_uid'] = self._device_uid
    except:
        pass
    return data
