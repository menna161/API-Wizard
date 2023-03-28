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


def uploaded_when(self):
    'If known, return the datetime when this version of\n           the file was uploaded\n        '
    if self.is_null():
        return None
    else:
        return self._datetime
