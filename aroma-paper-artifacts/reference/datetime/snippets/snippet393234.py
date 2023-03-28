import logging
from datetime import datetime
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import EXEC_PROFILE_DEFAULT, Cluster, ExecutionProfile, ResultSet, Session
from cassandra.concurrent import execute_concurrent_with_args
from cassandra.policies import DCAwareRoundRobinPolicy, TokenAwarePolicy
from cassandra.query import PreparedStatement
from pydantic import StrictFloat, StrictInt, StrictStr
from pydantic.typing import Literal
from feast import Entity, FeatureView, RepoConfig
from feast.infra.key_encoding_utils import serialize_entity_key
from feast.infra.online_stores.online_store import OnlineStore
from feast.protos.feast.types.EntityKey_pb2 import EntityKey as EntityKeyProto
from feast.protos.feast.types.Value_pb2 import Value as ValueProto
from feast.repo_config import FeastConfigBaseModel
from feast.usage import log_exceptions_and_usage, tracing_span


@log_exceptions_and_usage(online_store='cassandra')
def online_read(self, config: RepoConfig, table: FeatureView, entity_keys: List[EntityKeyProto], requested_features: Optional[List[str]]=None) -> List[Tuple[(Optional[datetime], Optional[Dict[(str, ValueProto)]])]]:
    '\n        Read feature values pertaining to the requested entities from\n        the online store.\n\n        Args:\n            config: The RepoConfig for the current FeatureStore.\n            table: Feast FeatureView.\n            entity_keys: a list of entity keys that should be read\n                         from the FeatureStore.\n        '
    project = config.project
    result: List[Tuple[(Optional[datetime], Optional[Dict[(str, ValueProto)]])]] = []
    entity_key_bins = [serialize_entity_key(entity_key, entity_key_serialization_version=config.entity_key_serialization_version).hex() for entity_key in entity_keys]
    with tracing_span(name='remote_call'):
        feature_rows_sequence = self._read_rows_by_entity_keys(config, project, table, entity_key_bins, columns=['feature_name', 'value', 'event_ts'])
    for (entity_key_bin, feature_rows) in zip(entity_key_bins, feature_rows_sequence):
        res = {}
        res_ts = None
        if feature_rows:
            for feature_row in feature_rows:
                if ((requested_features is None) or (feature_row.feature_name in requested_features)):
                    val = ValueProto()
                    val.ParseFromString(feature_row.value)
                    res[feature_row.feature_name] = val
                    res_ts = feature_row.event_ts
        if (not res):
            result.append((None, None))
        else:
            result.append((res_ts, res))
    return result
