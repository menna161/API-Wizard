import logging
import multiprocessing
import os
import random
from datetime import datetime, timedelta
from multiprocessing import Process
from sys import platform
from typing import Any, Dict, List, Tuple
import pandas as pd
import pytest
from _pytest.nodes import Item
from feast.feature_store import FeatureStore
from feast.wait import wait_retry_backoff
from tests.data.data_creator import create_basic_driver_dataset
from tests.integration.feature_repos.integration_test_repo_config import IntegrationTestRepoConfig
from tests.integration.feature_repos.repo_configuration import AVAILABLE_OFFLINE_STORES, AVAILABLE_ONLINE_STORES, OFFLINE_STORE_TO_PROVIDER_CONFIG, Environment, TestData, construct_test_environment, construct_universal_feature_views, construct_universal_test_data
from tests.integration.feature_repos.universal.data_sources.file import FileDataSourceCreator
from tests.integration.feature_repos.universal.entities import customer, driver, location
from tests.utils.http_server import check_port_open, free_port


@pytest.fixture
def simple_dataset_1() -> pd.DataFrame:
    now = datetime.utcnow()
    ts = pd.Timestamp(now).round('ms')
    data = {'id_join_key': [1, 2, 1, 3, 3], 'float_col': [0.1, 0.2, 0.3, 4, 5], 'int64_col': [1, 2, 3, 4, 5], 'string_col': ['a', 'b', 'c', 'd', 'e'], 'ts_1': [ts, (ts - timedelta(hours=4)), (ts - timedelta(hours=3)), (ts - timedelta(hours=2)), (ts - timedelta(hours=1))]}
    return pd.DataFrame.from_dict(data)
