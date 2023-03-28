import io as _io
import datetime as _datetime
import uuid as _uuid
import json as _json
import os as _os
import copy as _copy
import uuid as _uuid
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
import copy as _copy
from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
import copy as _copy
from Acquire.ObjectStore import ObjectStoreError
from Acquire.Crypto import PublicKey as _PublicKey
from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
from Acquire.ObjectStore import OSPar as _OSPar
from Acquire.ObjectStore import OSParRegistry as _OSParRegistry
from Acquire.ObjectStore import OSParRegistry as _OSParRegistry
from Acquire.ObjectStore import OSPar as _OSPar
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
import binascii as _binascii
import base64 as _base64
from oci.object_storage.models import CreateBucketDetails as _CreateBucketDetails
from oci.object_storage.models import CreateBucketDetails as _CreateBucketDetails
from Acquire.ObjectStore import ObjectStoreError
from Acquire.ObjectStore import ObjectStoreError
from Acquire.Client import PARError
from Acquire.Client import PARError
from oci.object_storage.models import CreatePreauthenticatedRequestDetails as _CreatePreauthenticatedRequestDetails
from Acquire.ObjectStore import ObjectStoreError
from Acquire.ObjectStore import ObjectStoreError
from Acquire.ObjectStore import ObjectStoreError
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
    from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
    expires_datetime = (_get_datetime_now() + _datetime.timedelta(seconds=duration))
    is_bucket = (key is None)
    if (is_bucket and readable):
        from Acquire.Client import PARError
        raise PARError('You cannot create a Bucket OSPar that has read permissions due to a limitation in the underlying platform')
    try:
        from oci.object_storage.models import CreatePreauthenticatedRequestDetails as _CreatePreauthenticatedRequestDetails
    except:
        raise ImportError("Cannot import OCI. Please install OCI, e.g. via 'pip install oci' so that you can connect to the Oracle Cloud Infrastructure")
    oci_par = None
    request = _CreatePreauthenticatedRequestDetails()
    if is_bucket:
        request.access_type = 'AnyObjectWrite'
    elif (readable and writeable):
        request.access_type = 'ObjectReadWrite'
    elif readable:
        request.access_type = 'ObjectRead'
    elif writeable:
        request.access_type = 'ObjectWrite'
    else:
        from Acquire.ObjectStore import ObjectStoreError
        raise ObjectStoreError('Unsupported permissions model for OSPar!')
    request.name = str(_uuid.uuid4())
    if (not is_bucket):
        request.object_name = _clean_key(key)
    request.time_expires = expires_datetime
    client = bucket['client']
    try:
        response = client.create_preauthenticated_request(client.get_namespace().data, bucket['bucket_name'], request)
    except Exception as e:
        from Acquire.ObjectStore import ObjectStoreError
        raise ObjectStoreError(("Unable to create the OSPar '%s': %s" % (str(request), str(e))))
    if (response.status != 200):
        from Acquire.ObjectStore import ObjectStoreError
        raise ObjectStoreError(("Unable to create the OSPar '%s': Status %s, Error %s" % (str(request), response.status, str(response.data))))
    oci_par = response.data
    if (oci_par is None):
        from Acquire.ObjectStore import ObjectStoreError
        raise ObjectStoreError('Unable to create the preauthenticated request!')
    created_datetime = oci_par.time_created.replace(tzinfo=_datetime.timezone.utc)
    expires_datetime = oci_par.time_expires.replace(tzinfo=_datetime.timezone.utc)
    url = _get_object_url_for_region(bucket['region'], oci_par.access_uri)
    from Acquire.ObjectStore import OSPar as _OSPar
    from Acquire.ObjectStore import OSParRegistry as _OSParRegistry
    url_checksum = _OSPar.checksum(url)
    driver_details = {'driver': 'oci', 'bucket': bucket['bucket_name'], 'created_datetime': created_datetime, 'par_id': oci_par.id, 'par_name': oci_par.name}
    par = _OSPar(url=url, encrypt_key=encrypt_key, key=oci_par.object_name, expires_datetime=expires_datetime, is_readable=readable, is_writeable=writeable, driver_details=driver_details)
    _OSParRegistry.register(par=par, url_checksum=url_checksum, details_function=_get_driver_details_from_par, cleanup_function=cleanup_function)
    return par
