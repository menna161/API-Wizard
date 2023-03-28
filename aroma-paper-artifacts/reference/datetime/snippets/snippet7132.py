from Acquire.Client import compress as _compress
from Acquire.Access import get_filesize_and_checksum as _get_filesize_and_checksum
import os as _os
import os as _os
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
from Acquire.Storage import ACLRule as _ACLRule
from Acquire.Identity import ACLRules as _ACLRules
import bz2 as _bz2
from Acquire.ObjectStore import string_to_filepath as _string_to_filepath
import bz2 as _bz2
from Acquire.ObjectStore import bytes_to_string as _bytes_to_string
from Acquire.Storage import ACLRules as _ACLRules
from Acquire.ObjectStore import string_to_bytes as _string_to_bytes
from Acquire.Access import get_size_and_checksum as _get_size_and_checksum


def to_data(self):
    'Return a json-serialisable dictionary for this object. Note\n           that this does not contain any information about the local\n           file itself - just the name it should be called on the\n           object store and the size, checksum and acl. If the file\n           (or compressed file) is sufficiently small then this\n           will also contain the packed version of that file data\n\n           Returns:\n                dict: JSON serialisable dictionary of object\n        '
    data = {}
    if (not self.is_null()):
        from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
        data['filename'] = self.filename()
        data['filesize'] = self.filesize()
        data['checksum'] = self.checksum()
        if (self._aclrules is not None):
            data['aclrules'] = self._aclrules.to_data()
        data['drive_uid'] = self.drive_uid()
        if (self._local_filedata is not None):
            from Acquire.ObjectStore import bytes_to_string as _bytes_to_string
            data['filedata'] = _bytes_to_string(self._local_filedata)
        if (self._compression is not None):
            data['compression'] = self._compression
    return data
