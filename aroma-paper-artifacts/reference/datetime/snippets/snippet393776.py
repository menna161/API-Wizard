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


def infer_event_timestamp_from_entity_df(entity_schema: Dict[(str, np.dtype)]) -> str:
    if (DEFAULT_ENTITY_DF_EVENT_TIMESTAMP_COL in entity_schema.keys()):
        return DEFAULT_ENTITY_DF_EVENT_TIMESTAMP_COL
    datetime_columns = [column for (column, dtype) in entity_schema.items() if pd.core.dtypes.common.is_datetime64_any_dtype(dtype)]
    if (len(datetime_columns) == 1):
        print(f'Using {datetime_columns[0]} as the event timestamp. To specify a column explicitly, please name it {DEFAULT_ENTITY_DF_EVENT_TIMESTAMP_COL}.')
        return datetime_columns[0]
    else:
        raise EntityTimestampInferenceException(DEFAULT_ENTITY_DF_EVENT_TIMESTAMP_COL)
