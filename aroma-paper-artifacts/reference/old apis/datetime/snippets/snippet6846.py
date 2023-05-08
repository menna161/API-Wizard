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


def assert_once(self, stale_time=7200, scope=None, permissions=None):
    'Assert that this is in the one and only time that this\n           service has seen this authorisation. This records the\n           UID of the authorisation to the object store and then\n           verifies that the signature of the UID is correct.\n\n           There is a small race condition if the service asserts\n           the authorisation at the exact same time, but this is\n           a highly unlikely occurance. The aim is to prevent\n           replay attacks.\n        '
    if self.is_null():
        raise PermissionError('Cannot assert_once a null Authorisation')
    if self.is_stale(stale_time):
        if (now < self._auth_datetime):
            raise PermissionError('Cannot assert_once an Authorisation signed in the future - please check your clock')
        else:
            raise PermissionError('Cannot assert_once a stale Authorisation')
    from Acquire.ObjectStore import ObjectStore as _ObjectStore
    from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
    from Acquire.ObjectStore import get_datetime_now_to_string as _get_datetime_now_to_string
    bucket = _get_service_account_bucket()
    authkey = ('auth_once/%s' % self._uid)
    now = _get_datetime_now_to_string()
    try:
        data = _ObjectStore.get_string_object(bucket=bucket, key=authkey)
    except:
        data = None
    if (data is not None):
        raise PermissionError('Cannot auth_once the authorisation as it has been used before on this service!')
    _ObjectStore.set_string_object(bucket=bucket, key=authkey, string_data=now)
    public_cert = self._get_user_public_cert(scope=scope, permissions=permissions)
    if (public_cert is None):
        raise PermissionError(("There is no public certificate for this user in scope '%s' with permissions '%s'" % (scope, permissions)))
    try:
        public_cert.verify(self._siguid, self._uid)
    except Exception as e:
        raise PermissionError(('Cannot auth_once the authorisation as the signature is invalid! % s' % str(e)))
