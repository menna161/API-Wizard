import numpy as np
from feast.type_map import feast_value_type_to_python_type, python_values_to_proto_values
from feast.value_type import ValueType


def test_null_unix_timestamp_list():
    'Test that UnixTimestamp lists with a null get converted from proto\n    correctly.'
    data = np.array([['NaT']], dtype='datetime64')
    protos = python_values_to_proto_values(data, ValueType.UNIX_TIMESTAMP_LIST)
    converted = feast_value_type_to_python_type(protos[0])
    assert (converted[0] is None)
