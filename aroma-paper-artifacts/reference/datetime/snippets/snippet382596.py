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


@unittest.skip("don't care about logical types")
def test_logical(self):
    schema_json = self.read_schema('logical_types.json')
    avrogen.schema.write_schema_files(schema_json, self.output_dir, use_logical_types=True)
    root_module = importlib.import_module(self.test_name)
    importlib.import_module('.schema_classes', self.test_name)
    self.assertTrue(hasattr(root_module, 'LogicalTypesTest'))
    LogicalTypesTest = root_module.LogicalTypesTest
    instance = LogicalTypesTest()
    import decimal
    import datetime
    import pytz
    import tzlocal
    self.assertIsInstance(instance.decimalField, decimal.Decimal)
    self.assertIsInstance(instance.decimalFieldWithDefault, decimal.Decimal)
    self.assertIsInstance(instance.dateField, datetime.date)
    self.assertIsInstance(instance.dateFieldWithDefault, datetime.date)
    self.assertIsInstance(instance.timeMillisField, datetime.time)
    self.assertIsInstance(instance.timeMillisFieldWithDefault, datetime.time)
    self.assertIsInstance(instance.timeMicrosField, datetime.time)
    self.assertIsInstance(instance.timeMicrosFieldWithDefault, datetime.time)
    self.assertIsInstance(instance.timestampMillisField, datetime.datetime)
    self.assertIsInstance(instance.timestampMillisFieldWithDefault, datetime.datetime)
    self.assertIsInstance(instance.timestampMicrosField, datetime.datetime)
    self.assertIsInstance(instance.timestampMicrosFieldWithDefault, datetime.datetime)
    self.assertEquals(instance.decimalFieldWithDefault, decimal.Decimal(10))
    self.assertEquals(instance.dateFieldWithDefault, datetime.date(1970, 2, 12))
    self.assertEquals(instance.timeMillisFieldWithDefault, datetime.time(second=42))
    self.assertEquals(instance.timeMicrosFieldWithDefault, datetime.time(second=42))
    self.assertEquals(tzlocal.get_localzone().localize(instance.timestampMicrosFieldWithDefault).astimezone(pytz.UTC), datetime.datetime(1970, 1, 1, 0, 0, 42, tzinfo=pytz.UTC))
    self.assertEquals(tzlocal.get_localzone().localize(instance.timestampMillisFieldWithDefault).astimezone(pytz.UTC), datetime.datetime(1970, 1, 1, 0, 0, 42, tzinfo=pytz.UTC))
