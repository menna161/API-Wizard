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


def _set_denied(self):
    'Call this function to remove all information that should\n           not be visible to someone who has denied access to the file\n        '
    self._uid = None
    self._filesize = None
    self._checksum = None
    self._user_guid = None
    self._datetime = None
    self._compression = None
    self._aclrules = None
    self._creds = None
    self._drive_metadata = None
    from Acquire.Storage import ACLRule as _ACLRule
    self._acl = _ACLRule.denied()
