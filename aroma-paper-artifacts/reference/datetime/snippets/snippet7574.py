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


@staticmethod
def from_data(data, passphrase=None):
    'Return a OSPar constructed from the passed json-deserliased\n           dictionary\n\n           Args:\n                data (dict): JSON-deserialised dictionary from which to\n                create OSPar\n            Returns:\n                OSPar: OSPar object created from dict\n        '
    if ((data is None) or (len(data) == 0)):
        return OSPar()
    from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
    from Acquire.ObjectStore import string_to_bytes as _string_to_bytes
    par = OSPar()
    par._url = _string_to_bytes(data['url'])
    par._key = data['key']
    par._uid = data['uid']
    if (par._key is not None):
        par._key = str(par._key)
    par._expires_datetime = _string_to_datetime(data['expires_datetime'])
    par._is_readable = data['is_readable']
    par._is_writeable = data['is_writeable']
    if ('service_url' in data):
        par._service_url = data['service_url']
    if ('privkey' in data):
        if (passphrase is not None):
            from Acquire.Crypto import PrivateKey as _PrivateKey
            par._privkey = _PrivateKey.from_data(data['privkey'], passphrase)
    return par
