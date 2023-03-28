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


def __init__(self, resource=None, user=None, testing_key=None, testing_user_guid=None):
    'Create an authorisation for the passed resource\n           that is authorised by the passed user (who must be authenticated)\n\n           If testing_key is passed, then this authorisation is being\n           tested as part of the unit tests\n        '
    if (resource is not None):
        resource = str(resource)
    self._signature = None
    self._last_validated_datetime = None
    self._scope = None
    self._permissions = None
    self._pubcert = None
    if (resource is not None):
        if ((user is None) and (testing_key is None)):
            raise ValueError(("You must pass in an authenticated user who will provide authorisation for resource '%s'" % resource))
    from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
    from Acquire.ObjectStore import create_uuid as _create_uuid
    if (user is not None):
        from Acquire.Client import User as _User
        if (not isinstance(user, _User)):
            raise TypeError('The passed user must be of type User')
        elif (not user.is_logged_in()):
            raise PermissionError("The passed user '%s' must be authenticated to enable you to generate an authorisation for the account")
        self._user_uid = user.uid()
        self._session_uid = user.session_uid()
        self._identity_url = user.identity_service().canonical_url()
        self._identity_uid = user.identity_service_uid()
        self._auth_datetime = _get_datetime_now()
        self._uid = _create_uuid(short_uid=True, include_date=self._auth_datetime)
        self._siguid = user.signing_key().sign(self._uid)
        message = self._get_message(resource)
        self._signature = user.signing_key().sign(message)
        self._last_validated_datetime = _get_datetime_now()
        self._last_verified_resource = resource
        self._last_verified_key = None
        if (user.guid() != self.user_guid()):
            raise PermissionError(('We do not yet support a single user being identified by multiple identity services: %s versus %s' % (user.guid(), self.user_guid())))
    elif (testing_key is not None):
        self._user_uid = 'some user uid'
        self._session_uid = 'some session uid'
        self._identity_url = 'some identity_url'
        self._identity_uid = 'some identity uid'
        self._auth_datetime = _get_datetime_now()
        self._uid = _create_uuid(short_uid=True, include_date=self._auth_datetime)
        self._is_testing = True
        self._testing_key = testing_key
        if (testing_user_guid is not None):
            parts = testing_user_guid.split('@')
            self._user_uid = parts[0]
            self._identity_uid = parts[1]
        message = self._get_message(resource)
        self._signature = testing_key.sign(message)
        self._siguid = testing_key.sign(self._uid)
        self._last_validated_datetime = _get_datetime_now()
        self._last_verified_resource = resource
        self._last_verified_key = testing_key.public_key()
