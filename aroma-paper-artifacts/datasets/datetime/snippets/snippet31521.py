import datetime
from twisted.trial import unittest
from twisted.internet import task
from twisted.internet.interfaces import IReactorTime
from zope.interface import implementer
from txtorcon.addrmap import AddrMap
from txtorcon.interface import IAddrListener


def test_parse(self):
    "\n        Make sure it's parsing things properly.\n        "
    now = (datetime.datetime.now() + datetime.timedelta(seconds=10))
    nowutc = (datetime.datetime.utcnow() + datetime.timedelta(seconds=10))
    line = ('www.example.com 72.30.2.43 "%s" EXPIRES="%s" FOO=bar BAR=baz' % (now.strftime(self.fmt), nowutc.strftime(self.fmt)))
    am = AddrMap()
    am.update(line)
    addr = am.find('www.example.com')
    self.assertTrue(((addr.ip == '72.30.2.43') or (addr.ip.exploded == '72.30.2.43')))
    self.assertEqual(addr.expires.ctime(), nowutc.ctime())
    line = ('www.example.com 72.30.2.43 "%s" "%s"' % (now.strftime(self.fmt), nowutc.strftime(self.fmt)))
    am.update(line)
    self.assertEqual(addr.expires.ctime(), nowutc.ctime())
    am.scheduler.getDelayedCalls()[0].cancel()
