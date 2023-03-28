from copy import copy as _copy
from Acquire.Service import Service as _Service
from Acquire.Service import Service as _Service
from Acquire.Service import ServiceError
from Acquire.Client import Wallet as _Wallet


def dump_keys(self):
    'Return a dump of the current key and certificate, so that\n           we can keep a record of all keys that have been used. The\n           returned json-serialisable dictionary contains the keys,\n           their fingerprints, and the datetime when they were\n           generated. If this is run on the service, then the keys\n           are encrypted the password which is encrypted using the\n           master key\n        '
    self._fail()
    return None
