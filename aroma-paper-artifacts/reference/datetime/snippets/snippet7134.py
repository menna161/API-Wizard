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


def __init__(self, filesize=None, checksum=None, aclrules=None, is_chunked=False, compression=None, identifiers=None):
    'Construct the version of the file that has the passed\n           size and checksum, was uploaded by the specified user,\n           and that has the specified aclrules, and whether or not\n           this file is stored and transmitted in a compressed\n           state\n        '
    if is_chunked:
        from Acquire.ObjectStore import create_uid as _create_uid
        from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
        from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
        from Acquire.Storage import ACLRules as _ACLRules
        try:
            user_guid = identifiers['user_guid']
        except:
            user_guid = None
        if (user_guid is None):
            raise PermissionError('You must specify the user_guid of the user who is uploading this version of the file!')
        if (aclrules is None):
            from Acquire.Identity import ACLRules as _ACLRules
            aclrules = _ACLRules.inherit()
        elif (not isinstance(aclrules, _ACLRules)):
            raise TypeError('The aclrules must be type ACLRules')
        self._filesize = 0
        self._nchunks = 0
        self._checksum = None
        self._compression = None
        self._datetime = _get_datetime_now()
        self._file_uid = ('%s/%s' % (_datetime_to_string(self._datetime), _create_uid(short_uid=True)))
        self._user_guid = str(user_guid)
        self._aclrules = aclrules
    elif (filesize is not None):
        from Acquire.ObjectStore import create_uid as _create_uid
        from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
        from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
        from Acquire.Storage import ACLRules as _ACLRules
        try:
            user_guid = identifiers['user_guid']
        except:
            user_guid = None
        if (user_guid is None):
            raise PermissionError('You must specify the user_guid of the user who is uploading this version of the file!')
        if (aclrules is None):
            from Acquire.Identity import ACLRules as _ACLRules
            aclrules = _ACLRules.inherit()
        elif (not isinstance(aclrules, _ACLRules)):
            raise TypeError('The aclrules must be type ACLRules')
        self._filesize = filesize
        self._checksum = checksum
        self._datetime = _get_datetime_now()
        self._file_uid = ('%s/%s' % (_datetime_to_string(self._datetime), _create_uid(short_uid=True)))
        self._user_guid = str(user_guid)
        self._compression = compression
        self._aclrules = aclrules
        self._nchunks = None
    else:
        self._filesize = None
        self._nchunks = None
