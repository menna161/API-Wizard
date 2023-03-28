import datetime
import unittest
import pipeline
from google.appengine.ext import db
from mapreduce import context
from mapreduce import errors
from mapreduce import input_readers
from mapreduce import mapper_pipeline
from mapreduce import model
from mapreduce import test_support
from testlib import testutil


def testEmptyMapper(self):
    'Test empty mapper over empty dataset.'
    p = mapper_pipeline.MapperPipeline('empty_map', handler_spec=(__name__ + '.test_empty_handler'), input_reader_spec=(input_readers.__name__ + '.DatastoreInputReader'), params={'input_reader': {'entity_kind': (__name__ + '.TestEntity'), 'filters': [('dt', '=', datetime.datetime(2000, 1, 1))]}})
    p.start()
    test_support.execute_until_empty(self.taskqueue)
    self.assertEquals(1, len(self.emails))
    self.assertTrue(self.emails[0][1].startswith('Pipeline successful:'))
    p = mapper_pipeline.MapperPipeline.from_id(p.pipeline_id)
    counters = p.outputs.counters.value
    self.assertTrue(counters)
    self.assertTrue((context.COUNTER_MAPPER_WALLTIME_MS in counters))
    self.assertEqual([], p.outputs.default.value)
    self.assertTrue(p.outputs.job_id.filled)
    state = model.MapreduceState.get_by_job_id(p.outputs.job_id.value)
    self.assertEqual(model.MapreduceState.RESULT_SUCCESS, state.result_status)
    self.assertEqual(model.MapreduceState.RESULT_SUCCESS, p.outputs.result_status.value)
