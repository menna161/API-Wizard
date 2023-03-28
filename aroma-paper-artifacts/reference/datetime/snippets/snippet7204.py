from Acquire.Client import File as _File
from Acquire.Storage import ACLRule as _ACLRule
from Acquire.Client import DriveMeta as _DriveMeta
from Acquire.Client import Location as _Location
from Acquire.Storage import ACLRules as _ACLRules
from Acquire.Access import get_size_and_checksum as _get_size_and_checksum
from Acquire.Access import get_filesize_and_checksum as _get_filesize_and_checksum
from Acquire.Storage import FileValidationError
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
from copy import copy as _copy
from copy import copy as _copy
from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
from Acquire.Client import ACLRule as _ACLRule
from Acquire.Storage import ACLRules as _ACLRules


def to_data(self):
    'Return a json-serialisable dictionary of this object'
    data = {}
    if self.is_null():
        return data
    data['filename'] = str(self._filename)
    if (self._uid is not None):
        data['uid'] = str(self._uid)
    if (self._filesize is not None):
        data['filesize'] = self._filesize
    if (self._checksum is not None):
        data['checksum'] = self._checksum
    if (self._user_guid is not None):
        data['user_guid'] = self._user_guid
    if (self._compression is not None):
        data['compression'] = self._compression
    try:
        acl = self._acl
    except:
        acl = None
    if (acl is not None):
        data['acl'] = acl.to_data()
    try:
        aclrules = self._aclrules
    except:
        aclrules = None
    if (aclrules is not None):
        data['aclrules'] = aclrules.to_data()
    if (self._datetime is not None):
        from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
        data['datetime'] = _datetime_to_string(self._datetime)
    return data
