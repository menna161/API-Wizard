from enum import Enum as _Enum
from Acquire.Crypto import Hash as _Hash
from Acquire.Service import is_running_service as _is_running_service
from Acquire.Client import PrivateKey as _PrivateKey
from Acquire.ObjectStore import create_uid as _create_uid
from Acquire.Client import Wallet as _Wallet
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.Client import Authorisation as _Authorisation
from Acquire.Crypto import PrivateKey as _PrivateKey
from Acquire.ObjectStore import bytes_to_string as _bytes_to_string
import json as _json
import json as _json
from Acquire.Client import PrivateKey as _PrivateKey
from Acquire.Client import PublicKey as _PublicKey
from Acquire.Service import ServiceError
from Acquire.Service import get_this_service as _get_this_service
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.ObjectStore import string_to_bytes as _string_to_bytes
from Acquire.Crypto import DecryptionError
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.Compute import ComputeJob as _ComputeJob
from Acquire.Compute import ComputeJob as _ComputeJob
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.ObjectStore import get_datetime_now_to_string as _get_datetime_now_to_string
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.Service import get_this_service as _get_this_service
from Acquire.Crypto import DecryptionError
from Acquire.Crypto import DecryptionError
from Acquire.ObjectStore import get_datetime_now_to_string as _get_datetime_now_to_string


def submit_job(self, uid):
    'Submit the job with specified UID to this cluster.\n\n           On the service this will put the UID of the job into the\n           "pending" pool, and will signal the cluster to pull that job\n\n           On the client this will pull the job with that UID from the\n           pending pool, moving it to the "submitting" pool and will\n           pass this job to the cluster submission system\n        '
    if Cluster._is_running_service():
        from Acquire.ObjectStore import ObjectStore as _ObjectStore
        from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
        from Acquire.ObjectStore import get_datetime_now_to_string as _get_datetime_now_to_string
        bucket = _get_service_account_bucket()
        key = ('compute/pending/%s' % uid)
        resource = {'pending': _get_datetime_now_to_string(), 'uid': uid}
        _ObjectStore.set_object_from_json(bucket, key, resource)
    else:
        return self.get_job(uid=uid, start_state='pending', end_state='submitting')
