from __future__ import absolute_import, division, print_function, with_statement
import copy
from datetime import datetime
import logging
import time
from bson.objectid import ObjectId
from turbo.util import escape as es, camel_to_underscore, basestring_type as basestring, unicode_type
from util import unittest


def test_recursive_to_str(self):
    now = datetime.now()
    objid = ObjectId()
    number = 10
    self.check_value_type(es.to_str(self.record))
    self.check_value_type(es.to_str(self.values))
    self.check_value_type(es.to_str(now))
    self.check_value_type(es.to_str(objid))
    self.check_value_type(es.to_str(number))
