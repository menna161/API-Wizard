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


def _get_driver_details_from_data(data):
    'Internal function used to get the GCP driver details from the\n       passed data\n\n       Args:\n            data (dict): Dict holding GCP driver details\n       Returns:\n            dict: Dict holding GCP driver details\n    '
    from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
    import copy as _copy
    details = _copy.copy(data)
    if ('created_datetime' in details):
        details['created_datetime'] = _string_to_datetime(details['created_datetime'])
    return details
