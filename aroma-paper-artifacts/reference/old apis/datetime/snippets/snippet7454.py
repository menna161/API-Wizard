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


@staticmethod
def from_data(data):
    'Return a LoginSession constructed from the passed data\n           (dictionary)\n        '
    l = LoginSession()
    if ((data is not None) and (len(data) > 0)):
        from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
        from Acquire.Crypto import PublicKey as _PublicKey
        l._uid = data['uid']
        l._username = data['username']
        l._request_datetime = _string_to_datetime(data['request_datetime'])
        l._pubcert = _PublicKey.from_data(data['public_certificate'])
        l._status = data['status']
        try:
            l._pubkey = _PublicKey.from_data(data['public_key'])
        except:
            l._pubkey = None
        try:
            l._login_datatime = _string_to_datetime(data['login_datetime'])
        except:
            pass
        try:
            l._logout_datetime = _string_to_datetime(data['logout_datetime'])
        except:
            pass
        try:
            l._ipaddr = data['ipaddr']
        except:
            pass
        try:
            l._hostname = data['hostname']
        except:
            pass
        try:
            l._login_message = data['login_message']
        except:
            pass
        try:
            l._scope = data['scope']
        except:
            pass
        try:
            l._permissions = data['permissions']
        except:
            pass
        try:
            l._user_uid = data['user_uid']
        except:
            pass
        try:
            l._device_uid = data['device_uid']
        except:
            pass
    return l
