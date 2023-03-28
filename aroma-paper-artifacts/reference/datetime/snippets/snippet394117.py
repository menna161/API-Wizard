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
def online_read(self, config: RepoConfig, table: FeatureView, entity_keys: List[EntityKeyProto], requested_features: Optional[List[str]]=None) -> List[Tuple[(Optional[datetime], Optional[Dict[(str, ValueProto)]])]]:
    '\n        Retrieve feature values from the online Rockset store.\n\n        Args:\n            config: The RepoConfig for the current FeatureStore.\n            table: Feast FeatureView.\n            entity_keys: a list of entity keys that should be read from the FeatureStore.\n        '
    online_config = config.online_store
    assert isinstance(online_config, RocksetOnlineStoreConfig)
    rs = self.get_rockset_client(online_config)
    collection_name = self.get_collection_name(config, table)
    feature_list = ''
    if (requested_features is not None):
        feature_list = ','.join(requested_features)
    entity_serialized_key_list = [compute_entity_id(k, entity_key_serialization_version=config.entity_key_serialization_version) for k in entity_keys]
    entity_query_str = ','.join(("'{id}'".format(id=s) for s in entity_serialized_key_list))
    query_str = f'''
            SELECT
                "_id",
                "event_ts",
                {feature_list}
            FROM
                {collection_name}
            WHERE
                "_id" IN ({entity_query_str})
        '''
    feature_set = set()
    if requested_features:
        feature_set.update(requested_features)
    result_map = {}
    for page in QueryPaginator(rs, rs.Queries.query(sql=QueryRequestSql(query=query_str, paginate=True, initial_paginate_response_doc_count=online_config.read_pagination_batch_size))):
        for doc in page:
            result = {}
            for (k, v) in doc.items():
                if (k not in feature_set):
                    continue
                val = ValueProto()
                val.ParseFromString(bytes.fromhex(v))
                result[k] = val
            result_map[doc['_id']] = (datetime.fromisoformat(doc['event_ts']), result)
    results_list: List[Tuple[(Optional[datetime], Optional[Dict[(str, ValueProto)]])]] = []
    for key in entity_serialized_key_list:
        if (key not in result_map):
            results_list.append((None, None))
            continue
        results_list.append(result_map[key])
    return results_list
