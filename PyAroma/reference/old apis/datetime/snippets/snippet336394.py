import datetime
import os
import types
import unittest
import urlparse
from google.appengine.ext import db
from google.appengine.ext import testbed
from mapreduce import hooks
from mapreduce import model
from google.appengine.ext.webapp import mock_webapp


def testCopyFrom(self):
    'Test copy_from method.'
    state = model.ShardState.create_new('my-map-job1', 14)
    state.active = False
    state.counters_map.increment('foo', 2)
    state.result_status = 'failed'
    state.mapreduce_id = 'mapreduce_id'
    state.update_time = datetime.datetime.now()
    state.shard_description = 'shard_description'
    state.last_work_item = 'last_work_item'
    another_state = model.ShardState.create_new('my-map-job1', 14)
    another_state.copy_from(state)
    self.assertEquals(state.active, another_state.active)
    self.assertEquals(state.counters_map, another_state.counters_map)
    self.assertEquals(state.result_status, another_state.result_status)
    self.assertEquals(state.mapreduce_id, another_state.mapreduce_id)
    self.assertEquals(state.update_time, another_state.update_time)
    self.assertEquals(state.shard_description, another_state.shard_description)
    self.assertEquals(state.last_work_item, another_state.last_work_item)
