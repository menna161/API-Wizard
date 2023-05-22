from __future__ import absolute_import, division, print_function, with_statement
import copy
from datetime import datetime
import logging
import time
from bson.objectid import ObjectId
from turbo.util import escape as es, camel_to_underscore, basestring_type as basestring, unicode_type
from util import unittest


def setUp(self):
    child = {'id': ObjectId(), 'atime': datetime.now(), 'number': 10, 'name': 'hello world', 'mail': None}
    self.record = {'id': ObjectId(), 'atime': datetime.now(), 'number': 10, 'name': 'hello world', 'child': child, 'childs': [copy.deepcopy(child) for i in range(3)]}
    self.values = [copy.deepcopy(self.record) for i in range(3)]
