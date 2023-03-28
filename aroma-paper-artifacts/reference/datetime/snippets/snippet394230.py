import sys
from binascii import unhexlify
import pandas
from _snowflake import vectorized
from feast.infra.key_encoding_utils import serialize_entity_key
from feast.protos.feast.types.EntityKey_pb2 import EntityKey as EntityKeyProto
from feast.protos.feast.types.Value_pb2 import Value as ValueProto
from feast.type_map import _convert_value_type_str_to_value_type, python_values_to_proto_values
from feast.value_type import ValueType


@vectorized(input=pandas.DataFrame)
def feast_snowflake_timestamp_to_unix_timestamp_proto(df):
    sys._xoptions['snowflake_partner_attribution'].append('feast')
    df = list(map(ValueProto.SerializeToString, python_values_to_proto_values(pandas.to_datetime(df[0], unit='ns').to_numpy(), ValueType.UNIX_TIMESTAMP)))
    return df
