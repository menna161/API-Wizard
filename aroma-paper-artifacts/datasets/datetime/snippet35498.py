from six.moves import copyreg
import datetime
import json
import persistent
from persistent.mapping import PersistentMapping
import pickle
from pprint import pprint
from six import BytesIO, PY3
import textwrap
import unittest
import ZODB
from ZODB.utils import z64, p64, maxtid
from ..jsonpickle import JsonUnpickler, dumps
import decimal
import pickletools
from zope.testing.loggingsupport import InstalledHandler
from ..jsonpickle import Jsonifier
from BTrees.OOBTree import BTree
from ..jsonpickle import Jsonifier


def test_basics(self):
    root = self.root
    root.numbers = (0, 123456789, (1 << 70), 1234.56789)
    root.time = datetime.datetime(2001, 2, 3, 4, 5, 6, 7)
    root.date = datetime.datetime(2001, 2, 3)
    root.delta = datetime.timedelta(1, 2, 3)
    root.name = u'root'
    root.data = b'\xff'
    root.list = [1, 2, 3, root.name, root.numbers]
    root.first = PersistentMapping()
    p = self.commit()
    self.check({'::': 'global', 'name': 'persistent.mapping.PersistentMapping'})
    self.assertEqual(p[(self.unpickler.pos - 1):self.unpickler.pos], b'.')
    self.check({u'data': {u'data': {u'::': u'hex', u'hex': u'ff'}, u'date': u'2001-02-03T00:00:00', u'delta': {u'::': u'datetime.timedelta', u'::()': [1, 2, 3]}, u'first': {u'::': u'persistent', u'::=>': 1, u'id': [1, u'persistent.mapping.PersistentMapping']}, u'list': [1, 2, 3, u'root', [0, 123456789, 1180591620717411303424, 1234.56789]], u'name': u'root', u'numbers': [0, 123456789, 1180591620717411303424, 1234.56789], u'time': u'2001-02-03T04:05:06.000007'}})
