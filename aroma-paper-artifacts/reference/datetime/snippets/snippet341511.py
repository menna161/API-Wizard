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


def test_insert(self):
    _id = self.tb_tag.insert({'value': 0})
    self.assertIsNot(_id, None)
    record = {'list': [{'key': ObjectId(), 'key2': 'test', 'key3': ObjectId()}, 10, 12, 13, ['name', 'name', 'name', ObjectId(), ObjectId()], datetime.datetime.now()], 'imgid': ObjectId(), 'up': {'key1': ObjectId(), 'key2': ObjectId(), 'key3': ObjectId()}}
    result = self.tb_tag.insert(record)
    self.assertIsInstance(result, ObjectId)
    _id = self.tb_tag.insert({'_id': fake_ids_2[0]})
    self.assertEqual(_id, fake_ids_2[0])
    result = self.tb_tag.find_by_id(fake_ids_2[0])
    self.assertEqual(result['value'], 0)
    with self.assertRaises(Exception):
        result = self.tb_tag.insert({'nokey': 10})
    _id = self.tb_tag.insert({'imgid': None})
    self.assertIsNot(_id, None)
    result = self.tb_tag.find_by_id(_id)
    self.assertEqual(result['value'], 0)
    self.tb_tag.remove_by_id(_id)
    docs = [{'_id': i} for i in fake_ids_2[1:]]
    result = self.tb_tag.insert(docs)
    self.assertEqual(1, len(result))
    for i in result:
        self.assertIn(i, fake_ids_2)
    result = self.tb_tag.find_by_id(fake_ids_2[1:])
    self.assertEqual(1, len(result))
    for i in result:
        self.assertEqual(i['value'], 0)
