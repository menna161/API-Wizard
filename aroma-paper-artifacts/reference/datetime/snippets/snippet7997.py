from Acquire.Crypto import Hash as _Hash
from Acquire.Service import get_this_service as _get_this_service
from Acquire.Crypto import PrivateKey as _PrivateKey
from Acquire.Crypto import OTP as _OTP
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.ObjectStore import bytes_to_string as _bytes_to_string
from Acquire.Crypto import PrivateKey as _PrivateKey
from Acquire.Crypto import OTP as _OTP
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.ObjectStore import string_to_bytes as _string_to_bytes
from Acquire.Client import Credentials as _Credentials
from Acquire.Crypto import RepeatedOTPCodeError as _RepeatedOTPCodeError
from Acquire.Identity import UserValidationError
from Acquire.Crypto import PrivateKey as _PrivateKey
from Acquire.Crypto import OTP as _OTP
from Acquire.ObjectStore import string_to_bytes as _string_to_bytes
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.Identity import UserAccount as _UserAccount
from Acquire.Identity import UserValidationError
from Acquire.Identity import UserValidationError
from Acquire.ObjectStore import create_uuid as _create_uuid
from Acquire.Client import Credentials as _Credentials
from Acquire.ObjectStore import get_datetime_now_to_string as _get_datetime_now_to_string


@staticmethod
def validate_password(user_uid, username, device_uid, secrets, password, otpcode, remember_device):
    "Validate that the passed password and one-time-code are valid.\n           If they are, then return a tuple of the UserAccount of the unlocked\n           user, the OTP that is used to generate secrets, and the\n           device_uid of the login device\n\n           If 'remember_device' is True and 'device_uid' is None, then\n           this creates a new OTP for the login device, which is returned,\n           and a new device_uid for that device. The password needed to\n           match this device is a MD5 of the normal user password.\n        "
    from Acquire.Crypto import PrivateKey as _PrivateKey
    from Acquire.Crypto import OTP as _OTP
    from Acquire.ObjectStore import string_to_bytes as _string_to_bytes
    privkey = _PrivateKey.from_data(data=secrets['private_key'], passphrase=password)
    data = _string_to_bytes(secrets['otpsecret'])
    otpsecret = privkey.decrypt(data)
    otp = _OTP(secret=otpsecret)
    otp.verify(code=otpcode, once_only=True)
    primary_password = _string_to_bytes(secrets['primary_password'])
    primary_password = privkey.decrypt(primary_password)
    from Acquire.ObjectStore import ObjectStore as _ObjectStore
    from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
    data = None
    secrets = None
    key = ('%s/uids/%s' % (_user_root, user_uid))
    bucket = _get_service_account_bucket()
    try:
        data = _ObjectStore.get_object_from_json(bucket=bucket, key=key)
    except:
        pass
    if (data is None):
        from Acquire.Identity import UserValidationError
        raise UserValidationError('Unable to validate user as no account data is present!')
    from Acquire.Identity import UserAccount as _UserAccount
    user = _UserAccount.from_data(data=data, passphrase=primary_password)
    if (user.uid() != user_uid):
        from Acquire.Identity import UserValidationError
        raise UserValidationError('Unable to validate user as mismatch in user_uids!')
    if ((device_uid is None) and remember_device):
        from Acquire.ObjectStore import create_uuid as _create_uuid
        from Acquire.Client import Credentials as _Credentials
        device_uid = _create_uuid()
        device_password = _Credentials.encode_device_uid(encoded_password=password, device_uid=device_uid)
        otp = UserCredentials.create(user_uid=user_uid, password=device_password, primary_password=primary_password, device_uid=device_uid)
        encoded_password = UserCredentials.hash(username=username, password=device_password)
        key = ('%s/passwords/%s/%s' % (_user_root, encoded_password, user_uid))
        from Acquire.ObjectStore import get_datetime_now_to_string as _get_datetime_now_to_string
        _ObjectStore.set_string_object(bucket=bucket, key=key, string_data=_get_datetime_now_to_string())
    return {'user': user, 'otp': otp, 'device_uid': device_uid}
