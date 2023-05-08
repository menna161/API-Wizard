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


def get_job(self, uid, start_state='pending', end_state=None, passphrase=None):
    "Return the job with specified 'uid' in the specified\n           state (start_state) - this will move the job to\n           'end_state' if this is specified. If you are on the\n           service you need to supply a valid passphrase\n        "
    if (end_state is None):
        resource = ('get_job %s %s' % (uid, start_state))
    else:
        resource = ('get_job %s %s->%s' % (uid, start_state, end_state))
    if Cluster._is_running_service():
        self.verify_passphrase(resource=resource, passphrase=passphrase)
        start_state = JobState(start_state)
        if (end_state is not None):
            end_state = JobState(end_state)
        from Acquire.ObjectStore import ObjectStore as _ObjectStore
        from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
        bucket = _get_service_account_bucket()
        key = ('compute/%s/%s' % (start_state.value, uid))
        if ((end_state is None) or (end_state == start_state)):
            try:
                data = _ObjectStore.get_object_from_json(bucket=bucket, key=key)
            except:
                data = None
        else:
            from Acquire.ObjectStore import get_datetime_now_to_string as _get_datetime_now_to_string
            try:
                data = _ObjectStore.take_object_from_json(bucket=bucket, key=key)
                data[end_state.value] = _get_datetime_now_to_string()
                key = ('compute/%s/%s' % (end_state.value, uid))
                _ObjectStore.set_object_from_json(bucket=bucket, key=key, data=data)
            except:
                data = None
        if (data is None):
            raise KeyError(('There is no job with UID %s in state %s' % (uid, start_state.value)))
        if (uid != data['uid']):
            raise ValueError(('The job info for UID %s is corrupt? %s' % (uid, data)))
        from Acquire.Compute import ComputeJob as _ComputeJob
        return _ComputeJob.load(uid=uid)
    else:
        passphrase = self.passphrase(resource)
        args = {'uid': str(uid), 'passphrase': passphrase, 'start_state': str(start_state)}
        if (end_state is not None):
            args['end_state'] = str(end_state)
        result = self.compute_service().call_function(function='get_job', args=args)
        from Acquire.Compute import ComputeJob as _ComputeJob
        return _ComputeJob.from_data(self.decrypt_data(result['job']))
