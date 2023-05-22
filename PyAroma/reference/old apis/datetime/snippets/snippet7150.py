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


def to_data(self):
    'Return a json-serialisable dictionary for this object'
    data = {}
    if (not self.is_null()):
        from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
        from Acquire.ObjectStore import dict_to_string as _dict_to_string
        data['filesize'] = self._filesize
        data['checksum'] = self._checksum
        data['file_uid'] = self._file_uid
        data['user_guid'] = self._user_guid
        if (self._nchunks is not None):
            data['nchunks'] = int(self._nchunks)
        if (self._aclrules is not None):
            data['aclrules'] = self._aclrules.to_data()
        if (self._compression is not None):
            data['compression'] = self._compression
    return data
