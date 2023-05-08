import os as _os
import json as _json
from cachetools import cached as _cached
from cachetools import LRUCache as _LRUCache
from Acquire.Service import ServiceAccountError
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.ObjectStore import Mutex as _Mutex
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.Service import Service as _Service
from Acquire.Client import Credentials as _Credentials
from Acquire.Identity import UserAccount as _UserAccount
from Acquire.Service import clear_service_cache as _clear_service_cache
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.ObjectStore import Mutex as _Mutex
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.ObjectStore import get_datetime_now_to_string as _get_datetime_now_to_string
from Acquire.Service import ServiceAccountError
from Acquire.Service import Service as _Service
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.ObjectStore import Mutex as _Mutex
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.Service import MissingServiceAccountError
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.Crypto import KeyManipulationError
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.Service import Service as _Service
from Acquire.ObjectStore import Mutex as _Mutex
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.Service import get_service_account_bucket
from ._errors import ServiceError
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.Service import MissingServiceAccountError
from Acquire.Service import ServiceAccountError
from Acquire.Registry import register_service as _register_service
from Acquire.Service import ServiceAccountError
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.Service import MissingServiceAccountError
from Acquire.Service import Service as _Service
from Acquire.Service import ServiceAccountError
from Acquire.Client import create_account as _create_account
from Acquire.Client import deposit as _deposit
from Acquire.Service import MissingServiceAccountError
from Acquire.Service import ServiceAccountError
from Acquire.Service import ServiceAccountError
from Acquire.Service import ServiceAccountError
from Acquire.Service import ServiceAccountError
from Acquire.Service import MissingServiceAccountError
from Acquire.Service import exception_to_string
from Acquire.Service import ServiceAccountError
from Acquire.Service import ServiceAccountError
from Acquire.Service import ServiceAccountError
from Acquire.Service import ServiceAccountError
from Acquire.Service import ServiceAccountMissingKeyError
from Acquire.Service import ServiceAccountError


def _refresh_this_service_keys_and_certs(service_info, service_password):
    from Acquire.Service import Service as _Service
    service = _Service.from_data(service_info, service_password)
    if (service._uid == 'STAGE1'):
        return service_info
    if (not service.should_refresh_keys()):
        return service_info
    oldkeys = service.dump_keys(include_old_keys=False)
    from Acquire.ObjectStore import ObjectStore as _ObjectStore
    from Acquire.ObjectStore import Mutex as _Mutex
    from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
    bucket = _get_service_account_bucket()
    key = ('%s/oldkeys/%s' % (_service_key, oldkeys['datetime']))
    _ObjectStore.set_object_from_json(bucket, key, oldkeys)
    for fingerprint in oldkeys.keys():
        if (fingerprint not in ['datetime', 'encrypted_passphrase']):
            _ObjectStore.set_string_object(bucket, ('%s/oldkeys/fingerprints/%s' % (_service_key, fingerprint)), key)
    last_update = service.last_key_update()
    service.refresh_keys()
    m = _Mutex(key=service.uid(), bucket=bucket)
    service_data = _ObjectStore.get_object_from_json(bucket, _service_key)
    service_info = _Service.from_data(service_data)
    if (service_info.last_key_update() == last_update):
        _ObjectStore.set_object_from_json(bucket, _service_key, service.to_data(service_password))
    m.unlock()
    return service_data
