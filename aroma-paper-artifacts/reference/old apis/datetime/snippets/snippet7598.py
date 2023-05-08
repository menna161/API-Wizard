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
def register(par, url_checksum, details_function, cleanup_function=None):
    "Register the passed PAR, passing in the checksum of\n           the PAR's secret URL (so we can verify the close),\n           and optionally supplying a cleanup_function that is\n           called when the PAR is closed. The passed 'details_function'\n           should be used to extract the object-store driver-specific\n           details from the PAR and convert them into a dictionary.\n           The signature should be;\n\n           driver_details = details_function(par)\n        "
    from Acquire.Service import is_running_service as _is_running_service
    if (not _is_running_service()):
        return
    from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
    from Acquire.ObjectStore import OSPar as _OSPar
    from Acquire.ObjectStore import ObjectStore as _ObjectStore
    from Acquire.ObjectStore import Function as _Function
    from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
    if (par is None):
        return
    if (not isinstance(par, _OSPar)):
        raise TypeError('You can only register pars of type PAR')
    if par.is_null():
        return
    data = {}
    data['par'] = par.to_data()
    if (details_function is None):
        data['driver_details'] = par._driver_details
    else:
        data['driver_details'] = details_function(par)
    data['url_checksum'] = url_checksum
    if (cleanup_function is not None):
        if (not isinstance(cleanup_function, _Function)):
            cleanup_function = _Function(cleanup_function)
        data['cleanup_function'] = cleanup_function.to_data()
    expire_string = _datetime_to_string(par.expires_when())
    key = ('%s/uid/%s/%s' % (_registry_key, par.uid(), expire_string))
    bucket = _get_service_account_bucket()
    _ObjectStore.set_object_from_json(bucket, key, data)
    key = ('%s/expire/%s/%s' % (_registry_key, expire_string, par.uid()))
    _ObjectStore.set_object_from_json(bucket, key, par.uid())
