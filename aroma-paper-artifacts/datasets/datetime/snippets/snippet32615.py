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


def age(self, now=None):
    "\n        Returns an integer which is the difference in seconds from\n        'now' to when this circuit was created.\n\n        Returns None if there is no created-time.\n        "
    if (not self.time_created):
        return None
    if (now is None):
        now = datetime.utcnow()
    return (now - self.time_created).seconds
