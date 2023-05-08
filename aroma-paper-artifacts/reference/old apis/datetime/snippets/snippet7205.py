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


@staticmethod
def from_data(data):
    'Return a new FileMeta constructed from the passed json-deserialised\n           dictionary\n        '
    f = FileMeta()
    if ((data is not None) and (len(data) > 0)):
        f._filename = data['filename']
        if ('uid' in data):
            f._uid = data['uid']
        if ('filesize' in data):
            f._filesize = data['filesize']
        if ('checksum' in data):
            f._checksum = data['checksum']
        if ('user_guid' in data):
            f._user_guid = data['user_guid']
        if ('datetime' in data):
            from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
            f._datetime = _string_to_datetime(data['datetime'])
        if ('compression' in data):
            f._compression = data['compression']
        if ('acl' in data):
            from Acquire.Client import ACLRule as _ACLRule
            f._acl = _ACLRule.from_data(data['acl'])
        if ('aclrules' in data):
            from Acquire.Storage import ACLRules as _ACLRules
            f._aclrules = _ACLRules.from_data(data['aclrules'])
    return f
