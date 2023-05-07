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


def test_many_pickle(self):
    s = 'spam '
    S = (s * 99)
    b = b'\xdd'
    f = 1.23
    d = datetime.date(2017, 1, 2)
    di = dict(n=None, t=True, f=False, l=[], l1=[1])
    t = datetime.datetime(2017, 1, 2, 4, 5, 6)
    tup = (s, S, b, f, d, di, t, 9, 99, (1 << 30), (1 << 60), (1 << 90))
    lst = list(tup)
    lst.append(tup)
    data = dict(l1=lst, l2=lst)
    got = JsonUnpickler(pickle.dumps(data, self.proto)).load(sort_keys=True, indent=2).replace(' \n', '\n')
    self.assertEqual(test_many_pickle_expect, got)
