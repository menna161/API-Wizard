from google.appengine.tools import os_compat
import datetime
import unittest
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore
from mapreduce import errors
from testlib import testutil
from mapreduce.api import map_job
from mapreduce.api.map_job import datastore_input_reader_base_test
from mapreduce.api.map_job import datastore_input_reader


def testValidate_Filters(self):
    'Tests validating filters parameter.'
    params = {'entity_kind': self.entity_kind, 'filters': [('a', '=', 1), ('b', '=', 2)]}
    new = datetime.datetime.now()
    old = new.replace(year=(new.year - 1))
    conf = map_job.JobConfig(job_name=self.TEST_JOB_NAME, mapper=map_job.Mapper, input_reader_cls=self.reader_cls, input_reader_params=params, shard_count=1)
    conf.input_reader_cls.validate(conf)
    params['filters'] = [['datetime_property', '>', old], ['datetime_property', '<=', new], ['a', '=', 1]]
    self.assertRaises(errors.BadReaderParamsError, conf.input_reader_cls.validate, conf)
