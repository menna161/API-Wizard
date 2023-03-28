import datetime as _datetime
import json as _json
import os as _os
from Acquire.Crypto import PrivateKey as _PrivateKey
from Acquire.Crypto import PrivateKey as _PrivateKey
from hashlib import md5 as _md5
from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
import copy as _copy
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
from Acquire.ObjectStore import bytes_to_string as _bytes_to_string
from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
from Acquire.ObjectStore import string_to_bytes as _string_to_bytes
from Acquire.Stubs import requests as _requests
from Acquire.Client import PARReadError
from Acquire.Stubs import requests as _requests
from Acquire.Client import PARWriteError
from Acquire.Crypto import PublicKey as _PublicKey
from Acquire.Crypto import PrivateKey as _PrivateKey
from Acquire.ObjectStore import create_uid as _create_uid
from Acquire.Client import PARPermissionsError
from Acquire.Client import PARTimeoutError
from Acquire.Service import get_trusted_service as _get_trusted_service
from Acquire.Client import PARPermissionsError
from Acquire.Client import PARPermissionsError
from Acquire.Client import PARReadError
from Acquire.Client import PARWriteError
from Acquire.Client import PARError
from Acquire.Client import PARError
from Acquire.Client import PARError
from Acquire.Client import PARError
from Acquire.Service import get_this_service as _get_this_service
from Acquire.Crypto import PrivateKey as _PrivateKey
from Acquire.Client import PARPermissionsError
from Acquire.Client import PARPermissionsError
from Acquire.Client import PARPermissionsError
from Acquire.Client import PARPermissionsError


def to_data(self, passphrase=None):
    'Return a json-serialisable dictionary that contains all data\n           for this object\n\n           Args:\n                passphrase (str, default=None): Passphrase to use to\n                encrypt OSPar\n           Returns:\n                dict: JSON serialisable dictionary\n        '
    data = {}
    if (self._url is None):
        return data
    from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
    from Acquire.ObjectStore import bytes_to_string as _bytes_to_string
    data['url'] = _bytes_to_string(self._url)
    data['uid'] = self._uid
    data['key'] = self._key
    data['expires_datetime'] = _datetime_to_string(self._expires_datetime)
    data['is_readable'] = self._is_readable
    data['is_writeable'] = self._is_writeable
    try:
        if (self._service_url is not None):
            data['service_url'] = self._service_url
    except:
        pass
    try:
        privkey = self._privkey
    except:
        privkey = None
    if (privkey is not None):
        if (passphrase is not None):
            data['privkey'] = privkey.to_data(passphrase)
    return data
