from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import with_statement
import json
from datetime import datetime
from .util import NetLocation
from .util import _Version
import six
from base64 import b64encode, b64decode
from binascii import b2a_hex, a2b_hex
from twisted.internet.defer import inlineCallbacks, returnValue, succeed
from twisted.python.deprecate import deprecated
from twisted.web.client import readBody


@property
def modified(self):
    "\n        This is the time of 'the publication time of its most recent\n        descriptor' (in UTC).\n\n        See also dir-spec.txt.\n\n        "
    if (self._modified is None):
        self._modified = datetime.strptime(self._modified_unparsed, '%Y-%m-%d %H:%M:%S')
    return self._modified
