from Acquire.Client import Location as _Location
from Acquire.Client import User as _User
from Acquire.Client import ACLRule as _ACLRule
from Acquire.Client import Authorisation as _Authorisation
from Acquire.Crypto import PrivateKey as _PrivateKey
from Acquire.Client import StorageCreds as _StorageCreds
from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
from Acquire.Client import Location as _Location
from Acquire.Client import ACLRule as _ACLRule
from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
from Acquire.ObjectStore import get_datetime_future as _get_datetime_future
from Acquire.ObjectStore import datetime_to_datetime as _datetime_to_datetime
from Acquire.Client import ACLRule as _ACLRule
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
from Acquire.Crypto import Hash
from Acquire.Client import DriveMeta as _DriveMeta
from Acquire.Client import Drive as _Drive
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
from Acquire.Client import FileMeta as _FileMeta
from Acquire.Client import File as _File
from Acquire.Client import FileMeta as _FileMeta
from Acquire.Client import File as _File
from Acquire.ObjectStore import string_to_list as _string_to_list


def seconds_remaining(self, buffer=30):
    "Return the number of seconds remaining before this PAR expires.\n           This will return 0 if the PAR has already expired. To be safe,\n           you should renew PARs if the number of seconds remaining is less\n           than 60. This will subtract 'buffer' seconds from the actual\n           validity to provide a buffer against race conditions (function\n           says this is valid when it is not)\n\n           Args:\n                buffer (int, default=30): buffer PAR validity (seconds)\n           Returns:\n                datetime: Seconds remaining on PAR validity\n        "
    if (not self.is_authorised()):
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
