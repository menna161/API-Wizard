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
def online_read(self, config: RepoConfig, table: FeatureView, entity_keys: List[EntityKeyProto], requested_features: Optional[List[str]]=None) -> List[Tuple[(Optional[datetime], Optional[Dict[(str, ValueProto)]])]]:
    conn = self._get_conn(config)
    cur = conn.cursor()
    result: List[Tuple[(Optional[datetime], Optional[Dict[(str, ValueProto)]])]] = []
    with tracing_span(name='remote_call'):
        cur.execute(f"SELECT entity_key, feature_name, value, event_ts FROM {_table_id(config.project, table)} WHERE entity_key IN ({','.join(('?' * len(entity_keys)))}) ORDER BY entity_key", [serialize_entity_key(entity_key, entity_key_serialization_version=config.entity_key_serialization_version) for entity_key in entity_keys])
        rows = cur.fetchall()
    rows = {k: list(group) for (k, group) in itertools.groupby(rows, key=(lambda r: r[0]))}
    for entity_key in entity_keys:
        entity_key_bin = serialize_entity_key(entity_key, entity_key_serialization_version=config.entity_key_serialization_version)
        res = {}
        res_ts = None
        for (_, feature_name, val_bin, ts) in rows.get(entity_key_bin, []):
            val = ValueProto()
            val.ParseFromString(val_bin)
            res[feature_name] = val
            res_ts = ts
        if (not res):
            result.append((None, None))
        else:
            result.append((res_ts, res))
    return result
