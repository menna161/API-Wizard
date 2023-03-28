from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.Crypto import Hash as _Hash
from hashlib import md5 as _md5
from Acquire.Client import FileMeta as _FileMeta
from Acquire.Client import FileMeta as _FileMeta
from Acquire.Storage import MissingVersionError
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.Storage import DriveInfo as _DriveInfo
from Acquire.Storage import FileMeta as _FileMeta
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.ObjectStore import string_to_encoded as _string_to_encoded
from Acquire.Storage import DriveInfo as _DriveInfo
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.ObjectStore import string_to_encoded as _string_to_encoded
from Acquire.ObjectStore import create_uid as _create_uid
from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
from Acquire.Storage import ACLRules as _ACLRules
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
from Acquire.ObjectStore import dict_to_string as _dict_to_string
from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
from Acquire.ObjectStore import string_to_encoded as _string_to_encoded
from Acquire.ObjectStore import string_to_filepath as _string_to_filepath
from Acquire.Storage import DriveInfo as _DriveInfo
from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
from Acquire.Storage import MissingFileError
from Acquire.ObjectStore import string_to_encoded as _string_to_encoded
from Acquire.Identity import ACLRules as _ACLRules
from Acquire.ObjectStore import create_uid as _create_uid
from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
from Acquire.Storage import ACLRules as _ACLRules
from Acquire.Storage import ACLRules as _ACLRules
from Acquire.Storage import FileHandle as _FileHandle
from Acquire.ObjectStore import string_to_encoded as _string_to_encoded
from Acquire.ObjectStore import string_to_filepath as _string_to_filepath
from Acquire.Identity import ACLRules as _ACLRules


def datetime(self):
    'Return the datetime when this version was created'
    if self.is_null():
        return None
    else:
        return self._datetime
