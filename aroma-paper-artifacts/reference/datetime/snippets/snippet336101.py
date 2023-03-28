import datetime
import unittest
from google.appengine.api import datastore_errors
from google.appengine.ext import db
from mapreduce import json_util


def testE2e(self):
    now = datetime.datetime.now()
    obj = {'a': 1, 'b': [{'c': 'd'}], 'e': now}
    new_obj = json_util.json.loads(json_util.json.dumps(obj, cls=json_util.JsonEncoder), cls=json_util.JsonDecoder)
    self.assertEquals(obj, new_obj)
