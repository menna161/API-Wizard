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


@staticmethod
def from_data(data):
    'Return this object constructed from the passed json-deserialised\n           dictionary\n        '
    v = VersionInfo()
    if ((data is not None) and (len(data) > 0)):
        from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
        v._filesize = data['filesize']
        v._checksum = data['checksum']
        v._file_uid = data['file_uid']
        v._user_guid = data['user_guid']
        try:
            v._datetime = _string_to_datetime(data['datetime'])
            v._file_uid = ('%s/%s' % (data['datetime'], v._file_uid))
        except:
            v._datetime = _string_to_datetime(v._file_uid.split('/')[0])
        if ('aclrules' in data):
            from Acquire.Storage import ACLRules as _ACLRules
            v._aclrules = _ACLRules.from_data(data['aclrules'])
        if ('compression' in data):
            v._compression = data['compression']
        else:
            v._compression = None
        if ('nchunks' in data):
            v._nchunks = int(data['nchunks'])
        else:
            v._nchunks = None
    return v
