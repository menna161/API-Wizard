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


def add_admin_user(service, account_uid, authorisation=None):
    'Function that is called to add a new user account as a service\n       administrator. If this is the first account then authorisation\n       is not needed. If this is the second or subsequent admin account,\n       then you need to provide an authorisation signed by one of the\n       existing admin users. If you need to reset the admin users then\n       delete the user accounts from the service.\n    '
    assert_running_service()
    from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
    from Acquire.ObjectStore import Mutex as _Mutex
    from Acquire.ObjectStore import ObjectStore as _ObjectStore
    from Acquire.ObjectStore import get_datetime_now_to_string as _get_datetime_now_to_string
    bucket = _get_service_account_bucket()
    admin_key = ('%s/admin_users' % _service_key)
    mutex = _Mutex(key=admin_key, bucket=bucket)
    try:
        admin_users = _ObjectStore.get_object_from_json(bucket, admin_key)
    except:
        admin_users = None
    if (admin_users is None):
        admin_users = {}
        authorised_by = 'first admin'
    else:
        if (authorisation is None):
            from Acquire.Service import ServiceAccountError
            raise ServiceAccountError('You must supply a valid authorisation from an existing admin user if you want to add a new admin user.')
        if (authorisation.user_uid() not in admin_users):
            from Acquire.Service import ServiceAccountError
            raise ServiceAccountError('The authorisation for the new admin account is not valid because the user who signed it is not a valid admin on this service.')
        authorisation.verify(account_uid)
        authorised_by = authorisation.user_uid()
    admin_users[account_uid] = {'datetime': _get_datetime_now_to_string(), 'authorised_by': authorised_by}
    _ObjectStore.set_object_from_json(bucket, admin_key, _json.dumps(admin_users))
    mutex.unlock()
    _cache_adminusers.clear()
