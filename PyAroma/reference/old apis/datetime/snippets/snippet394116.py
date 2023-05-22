import json
import logging
import os
import random
import time
from datetime import datetime
from typing import Any, Callable, Dict, List, Literal, Optional, Sequence, Tuple, cast
import requests
from rockset.exceptions import BadRequestException, RocksetException
from rockset.models import QueryRequestSql
from rockset.query_paginator import QueryPaginator
from rockset.rockset_client import RocksetClient
from feast.entity import Entity
from feast.feature_view import FeatureView
from feast.infra.online_stores.helpers import compute_entity_id
from feast.infra.online_stores.online_store import OnlineStore
from feast.protos.feast.types.EntityKey_pb2 import EntityKey as EntityKeyProto
from feast.protos.feast.types.Value_pb2 import Value as ValueProto
from feast.repo_config import FeastConfigBaseModel, RepoConfig
from feast.usage import log_exceptions_and_usage


@log_exceptions_and_usage(online_store='rockset')
def online_write_batch(self, config: RepoConfig, table: FeatureView, data: List[Tuple[(EntityKeyProto, Dict[(str, ValueProto)], datetime, Optional[datetime])]], progress: Optional[Callable[([int], Any)]]) -> None:
    '\n        Write a batch of feature rows to online Rockset store.\n\n        Args:\n            config: The RepoConfig for the current FeatureStore.\n            table: Feast FeatureView.\n            data: a list of quadruplets containing Feature data. Each quadruplet contains an Entity Key,\n            a dict containing feature values, an event timestamp for the row, and\n            the created timestamp for the row if it exists.\n            progress: Optional function to be called once every mini-batch of rows is written to\n            the online store. Can be used to display progress.\n        '
    online_config = config.online_store
    assert isinstance(online_config, RocksetOnlineStoreConfig)
    rs = self.get_rockset_client(online_config)
    collection_name = self.get_collection_name(config, table)
    dedup_dict = {}
    for feature_vals in data:
        (entity_key, features, timestamp, created_ts) = feature_vals
        serialized_key = compute_entity_id(entity_key=entity_key, entity_key_serialization_version=config.entity_key_serialization_version)
        if (serialized_key not in dedup_dict):
            dedup_dict[serialized_key] = feature_vals
            continue
        if (timestamp <= dedup_dict[serialized_key][2]):
            continue
        dedup_dict[serialized_key] = feature_vals
    request_batch = []
    for (serialized_key, feature_vals) in dedup_dict.items():
        document = {}
        (entity_key, features, timestamp, created_ts) = feature_vals
        document['_id'] = serialized_key
        document['event_ts'] = timestamp.isoformat()
        document['created_ts'] = ('' if (created_ts is None) else created_ts.isoformat())
        for (k, v) in features.items():
            document[k] = v.SerializeToString().hex()
        request_batch.append(document)
        if progress:
            progress(1)
    resp = rs.Documents.add_documents(collection=collection_name, data=request_batch)
    if online_config.fence_all_writes:
        self.wait_for_fence(rs, collection_name, resp['last_offset'], online_config)
    return None
