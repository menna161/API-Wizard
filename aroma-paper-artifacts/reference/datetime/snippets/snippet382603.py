import os
import unittest
import avrogen
import sys
import importlib
import shutil
from avro import io
from avro import datafile, schema
import tempfile
import avrogen.schema
import avrogen.protocol
import logging
import sys
import datetime
import six
import decimal
import datetime
import pytz
import tzlocal
from twitter_schema.com.bifflabs.grok.model.twitter.avro import AvroTweet, AvroTweetMetadata
from twitter_schema.com.bifflabs.grok.model.common.avro import AvroPoint, AvroDateTime, AvroKnowableOptionString, AvroKnowableListString, AvroKnowableBoolean, AvroKnowableOptionPoint
from twitter_schema import SpecificDatumReader


@unittest.skip
def test_defaults(self):
    schema_json = self.read_schema('record_with_default_nested.json')
    avrogen.schema.write_schema_files(schema_json, self.output_dir, use_logical_types=True)
    (root_module, schema_classes) = self.load_gen(self.test_name)
    self.assertTrue(hasattr(root_module, 'sample_recordClass'))
    record = root_module.sample_recordClass()
    self.assertEquals(record.withDefault.field1, 42)
    self.assertEquals(record.nullableWithDefault.field1, 42)
    self.assertEquals(record.nullableRecordWithLogicalType.field1, datetime.date(1970, 2, 12))
    self.assertEquals(record.nullableWithLogicalType, datetime.date(1970, 2, 12))
    self.assertEquals(record.multiNullable, 42)
