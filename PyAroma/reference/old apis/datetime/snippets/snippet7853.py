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


def _get_driver_details_from_data(data):
    from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
    import copy as _copy
    details = _copy.copy(data)
    if ('created_datetime' in details):
        details['created_datetime'] = _string_to_datetime(details['created_datetime'])
    return details
