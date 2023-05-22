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


def __init__(self, filename=None, uid=None, filesize=None, checksum=None, uploaded_by=None, uploaded_when=None, compression=None, aclrules=None):
    'Construct, specifying the filename, and then optionally\n           other useful data\n        '
    self._filename = filename
    self._uid = uid
    self._filesize = filesize
    self._checksum = checksum
    self._user_guid = uploaded_by
    self._datetime = uploaded_when
    self._compression = compression
    self._acl = None
    self._aclrules = None
    self._creds = None
    self._drive_metadata = None
    if (aclrules is not None):
        from Acquire.Storage import ACLRules as _ACLRules
        if (not isinstance(aclrules, _ACLRules)):
            raise TypeError('The aclrules must be type ACLRules')
        self._aclrules = aclrules
