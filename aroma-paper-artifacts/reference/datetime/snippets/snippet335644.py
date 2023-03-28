import datetime
import os
import random
import string
import time
import unittest
from google.appengine.ext import db
from mapreduce import control
from mapreduce import hooks
from mapreduce import model
from mapreduce import test_support
from testlib import testutil
from mapreduce.api import map_job


def testStartMap_Eta(self):
    'Test that MR can be scheduled into the future.\n\n    Most of start_map functionality is already tested by handlers_test.\n    Just a smoke test is enough.\n    '
    TestEntity().put()
    eta = (datetime.datetime.utcnow() + datetime.timedelta(hours=1))
    shard_count = 4
    mapreduce_id = control.start_map('test_map', (__name__ + '.test_handler'), 'mapreduce.input_readers.DatastoreInputReader', {'entity_kind': ((__name__ + '.') + TestEntity.__name__)}, shard_count, mapreduce_parameters={'foo': 'bar'}, base_path='/mapreduce_base_path', queue_name=self.QUEUE_NAME, eta=eta)
    task_eta = self.validate_map_started(mapreduce_id)
    self.assertEquals(eta.strftime('%Y/%m/%d %H:%M:%S'), task_eta)
