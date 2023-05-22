import itertools
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple
from pydantic import StrictStr
from pydantic.schema import Literal
from feast import Entity
from feast.feature_view import FeatureView
from feast.infra.infra_object import SQLITE_INFRA_OBJECT_CLASS_TYPE, InfraObject
from feast.infra.key_encoding_utils import serialize_entity_key
from feast.infra.online_stores.online_store import OnlineStore
from feast.protos.feast.core.InfraObject_pb2 import InfraObject as InfraObjectProto
from feast.protos.feast.core.Registry_pb2 import Registry as RegistryProto
from feast.protos.feast.core.SqliteTable_pb2 import SqliteTable as SqliteTableProto
from feast.protos.feast.types.EntityKey_pb2 import EntityKey as EntityKeyProto
from feast.protos.feast.types.Value_pb2 import Value as ValueProto
from feast.repo_config import FeastConfigBaseModel, RepoConfig
from feast.usage import log_exceptions_and_usage, tracing_span
from feast.utils import to_naive_utc


@log_exceptions_and_usage(online_store='sqlite')
def online_write_batch(self, config: RepoConfig, table: FeatureView, data: List[Tuple[(EntityKeyProto, Dict[(str, ValueProto)], datetime, Optional[datetime])]], progress: Optional[Callable[([int], Any)]]) -> None:
    conn = self._get_conn(config)
    project = config.project
    with conn:
        for (entity_key, values, timestamp, created_ts) in data:
            entity_key_bin = serialize_entity_key(entity_key, entity_key_serialization_version=config.entity_key_serialization_version)
            timestamp = to_naive_utc(timestamp)
            if (created_ts is not None):
                created_ts = to_naive_utc(created_ts)
            for (feature_name, val) in values.items():
                conn.execute(f'''
                            UPDATE {_table_id(project, table)}
                            SET value = ?, event_ts = ?, created_ts = ?
                            WHERE (entity_key = ? AND feature_name = ?)
                        ''', (val.SerializeToString(), timestamp, created_ts, entity_key_bin, feature_name))
                conn.execute(f'''INSERT OR IGNORE INTO {_table_id(project, table)}
                            (entity_key, feature_name, value, event_ts, created_ts)
                            VALUES (?, ?, ?, ?, ?)''', (entity_key_bin, feature_name, val.SerializeToString(), timestamp, created_ts))
            if progress:
                progress(1)
