import datetime
from twisted.trial import unittest
from twisted.internet import task
from twisted.internet.interfaces import IReactorTime
from zope.interface import implementer
from txtorcon.addrmap import AddrMap
from txtorcon.interface import IAddrListener


def test_expires_with_update(self):
    '\n        This test updates the expiry time and checks that we properly\n        delay our expiry callback.\n        '
    clock = task.Clock()
    am = AddrMap()
    am.scheduler = IReactorTime(clock)
    now = (datetime.datetime.now() + datetime.timedelta(seconds=10))
    nowutc = (datetime.datetime.utcnow() + datetime.timedelta(seconds=10))
    line = ('www.example.com 72.30.2.43 "%s" EXPIRES="%s"' % (now.strftime(self.fmt), nowutc.strftime(self.fmt)))
    am.update(line)
    self.assertTrue(am.find('www.example.com'))
    now = (datetime.datetime.now() + datetime.timedelta(seconds=20))
    nowutc = (datetime.datetime.utcnow() + datetime.timedelta(seconds=20))
    line = ('www.example.com 72.30.2.43 "%s" EXPIRES="%s"' % (now.strftime(self.fmt), nowutc.strftime(self.fmt)))
    am.update(line)
    self.assertTrue(('www.example.com' in am.addr))
    clock.advance(10)
    self.assertTrue(('www.example.com' in am.addr))
    clock.advance(10)
    self.assertTrue(('www.example.com' not in am.addr))
