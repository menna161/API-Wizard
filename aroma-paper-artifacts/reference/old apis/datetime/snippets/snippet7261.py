import io as _io
import datetime as _datetime
import uuid as _uuid
import json as _json
import os as _os
import copy as _copy
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
import copy as _copy
from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
import copy as _copy
from Acquire.ObjectStore import ObjectStoreError
from Acquire.Crypto import PublicKey as _PublicKey
from Acquire.ObjectStore import OSPar as _OSPar
from Acquire.ObjectStore import OSParRegistry as _OSParRegistry
from Acquire.ObjectStore import OSParRegistry as _OSParRegistry
from Acquire.ObjectStore import OSPar as _OSPar
import binascii as _binascii
import base64 as _base64
from google.cloud import storage as _storage
from Acquire.ObjectStore import ObjectStoreError
from Acquire.Client import PARError
from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
from Acquire.ObjectStore import ObjectStoreError
from Acquire.ObjectStore import ObjectStoreError
from Acquire.ObjectStore import ObjectStoreError
from Acquire.ObjectStore import ObjectStoreError
from Acquire.ObjectStore import ObjectStoreError
from Acquire.ObjectStore import ObjectStoreError
from Acquire.ObjectStore import ObjectStoreError


@staticmethod
def create_par(bucket, encrypt_key, key=None, readable=True, writeable=False, duration=3600, cleanup_function=None):
    "Create a pre-authenticated request for the passed bucket and\n           key (if key is None then the request is for the entire bucket).\n           This will return a OSPar object that will contain a URL that can\n           be used to access the object/bucket. If writeable is true, then\n           the URL will also allow the object/bucket to be written to.\n           PARs are time-limited. Set the lifetime in seconds by passing\n           in 'duration' (by default this is one hour)\n\n           Args:\n                bucket (dict): Bucket to create OSPar for\n                encrypt_key (PublicKey): Public key to\n                encrypt PAR\n                key (str, default=None): Key\n                readable (bool, default=True): If bucket is readable\n                writeable (bool, default=False): If bucket is writeable\n                duration (int, default=3600): Duration OSPar should be\n                valid for in seconds\n                cleanup_function (function, default=None): Cleanup\n                function to be passed to PARRegistry\n\n           Returns:\n                OSPar: Pre-authenticated request for the bucket\n        "
    from Acquire.Crypto import PublicKey as _PublicKey
    if (not isinstance(encrypt_key, _PublicKey)):
        from Acquire.Client import PARError
        raise PARError('You must supply a valid PublicKey to encrypt the returned OSPar')
    is_bucket = (key is None)
    if writeable:
        method = 'PUT'
    elif readable:
        method = 'GET'
    else:
        from Acquire.ObjectStore import ObjectStoreError
        raise ObjectStoreError('Unsupported permissions model for OSPar!')
    try:
        from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
        created_datetime = _get_datetime_now()
        expires_datetime = (_get_datetime_now() + _datetime.timedelta(seconds=duration))
        bucket_obj = bucket['bucket']
        if is_bucket:
            url = bucket_obj.generate_signed_url(version='v4', expiration=expires_datetime, method=method)
        else:
            blob = bucket_obj.blob(key)
            url = blob.generate_signed_url(version='v4', expiration=expires_datetime, method=method)
    except Exception as e:
        from Acquire.ObjectStore import ObjectStoreError
        raise ObjectStoreError(("Unable to create the OSPar '%s': %s" % (key, str(e))))
    if (url is None):
        from Acquire.ObjectStore import ObjectStoreError
        raise ObjectStoreError('Unable to create the signed URL!')
    from Acquire.ObjectStore import OSPar as _OSPar
    from Acquire.ObjectStore import OSParRegistry as _OSParRegistry
    url_checksum = _OSPar.checksum(url)
    bucket_name = bucket['bucket_name']
    driver_details = {'driver': 'gcp', 'bucket': bucket_name, 'created_datetime': created_datetime}
    par = _OSPar(url=url, encrypt_key=encrypt_key, key=key, expires_datetime=expires_datetime, is_readable=readable, is_writeable=writeable, driver_details=driver_details)
    _OSParRegistry.register(par=par, url_checksum=url_checksum, details_function=_get_driver_details_from_par, cleanup_function=cleanup_function)
    return par
