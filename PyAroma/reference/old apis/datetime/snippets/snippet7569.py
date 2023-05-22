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


def seconds_remaining(self, buffer=30):
    "Return the number of seconds remaining before this OSPar expires.\n           This will return 0 if the OSPar has already expired. To be safe,\n           you should renew PARs if the number of seconds remaining is less\n           than 60. This will subtract 'buffer' seconds from the actual\n           validity to provide a buffer against race conditions (function\n           says this is valid when it is not)\n\n           Args:\n                buffer (int, default=30): buffer OSPar validity (seconds)\n           Returns:\n                datetime: Seconds remaining on OSPar validity\n        "
    if self.is_null():
        return 0
    from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
    buffer = float(buffer)
    if (buffer < 0):
        buffer = 0
    now = _get_datetime_now()
    delta = ((self._expires_datetime - now).total_seconds() - buffer)
    if (delta < 0):
        return 0
    else:
        return delta
