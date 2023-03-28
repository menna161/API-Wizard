from copy import copy as _copy
from Acquire.Service import Service as _Service
from Acquire.Service import Service as _Service
from Acquire.Service import ServiceError
from Acquire.Client import Wallet as _Wallet


def last_key_update(self):
    'Return the datetime when the key and certificate of this\n           service were last updated\n        '
    self._fail()
    return None
