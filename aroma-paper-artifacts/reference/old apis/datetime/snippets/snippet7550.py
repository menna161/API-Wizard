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


def __init__(self, url=None, key=None, encrypt_key=None, expires_datetime=None, is_readable=False, is_writeable=False, driver_details=None):
    "Construct an OSPar result by passing in the URL at which the\n           object can be accessed, the UTC datetime when this expires,\n           whether this is readable or writeable, and\n           the encryption key to use to encrypt the OSPar.\n\n           You can optionally pass in the key for the object in the\n           object store that\n           this provides access to. If this is not supplied, then an\n           entire bucket is accessed). If 'is_readable', then read-access\n           has been granted, while if 'is_writeable' then write\n           access has been granted.\n\n           Otherwise no access is possible.\n\n           driver_details is provided by the machinery that creates\n           the OSPar, and supplies extra details that are used by the\n           driver to create, register and manage OSPars... You should\n           not do anything with driver_details yourself\n        "
    service_url = None
    if (url is None):
        is_readable = True
        self._uid = None
    else:
        from Acquire.Crypto import PublicKey as _PublicKey
        from Acquire.Crypto import PrivateKey as _PrivateKey
        if isinstance(encrypt_key, _PrivateKey):
            encrypt_key = encrypt_key.public_key()
        if (not isinstance(encrypt_key, _PublicKey)):
            raise TypeError('You must supply a valid PublicKey to encrypt a OSPar')
        url = encrypt_key.encrypt(url)
        from Acquire.ObjectStore import create_uid as _create_uid
        self._uid = _create_uid()
        try:
            from Acquire.Service import get_this_service as _get_this_service
            service_url = _get_this_service().canonical_url()
        except:
            pass
    self._url = url
    self._key = key
    self._expires_datetime = expires_datetime
    self._service_url = service_url
    if (driver_details is not None):
        if (not isinstance(driver_details, dict)):
            raise TypeError('The driver details must be a dictionary')
    self._driver_details = driver_details
    if is_readable:
        self._is_readable = True
    else:
        self._is_readable = False
    if is_writeable:
        self._is_writeable = True
    else:
        self._is_writeable = False
    if (not (self._is_readable or self._is_writeable)):
        from Acquire.Client import PARPermissionsError
        raise PARPermissionsError('You cannot create a OSPar that has no read or write permissions!')
