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


def verify(self, resource=None, refresh_time=3600, stale_time=7200, force=False, accept_partial_match=False, scope=None, permissions=None, return_identifiers=True):
    'Verify that this is a valid authorisation provided by the\n           user for the passed \'resource\'. This will\n           cache the verification for \'refresh_time\' (in seconds), but\n           re-verification can be forced if \'force\' is True.\n\n           \'stale_time\' gives the time (in seconds) beyond which the\n           authorisation will be considered stale (and thus not valid).\n           By default this is 7200 seconds (2 hours), meaning that the\n           authorisation must be used within 2 hours to be valid.\n\n           If \'accept_partial_match\' is True, then if this Authorisation\n           has been previously validated, then this previous authorisation\n           is valid if the previously-verified resource contains\n           \'resource\', e.g. if you have previously verified that\n           "create ABC123" is the verified resource, then this will\n           still verify if "ABC123" if the partially-accepted match\n\n           If \'scope\' is passed, then verify that the user logged in\n           and signed the authorisation with the required \'scope\'.\n\n           If \'permissions\' is passed, then verify that the user\n           logged in and signed the authorisation with at least\n           the specified \'permissions\'\n\n           If \'testing_key\' is passed, then this object is being\n           tested as part of the unit tests\n\n           If the authorisation was verified, then if \'return_identifiers\'\n           is True then this will return the full set of identifiers\n           associated with the user who provided the authorisation\n        '
    if self.is_null():
        raise PermissionError('Cannot verify a null Authorisation')
    from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
    import datetime as _datetime
    if self.is_stale(stale_time):
        now = _get_datetime_now()
        if (now < self._auth_datetime):
            raise PermissionError('Cannot verify an Authorisation signed in the future - please check your clock')
        else:
            raise PermissionError('Cannot verify a stale Authorisation')
    matched_resource = False
    try:
        last_resource = self._last_verified_resource
    except:
        last_resource = None
    if (last_resource is not None):
        if accept_partial_match:
            if (resource is None):
                matched_resource = True
            else:
                matched_resource = (last_resource.find(resource) != (- 1))
        else:
            matched_resource = (resource == last_resource)
    if (not force):
        if self.is_verified(refresh_time=refresh_time, stale_time=stale_time):
            if matched_resource:
                if return_identifiers:
                    return self.identifiers()
                else:
                    return
    public_cert = self._get_user_public_cert(scope=scope, permissions=permissions)
    message = self._get_message(resource=resource, matched_resource=matched_resource)
    try:
        public_cert.verify(self._signature, message)
    except:
        raise PermissionError(("Cannot verify the authorisation as the signature for resource '%s' is invalid!" % resource))
    from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
    self._last_validated_datetime = _get_datetime_now()
    self._last_verified_resource = resource
    self._last_verified_key = public_cert
    if return_identifiers:
        return self.identifiers()
    else:
        return
