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


def _write_rows_concurrently(self, config: RepoConfig, project: str, table: FeatureView, rows: Iterable[Tuple[(str, bytes, str, datetime)]]):
    session: Session = self._get_session(config)
    keyspace: str = self._keyspace
    fqtable = CassandraOnlineStore._fq_table_name(keyspace, project, table)
    insert_cql = self._get_cql_statement(config, 'insert4', fqtable=fqtable)
    execute_concurrent_with_args(session, insert_cql, rows, concurrency=config.online_store.write_concurrency)
