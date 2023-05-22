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


@staticmethod
def from_data(data):
    'Return an authorisation created from the json-decoded dictionary'
    auth = Authorisation()
    if (data and (len(data) > 0)):
        from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
        from Acquire.ObjectStore import string_to_bytes as _string_to_bytes
        auth._user_uid = data['user_uid']
        auth._session_uid = data['session_uid']
        auth._identity_url = data['identity_url']
        auth._identity_uid = data['identity_uid']
        auth._uid = data['uid']
        parts = auth._uid.split('/')
        auth._auth_datetime = _string_to_datetime(parts[0])
        auth._signature = _string_to_bytes(data['signature'])
        auth._siguid = _string_to_bytes(data['siguid'])
        auth._last_validated_datetime = None
        if ('is_testing' in data):
            auth._is_testing = data['is_testing']
    return auth
