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
def online_write_batch(self, config: RepoConfig, table: FeatureView, data: List[Tuple[(EntityKeyProto, Dict[(str, ValueProto)], datetime, Optional[datetime])]], progress: Optional[Callable[([int], Any)]]) -> None:
    '\n        Write a batch of features of several entities to the database.\n\n        Args:\n            config: The RepoConfig for the current FeatureStore.\n            table: Feast FeatureView.\n            data: a list of quadruplets containing Feature data. Each\n                  quadruplet contains an Entity Key, a dict containing feature\n                  values, an event timestamp for the row, and\n                  the created timestamp for the row if it exists.\n            progress: Optional function to be called once every mini-batch of\n                      rows is written to the online store. Can be used to\n                      display progress.\n        '
    project = config.project

    def unroll_insertion_tuples() -> Iterable[Tuple[(str, bytes, str, datetime)]]:
        '\n            We craft an iterable over all rows to be inserted (entities->features),\n            but this way we can call `progress` after each entity is done.\n            '
        for (entity_key, values, timestamp, created_ts) in data:
            entity_key_bin = serialize_entity_key(entity_key, entity_key_serialization_version=config.entity_key_serialization_version).hex()
            for (feature_name, val) in values.items():
                params: Tuple[(str, bytes, str, datetime)] = (feature_name, val.SerializeToString(), entity_key_bin, timestamp)
                (yield params)
            if progress:
                progress(1)
    with tracing_span(name='remote_call'):
        self._write_rows_concurrently(config, project, table, unroll_insertion_tuples())
        if progress:
            progress(1)
