from Acquire.Service import is_running_service as _is_running_service
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.ObjectStore import OSPar as _OSPar
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.ObjectStore import Function as _Function
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
from Acquire.Service import is_running_service as _is_running_service
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.ObjectStore import OSPar as _OSPar
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
from Acquire.Service import is_running_service as _is_running_service
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.ObjectStore import OSPar as _OSPar
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
from Acquire.ObjectStore import Function as _Function
from Acquire.ObjectStore import ObjectStoreError


@staticmethod
def close(par):
    'Close the passed PAR. This will remove the registration\n           for the PAR and will also call the associated\n           cleanup_function (if any)\n        '
    from Acquire.Service import is_running_service as _is_running_service
    if (not _is_running_service()):
        return
    from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
    from Acquire.ObjectStore import OSPar as _OSPar
    from Acquire.ObjectStore import ObjectStore as _ObjectStore
    from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
    from Acquire.ObjectStore import Function as _Function
    if (par is None):
        return
    if (not isinstance(par, _OSPar)):
        raise TypeError('You can only close OSPar objects!')
    if par.is_null():
        return
    expire_string = _datetime_to_string(par.expires_when())
    bucket = _get_service_account_bucket()
    key = ('%s/expire/%s/%s' % (_registry_key, expire_string, par.uid()))
    try:
        _ObjectStore.delete_object(bucket=bucket, key=key)
    except:
        pass
    key = ('%s/uid/%s/%s' % (_registry_key, par.uid(), expire_string))
    try:
        data = _ObjectStore.take_object_from_json(bucket=bucket, key=key)
    except:
        data = None
    if (data is None):
        return
    if ('cleanup_function' in data):
        cleanup_function = _Function.from_data(data['cleanup_function'])
        cleanup_function(par=par)
