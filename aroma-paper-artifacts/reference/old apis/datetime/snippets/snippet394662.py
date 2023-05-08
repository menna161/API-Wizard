import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
import pyarrow as pa
import pytest
from feast.infra.offline_stores.offline_store import RetrievalJob
from feast.types import Array, Bool, FeastType, Float32, Float64, Int32, Int64, String, UnixTimestamp
from tests.data.data_creator import create_basic_driver_dataset
from tests.integration.feature_repos.universal.entities import driver
from tests.integration.feature_repos.universal.feature_views import driver_feature_view


def populate_test_configs(offline: bool):
    feature_dtypes = ['int32', 'int64', 'float', 'bool', 'datetime']
    configs: List[TypeTestConfig] = []
    for feature_dtype in feature_dtypes:
        for feature_is_list in [True, False]:
            for has_empty_list in [True, False]:
                if ((feature_is_list is False) and (has_empty_list is True)):
                    continue
                configs.append(TypeTestConfig(feature_dtype=feature_dtype, feature_is_list=feature_is_list, has_empty_list=has_empty_list))
    return configs
