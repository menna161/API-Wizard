from datetime import datetime
import boto3
from feast import utils
from feast.infra.online_stores.helpers import compute_entity_id
from feast.protos.feast.types.EntityKey_pb2 import EntityKey as EntityKeyProto
from feast.protos.feast.types.Value_pb2 import Value as ValueProto


def create_n_customer_test_samples(n=10):
    return [(EntityKeyProto(join_keys=['customer'], entity_values=[ValueProto(string_val=str(i))]), {'avg_orders_day': ValueProto(float_val=1.0), 'name': ValueProto(string_val='John'), 'age': ValueProto(int64_val=3)}, datetime.utcnow(), None) for i in range(n)]
