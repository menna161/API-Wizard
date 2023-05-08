import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, KeysView, List, Optional, Set, Tuple
import numpy as np
import pandas as pd
import pyarrow as pa
from jinja2 import BaseLoader, Environment
from pandas import Timestamp
from feast.data_source import DataSource
from feast.errors import EntityTimestampInferenceException, FeastEntityDFMissingColumnsError
from feast.feature_view import FeatureView
from feast.importer import import_class
from feast.infra.offline_stores.offline_store import OfflineStore
from feast.infra.registry.base_registry import BaseRegistry
from feast.repo_config import RepoConfig
from feast.type_map import feast_value_type_to_pa
from feast.utils import _get_requested_feature_views_to_features_dict, to_naive_utc


def get_feature_view_query_context(feature_refs: List[str], feature_views: List[FeatureView], registry: BaseRegistry, project: str, entity_df_timestamp_range: Tuple[(datetime, datetime)]) -> List[FeatureViewQueryContext]:
    '\n    Build a query context containing all information required to template a BigQuery and\n    Redshift point-in-time SQL query\n    '
    (feature_views_to_feature_map, on_demand_feature_views_to_features) = _get_requested_feature_views_to_features_dict(feature_refs, feature_views, registry.list_on_demand_feature_views(project))
    query_context = []
    for (feature_view, features) in feature_views_to_feature_map.items():
        join_keys: List[str] = []
        entity_selections: List[str] = []
        for entity_column in feature_view.entity_columns:
            join_key = feature_view.projection.join_key_map.get(entity_column.name, entity_column.name)
            join_keys.append(join_key)
            entity_selections.append(f'{entity_column.name} AS {join_key}')
        if isinstance(feature_view.ttl, timedelta):
            ttl_seconds = int(feature_view.ttl.total_seconds())
        else:
            ttl_seconds = 0
        reverse_field_mapping = {v: k for (k, v) in feature_view.batch_source.field_mapping.items()}
        features = [reverse_field_mapping.get(feature, feature) for feature in features]
        timestamp_field = reverse_field_mapping.get(feature_view.batch_source.timestamp_field, feature_view.batch_source.timestamp_field)
        created_timestamp_column = reverse_field_mapping.get(feature_view.batch_source.created_timestamp_column, feature_view.batch_source.created_timestamp_column)
        date_partition_column = reverse_field_mapping.get(feature_view.batch_source.date_partition_column, feature_view.batch_source.date_partition_column)
        max_event_timestamp = to_naive_utc(entity_df_timestamp_range[1]).isoformat()
        min_event_timestamp = None
        if feature_view.ttl:
            min_event_timestamp = to_naive_utc((entity_df_timestamp_range[0] - feature_view.ttl)).isoformat()
        context = FeatureViewQueryContext(name=feature_view.projection.name_to_use(), ttl=ttl_seconds, entities=join_keys, features=features, field_mapping=feature_view.batch_source.field_mapping, timestamp_field=timestamp_field, created_timestamp_column=created_timestamp_column, table_subquery=feature_view.batch_source.get_table_query_string(), entity_selections=entity_selections, min_event_timestamp=min_event_timestamp, max_event_timestamp=max_event_timestamp, date_partition_column=date_partition_column)
        query_context.append(context)
    return query_context
