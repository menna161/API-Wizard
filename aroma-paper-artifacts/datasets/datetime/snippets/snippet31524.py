import datetime
from twisted.trial import unittest
from twisted.internet import task
from twisted.internet.interfaces import IReactorTime
from zope.interface import implementer
from txtorcon.addrmap import AddrMap
from txtorcon.interface import IAddrListener


def test_expires_old(self):
    '\n        Test something that expires before "now"\n        '
    clock = task.Clock()
    am = AddrMap()
    am.scheduler = IReactorTime(clock)
    now = (datetime.datetime.now() + datetime.timedelta(seconds=(- 10)))
    nowutc = (datetime.datetime.utcnow() + datetime.timedelta(seconds=(- 10)))
    line = ('www.example.com 72.30.2.43 "%s" EXPIRES="%s"' % (now.strftime(self.fmt), nowutc.strftime(self.fmt)))
    am.update(line)
    self.assertTrue(('www.example.com' in am.addr))
    clock.advance(0)
    self.assertTrue(('www.example.com' not in am.addr))
