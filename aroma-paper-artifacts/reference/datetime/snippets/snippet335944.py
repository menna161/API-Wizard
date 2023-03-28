from google.appengine.tools import os_compat
import cStringIO
import datetime
import math
import os
import random
import string
import time
import unittest
import zipfile
import mox
from google.appengine.ext import ndb
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore
from google.appengine.api import datastore_file_stub
from google.appengine.api import datastore_types
from google.appengine.api import logservice
from google.appengine.api import namespace_manager
from google.appengine.api.blobstore import blobstore_stub
from google.appengine.api.blobstore import dict_blob_storage
from google.appengine.api.logservice import log_service_pb
from google.appengine.api.logservice import logservice_stub
from google.appengine.datastore import datastore_stub_util
from google.appengine.ext import blobstore
from google.appengine.ext import key_range
from google.appengine.ext import testbed
from google.appengine.ext.blobstore import blobstore as blobstore_internal
from mapreduce import context
from mapreduce import errors
from mapreduce import input_readers
from mapreduce import kv_pb
from mapreduce import model
from mapreduce import namespace_range
from mapreduce import records
from testlib import testutil
import cloudstorage


def testValidate_Filters(self):
    'Tests validating filters parameter.'
    params = {'entity_kind': self.entity_kind, 'filters': [('a', '=', 1), ('b', '=', 2)]}
    new = datetime.datetime.now()
    old = new.replace(year=(new.year - 1))
    mapper_spec = model.MapperSpec('FooHandler', 'DatastoreInputReader', params, 1)
    self.reader_cls.validate(mapper_spec)
    params['filters'] = [['a', '>', 1], ['a', '<', 2]]
    self.reader_cls.validate(mapper_spec)
    params['filters'] = [['datetime_property', '>', old], ['datetime_property', '<=', new], ['a', '=', 1]]
    self.reader_cls.validate(mapper_spec)
    params['filters'] = [['a', '=', 1]]
    self.reader_cls.validate(mapper_spec)
    params['filters'] = [('c', '=', 1)]
    self.assertRaises(input_readers.BadReaderParamsError, self.reader_cls.validate, mapper_spec)
    params['filters'] = [('a', '<=', 1)]
    self.assertRaises(input_readers.BadReaderParamsError, self.reader_cls.validate, mapper_spec)
    params['filters'] = [['datetime_property', '>', 1], ['datetime_property', '<=', datetime.datetime.now()]]
    self.assertRaises(input_readers.BadReaderParamsError, self.reader_cls.validate, mapper_spec)
    params['filters'] = [['datetime_property', '>', new], ['datetime_property', '<=', old]]
    self.assertRaises(input_readers.BadReaderParamsError, self.reader_cls.validate, mapper_spec)
