from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import with_statement
from txtorcon.interface import IAddrListener
from txtorcon.util import maybe_ip_addr
from twisted.internet.interfaces import IReactorTime
from twisted.internet import reactor
import datetime
import shlex


def update(self, *args):
    '\n        deals with an update from Tor; see parsing logic in torcontroller\n        '
    gmtexpires = None
    (name, ip, expires) = args[:3]
    for arg in args:
        if arg.lower().startswith('expires='):
            gmtexpires = arg[8:]
    if (gmtexpires is None):
        if (len(args) == 3):
            gmtexpires = expires
        elif (args[2] == 'NEVER'):
            gmtexpires = args[2]
        else:
            gmtexpires = args[3]
    self.name = name
    self.ip = maybe_ip_addr(ip)
    if (self.ip == '<error>'):
        self._expire()
        return
    fmt = '%Y-%m-%d %H:%M:%S'
    oldexpires = self.expires
    if (gmtexpires.upper() == 'NEVER'):
        self.expires = None
    else:
        self.expires = datetime.datetime.strptime(gmtexpires, fmt)
    self.created = datetime.datetime.utcnow()
    if (self.expires is not None):
        if (oldexpires is None):
            if (self.expires <= self.created):
                diff = datetime.timedelta(seconds=0)
            else:
                diff = (self.expires - self.created)
            self.expiry = self.map.scheduler.callLater(diff.seconds, self._expire)
        else:
            diff = (self.expires - oldexpires)
            self.expiry.delay(diff.seconds)
