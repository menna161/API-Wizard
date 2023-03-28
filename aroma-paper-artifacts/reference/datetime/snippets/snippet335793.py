import datetime
import logging
import random
import string
import unittest
from google.appengine.ext import db
from google.appengine.ext import ndb
from mapreduce import context
from mapreduce import control
from mapreduce import handlers
from mapreduce import input_readers
from mapreduce import model
from mapreduce import output_writers
from mapreduce import parameters
from mapreduce import records
from mapreduce import test_support
from mapreduce.tools import gcs_file_seg_reader
from testlib import testutil
import cloudstorage
from cloudstorage import storage_api


def testEntityQuery(self):
    entity_count = 1000
    for i in range(entity_count):
        TestEntity(int_property=(i % 5)).put()
    control.start_map('test_map', (__name__ + '.TestHandler'), (input_readers.__name__ + '.DatastoreInputReader'), {'entity_kind': ((__name__ + '.') + TestEntity.__name__), 'filters': [('int_property', '=', 3), ('dt', '=', datetime.datetime(2000, 1, 1))]}, shard_count=4, base_path='/mapreduce_base_path')
    test_support.execute_until_empty(self.taskqueue)
    self.assertEquals(200, len(TestHandler.processed_entites))
