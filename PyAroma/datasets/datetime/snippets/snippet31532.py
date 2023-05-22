import datetime
from twisted.trial import unittest
from twisted.internet import task
from twisted.internet.interfaces import IReactorTime
from zope.interface import implementer
from txtorcon.addrmap import AddrMap
from txtorcon.interface import IAddrListener


def test_listeners(self):
    self.expires = []
    self.addrmap = []
    clock = task.Clock()
    am = AddrMap()
    am.scheduler = IReactorTime(clock)
    am.add_listener(self)
    now = (datetime.datetime.now() + datetime.timedelta(seconds=10))
    nowutc = (datetime.datetime.utcnow() + datetime.timedelta(seconds=10))
    line = ('www.example.com 72.30.2.43 "%s" EXPIRES="%s"' % (now.strftime(self.fmt), nowutc.strftime(self.fmt)))
    am.update(line)
    a = am.find('www.example.com')
    self.assertEqual(self.addrmap, [a])
    clock.advance(10)
    self.assertEqual(self.expires, ['www.example.com'])
