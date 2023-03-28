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


def __init__(self, location=None, user=None, aclrule=None, expires_datetime=None):
    "Construct a PAR for the specified location,\n           authorised by the passed user, giving permissions\n           according to the passed 'aclrule' (default is\n           ACLRule.reader()).\n\n           The passed 'expires_datetime' is the time at which\n           this PAR will expire (by default within 24 hours)\n        "
    self._location = None
    self._uid = None
    self._expires_datetime = None
    if (location is None):
        return
    from Acquire.Client import Location as _Location
    if (not isinstance(location, _Location)):
        raise TypeError('The location must be type Location')
    if location.is_null():
        return
    from Acquire.Client import User as _User
    if (not isinstance(user, _User)):
        raise TypeError('The user must be type User')
    if (not user.is_logged_in()):
        raise PermissionError('The passed User must be logged in!')
    from Acquire.Client import ACLRule as _ACLRule
    if (aclrule is None):
        aclrule = _ACLRule.reader()
    elif (not isinstance(aclrule, _ACLRule)):
        raise TypeError('The aclrule must be type ACLRule')
    if (expires_datetime is None):
        from Acquire.ObjectStore import get_datetime_future as _get_datetime_future
        expires_datetime = _get_datetime_future(days=1)
    else:
        from Acquire.ObjectStore import datetime_to_datetime as _datetime_to_datetime
        expires_datetime = _datetime_to_datetime(expires_datetime)
    self._location = location
    self._expires_datetime = expires_datetime
    self._aclrule = aclrule
    from Acquire.Client import Authorisation as _Authorisation
    auth = _Authorisation(user=user, resource=('create_par %s' % self.fingerprint()))
    from Acquire.Crypto import PrivateKey as _PrivateKey
    self._secret = _PrivateKey.random_passphrase()
    args = {'authorisation': auth.to_data(), 'par': self.to_data(), 'secret': self._secret}
    service = location.service()
    result = service.call_function(function='create_par', args=args)
    self._set_uid(result['par_uid'])
