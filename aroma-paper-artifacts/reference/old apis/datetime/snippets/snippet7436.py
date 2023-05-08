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


def set_logged_out(self, authorisation=None, signature=None):
    'Register that this request has been closed as\n           the user has logged out. If an authorisation is\n           passed then verify that this is correct\n        '
    if self.is_null():
        raise PermissionError('You cannot logout from a null LoginSession!')
    if (authorisation is not None):
        from Acquire.Identity import Authorisation as _Authorisation
        if (not isinstance(authorisation, _Authorisation)):
            raise TypeError('The authorisation must be type Authorisation')
        authorisation.verify(resource=('logout %s' % self.uid()))
        if (authorisation.user_uid() != self.user_uid()):
            raise PermissionError(("The user '%s' does not have permission to logout a session owned by %s" % (authorisation.user_uid(), self.user_uid())))
    if (signature is not None):
        message = ('logout %s' % self.uid())
        self._pubcert.verify(signature=signature, message=message)
    from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
    self._logout_datetime = _get_datetime_now()
    self._clear_keys()
    self._set_status('logged_out')
