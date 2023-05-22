from __future__ import absolute_import, division, print_function, with_statement
import copy
from datetime import datetime
import logging
import time
from bson.objectid import ObjectId
from turbo.util import escape as es, camel_to_underscore, basestring_type as basestring, unicode_type
from util import unittest


def test_default_encode(self):
    now = datetime.now()
    objid = ObjectId()
    number = 10
    self.assertEqual(es.default_encode(now), time.mktime(now.timetuple()))
    self.assertEqual(es.default_encode(objid), unicode_type(objid))
    self.assertEqual(es.default_encode(number), number)
