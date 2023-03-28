from Acquire.ObjectStore import string_to_encoded as _string_to_encoded
from Acquire.Identity import UsernameError
from Acquire.ObjectStore import create_uuid as _create_uuid
from Acquire.Crypto import PrivateKey as _PrivateKey
from Acquire.Crypto import PublicKey as _PublicKey
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.ObjectStore import bytes_to_string as _bytes_to_string
from Acquire.Identity import UserCredentials as _UserCredentials
from Acquire.ObjectStore import get_datetime_now_to_string as _get_datetime_now_to_string
from Acquire.Identity import UserCredentials as _UserCredentials
from Acquire.Service import get_this_service as _get_this_service
from Acquire.Service import get_this_service as _get_this_service
from Acquire.Service import get_this_service as _get_this_service
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.Client import Credentials as _Credentials
from Acquire.Identity import UserCredentials as _UserCredentials
from Acquire.Service import get_this_service as _get_this_service
from Acquire.Identity import UserValidationError
from Acquire.Crypto import PrivateKey as _PrivateKey


@staticmethod
def create(username, password, _service_uid=None, _service_public_key=None):
    "Create a new account with username 'username', which will\n           be secured using the passed password.\n\n           Note that this will create an account with a specified\n           user UID, meaning that different users can have the same\n           username. We identify the right user via the combination\n           of username, password and OTP code.\n\n           Normally the UID of the service, and the skeleton key\n           used to encrypt the backup password are obtained\n           directly from the service. However, when initialising\n           a new service we must pass these directly. In those\n           cases, pass the object using _service_uid and\n           _service_public_key\n\n           This returns a tuple of the user_uid and OTP for the\n           newly-created account\n        "
    from Acquire.ObjectStore import create_uuid as _create_uuid
    from Acquire.Crypto import PrivateKey as _PrivateKey
    from Acquire.Crypto import PublicKey as _PublicKey
    from Acquire.ObjectStore import ObjectStore as _ObjectStore
    from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
    from Acquire.ObjectStore import bytes_to_string as _bytes_to_string
    from Acquire.Identity import UserCredentials as _UserCredentials
    from Acquire.ObjectStore import get_datetime_now_to_string as _get_datetime_now_to_string
    if (_service_public_key is None):
        from Acquire.Service import get_this_service as _get_this_service
        service_pubkey = _get_this_service().public_skeleton_key()
        assert (service_pubkey is not None)
    else:
        service_pubkey = _service_public_key
    if (not isinstance(service_pubkey, _PublicKey)):
        raise TypeError('The service public key must be type PublicKey')
    if (_service_uid is None):
        from Acquire.Service import get_this_service as _get_this_service
        service_uid = _get_this_service(need_private_access=False).uid()
    else:
        service_uid = _service_uid
    user_uid = _create_uuid()
    privkey = _PrivateKey(name=('user_secret_key %s %s' % (username, user_uid)))
    primary_password = _PrivateKey.random_passphrase()
    bucket = _get_service_account_bucket()
    otp = _UserCredentials.create(user_uid=user_uid, password=password, primary_password=primary_password)
    user = UserAccount(username=username, user_uid=user_uid, private_key=privkey, status='active')
    recovery_password = _bytes_to_string(service_pubkey.encrypt(primary_password))
    key = ('%s/names/%s/%s' % (_user_root, user.encoded_name(), user_uid))
    _ObjectStore.set_string_object(bucket=bucket, key=key, string_data=recovery_password)
    encoded_password = _UserCredentials.hash(username=username, password=password, service_uid=service_uid)
    key = ('%s/passwords/%s/%s' % (_user_root, encoded_password, user_uid))
    _ObjectStore.set_string_object(bucket=bucket, key=key, string_data=_get_datetime_now_to_string())
    key = ('%s/uids/%s' % (_user_root, user_uid))
    data = user.to_data(passphrase=primary_password)
    _ObjectStore.set_object_from_json(bucket=bucket, key=key, data=data)
    return (user_uid, otp)
