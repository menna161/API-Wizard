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


def test_dt_with_tz(self):
    data = datetime.datetime(1, 2, 3, 4, 5, 6, 7, TZ())
    got = JsonUnpickler(pickle.dumps(data, self.proto)).load(sort_keys=True)
    self.assertEqual('{"::": "datetime", "tz": {"::": "newt.db.tests.testjsonpickle.TZ"}, "value": "0001-02-03T04:05:06.000007"}', got)
