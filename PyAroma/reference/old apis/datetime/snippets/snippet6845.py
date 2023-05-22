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


def _get_user_public_cert(self, scope=None, permissions=None):
    'Internal function that returns the public certificate\n           of the user who signed this authorisation. This will\n           check that the authorisation was not signed after the\n           user logged out, as well as validating the services\n           that provide the user session keys etc.\n        '
    must_fetch = False
    try:
        if ((scope != self._scope) or (permissions != self._permissions)):
            must_fetch = True
    except:
        must_fetch = True
    if (self._pubcert is not None):
        if (not must_fetch):
            try:
                return self._pubcert
            except:
                pass
    try:
        testing_key = self._testing_key
    except:
        testing_key = None
    if (testing_key is not None):
        if (not self._is_testing):
            raise PermissionError('You cannot pass a test key to a non-testing Authorisation')
        return testing_key
    from Acquire.Service import get_trusted_service as _get_trusted_service
    from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
    try:
        identity_service = _get_trusted_service(self._identity_url)
    except:
        raise PermissionError(('Unable to verify the authorisation as we do not trust the identity service at %s' % self._identity_url))
    if (not identity_service.can_identify_users()):
        raise PermissionError('Cannot verify an Authorisation that does not use a valid identity service')
    if (identity_service.uid() != self._identity_uid):
        raise PermissionError(("Cannot auth_once this Authorisation as the actual UID of the identity service at '%s' (%s) does not match the UID of the service that signed this authorisation (%s)" % (self._identity_url, identity_service.uid(), self._identity_uid)))
    response = identity_service.get_session_info(session_uid=self._session_uid, scope=scope, permissions=permissions)
    try:
        user_uid = response['user_uid']
    except:
        pass
    if (self._user_uid != user_uid):
        raise PermissionError(('Cannot verify the authorisation as there is disagreement over the UID of the user who signed the authorisation. %s versus %s' % (self._user_uid, user_uid)))
    try:
        logout_datetime = _string_to_datetime(response['logout_datetime'])
    except:
        logout_datetime = None
    if logout_datetime:
        if (logout_datetime < self.signature_time()):
            raise PermissionError('This authorisation was signed after the user logged out. This means that the authorisation is not valid. Please log in again and create a new authorisation.')
    from Acquire.Crypto import PublicKey as _PublicKey
    pubcert = _PublicKey.from_data(response['public_cert'])
    self._pubcert = pubcert
    self._scope = scope
    self._permissions = permissions
    return pubcert
