import os
import typing
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import pandas as pd
import pyarrow
from dask import dataframe as dd
from dateutil.tz import tzlocal
from pytz import utc
from feast.constants import FEAST_FS_YAML_FILE_PATH_ENV_NAME
from feast.entity import Entity
from feast.protos.feast.types.EntityKey_pb2 import EntityKey as EntityKeyProto
from feast.protos.feast.types.Value_pb2 import Value as ValueProto
from feast.type_map import python_values_to_proto_values
from feast.value_type import ValueType
from feast.feature_view import FeatureView
from feast.on_demand_feature_view import OnDemandFeatureView
from feast.feature_view import DUMMY_ENTITY_ID


def to_naive_utc(ts: datetime) -> datetime:
    if (ts.tzinfo is None):
        return ts
    else:
        return ts.astimezone(utc).replace(tzinfo=None)
