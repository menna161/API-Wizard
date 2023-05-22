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


def __str__(self):
    if self.is_null():
        return 'PAR::null'
    elif (not self.is_authorised()):
        return 'PAR::unauthorised'
    else:
        from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
        return ('PAR( %s, %s, expires %s )' % (self._location.to_string(), self._aclrule, _datetime_to_string(self._expires_datetime)))
