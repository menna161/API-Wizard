from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import with_statement
import six
import time
from datetime import datetime
from twisted.python.failure import Failure
from twisted.python import log
from twisted.internet import defer
from twisted.internet.interfaces import IStreamClientEndpoint
from zope.interface import implementer
from .interface import IRouterContainer, IStreamAttacher
from txtorcon.util import find_keywords, maybe_ip_addr, SingleObserver
from txtorcon import web
from .endpoints import TorClientEndpoint


@property
def time_created(self):
    if (self._time_created is not None):
        return self._time_created
    if ('TIME_CREATED' in self.flags):
        t = self.flags['TIME_CREATED'].split('.')[0]
        tstruct = time.strptime(t, TIME_FORMAT)
        self._time_created = datetime(*tstruct[:7])
    return self._time_created
