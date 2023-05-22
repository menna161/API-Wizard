from __future__ import absolute_import, division, print_function, with_statement
import datetime
import json
from copy import deepcopy
from bson.objectid import ObjectId
from turbo.util import escape, basestring_type
from util import unittest


def test_to_str(self):
    data = {'v1': 10, 'v2': datetime.datetime.now(), 'v3': ObjectId(), 'v4': 'value'}
    self.assertTrue(isinstance(json.dumps(escape.to_str([deepcopy(data) for i in range(10)])), basestring_type))
    self.assertTrue(isinstance(json.dumps(escape.to_str(deepcopy(data))), basestring_type))
