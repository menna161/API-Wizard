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
def get(par_uid, details_function, url_checksum=None):
    "Return the PAR that matches the passed PAR_UID.\n           If 'url_checksum' is supplied then this verifies that\n           the checksum of the secret URL is correct.\n\n           This returns the PAR with a completed 'driver_details'.\n           The 'driver_details' is created from the dictionary\n           of data saved with the PAR. The signature should be;\n\n           driver_details = details_function(data)\n        "
    if ((par_uid is None) or (len(par_uid) == 0)):
        return
    from Acquire.Service import is_running_service as _is_running_service
    if (not _is_running_service()):
        return
    from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
    from Acquire.ObjectStore import OSPar as _OSPar
    from Acquire.ObjectStore import ObjectStore as _ObjectStore
    from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
    key = ('%s/uid/%s' % (_registry_key, par_uid))
    bucket = _get_service_account_bucket()
    objs = _ObjectStore.get_all_objects_from_json(bucket=bucket, prefix=key)
    data = None
    for obj in objs.values():
        if (url_checksum is not None):
            if (url_checksum == obj['url_checksum']):
                data = obj
                break
        else:
            data = obj
            break
    if (data is None):
        from Acquire.ObjectStore import ObjectStoreError
        raise ObjectStoreError('There is matching PAR available to close...')
    par = _OSPar.from_data(data['par'])
    if ('driver_details' in data):
        if (details_function is not None):
            driver_details = details_function(data['driver_details'])
            par._driver_details = driver_details
        else:
            par._driver_details = driver_details
    return par
