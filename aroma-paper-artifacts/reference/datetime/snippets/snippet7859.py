import os as _os
import shutil as _shutil
import datetime as _datetime
import uuid as _uuid
import json as _json
import glob as _glob
import threading
import uuid as _uuid
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
import copy as _copy
from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
import copy as _copy
from Acquire.Crypto import PublicKey as _PublicKey
from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
from Acquire.ObjectStore import OSPar as _OSPar
from Acquire.ObjectStore import OSParRegistry as _OSParRegistry
from Acquire.ObjectStore import OSParRegistry as _OSParRegistry
from Acquire.ObjectStore import OSPar as _OSPar
from Acquire.Access import get_filesize_and_checksum as _get_filesize_and_checksum
from Acquire.ObjectStore import ObjectStoreError
from Acquire.Client import PARError
from Acquire.Client import PARError
from Acquire.ObjectStore import ObjectStoreError
from Acquire.ObjectStore import ObjectStoreError
from Acquire.Client import PARError
from Acquire.Client import PARError
from Acquire.ObjectStore import ObjectStoreError
from Acquire.ObjectStore import ObjectStoreError


@staticmethod
def create_par(bucket, encrypt_key, key=None, readable=True, writeable=False, duration=3600, cleanup_function=None):
    "Create a pre-authenticated request for the passed bucket and\n           key (if key is None then the request is for the entire bucket).\n           This will return a PAR object that will contain a URL that can\n           be used to access the object/bucket. If writeable is true, then\n           the URL will also allow the object/bucket to be written to.\n           PARs are time-limited. Set the lifetime in seconds by passing\n           in 'duration' (by default this is one hour). Note that you must\n           pass in a public key that will be used to encrypt this PAR. This is\n           necessary as the PAR grants access to anyone who can decrypt\n           the URL\n        "
    from Acquire.Crypto import PublicKey as _PublicKey
    if (not isinstance(encrypt_key, _PublicKey)):
        from Acquire.Client import PARError
        raise PARError('You must supply a valid PublicKey to encrypt the returned PAR')
    if (key is not None):
        if (not _os.path.exists(('%s/%s._data' % (bucket, key)))):
            from Acquire.Client import PARError
            raise PARError(("The object '%s' in bucket '%s' does not exist!" % (key, bucket)))
    elif (not _os.path.exists(bucket)):
        from Acquire.Client import PARError
        raise PARError(("The bucket '%s' does not exist!" % bucket))
    url = ('file://%s' % bucket)
    if key:
        url = ('%s/%s' % (url, key))
    from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
    created_datetime = _get_datetime_now()
    expires_datetime = (created_datetime + _datetime.timedelta(seconds=duration))
    if ((key is None) and readable):
        from Acquire.Client import PARError
        raise PARError('You cannot create a Bucket PAR that has read permissions due to a limitation in the underlying platform')
    from Acquire.ObjectStore import OSPar as _OSPar
    from Acquire.ObjectStore import OSParRegistry as _OSParRegistry
    url_checksum = _OSPar.checksum(url)
    driver_details = {'driver': 'testing_objstore', 'bucket': bucket, 'created_datetime': created_datetime}
    par = _OSPar(url=url, key=key, encrypt_key=encrypt_key, expires_datetime=expires_datetime, is_readable=readable, is_writeable=writeable, driver_details=driver_details)
    _OSParRegistry.register(par=par, url_checksum=url_checksum, details_function=_get_driver_details_from_par, cleanup_function=cleanup_function)
    return par
