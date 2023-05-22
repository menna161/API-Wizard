from __future__ import absolute_import, division, print_function, with_statement
import datetime
import json
from bson.objectid import ObjectId
import gridfs
from pymongo import MongoClient
from turbo.model import BaseModel
from turbo.util import PY3, basestring_type as basestring, utf8
from util import unittest, fake_ids, fake_ids_2
from io import StringIO
from cStringIO import StringIO


def test_default_encode(self):
    self.assertTrue(isinstance(self.tb_tag.default_encode(ObjectId()), basestring))
    self.assertTrue(isinstance(self.tb_tag.default_encode(datetime.datetime.now()), float))
    self.assertEqual(self.tb_tag.default_encode('string'), 'string')
