from avrogen import avrojson
from avrogen import logical
from avro import schema
import unittest
import six
import datetime
from avrogen.dict_wrapper import DictWrapper


def test_logical_type(self):
    writers_schema = make_avsc_object({'type': 'record', 'name': 'test_record', 'fields': [{'name': 'field1', 'type': 'int'}, {'name': 'field2', 'type': 'string'}, {'name': 'date1', 'type': {'type': 'int', 'logicalType': 'date'}}]})
    readers_schema = make_avsc_object({'type': 'record', 'name': 'test_record', 'fields': [{'name': 'field1', 'type': 'int'}, {'name': 'field2', 'type': 'string'}, {'name': 'field3', 'type': 'double', 'default': 3.0}, {'name': 'date1', 'type': {'type': 'int', 'logicalType': 'date'}}, {'name': 'date2', 'type': {'type': 'int', 'logicalType': 'date'}, 'default': 42}]})
    input = dict(field1=2, field2='3', date1=datetime.date(2012, 3, 4))
    output1 = dict(field1=2, field2='3', date1=datetime.date(2012, 3, 4))
    output2 = dict(field1=2, field2='3', field3=3.0, date1=datetime.date(2012, 3, 4), date2=datetime.date(1970, 2, 12))
    self.assertDictEqual(self.converter_lt.from_json_object(self.converter_lt.to_json_object(input, writers_schema), writers_schema, writers_schema), output1)
    self.assertDictEqual(self.converter_lt.from_json_object(self.converter_lt.to_json_object(input, writers_schema), writers_schema, readers_schema), output2)
