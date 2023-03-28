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
def list_versions(drive, filename, identifiers=None, upstream=None, include_metadata=False):
    "List all of the versions of this file. If 'include_metadata'\n           is True then this will load all of the associated metadata\n           for each file\n        "
    from Acquire.Storage import DriveInfo as _DriveInfo
    from Acquire.Storage import FileMeta as _FileMeta
    if (not isinstance(drive, _DriveInfo)):
        raise TypeError('The drive must be of type DriveInfo')
    from Acquire.ObjectStore import ObjectStore as _ObjectStore
    from Acquire.ObjectStore import string_to_encoded as _string_to_encoded
    metadata_bucket = drive._get_metadata_bucket()
    encoded_filename = _string_to_encoded(filename)
    version_root = ('%s/%s/%s/' % (_version_root, drive.uid(), encoded_filename))
    versions = []
    if include_metadata:
        objs = _ObjectStore.get_all_objects_from_json(bucket=metadata_bucket, prefix=version_root)
        for data in objs.values():
            version = VersionInfo.from_data(data)
            filemeta = FileInfo._get_filemeta(filename=filename, version=version, identifiers=identifiers, upstream=upstream)
            if (not filemeta.acl().denied_all()):
                versions.append(filemeta)
    else:
        from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
        keys = _ObjectStore.get_all_object_names(bucket=metadata_bucket, prefix=version_root)
        for key in keys:
            parts = key.split('/')
            uploaded_when = _string_to_datetime(parts[(- 2)])
            uid = ('%s/%s' % (parts[(- 2)], parts[(- 1)]))
            filemeta = _FileMeta(filename=filename, uploaded_when=uploaded_when, uid=uid)
            versions.append(filemeta)
    return versions
