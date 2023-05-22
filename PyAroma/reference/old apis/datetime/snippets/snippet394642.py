import datetime
import itertools
import os
import time
import unittest
from datetime import timedelta
from typing import Any, Dict, List, Tuple, Union
import assertpy
import numpy as np
import pandas as pd
import pytest
import requests
from botocore.exceptions import BotoCoreError
from feast.entity import Entity
from feast.errors import FeatureNameCollisionError, RequestDataNotFoundInEntityRowsException
from feast.feature_service import FeatureService
from feast.feature_view import FeatureView
from feast.field import Field
from feast.online_response import TIMESTAMP_POSTFIX
from feast.types import Float32, Int32, String
from feast.wait import wait_retry_backoff
from tests.integration.feature_repos.repo_configuration import Environment, construct_universal_feature_views
from tests.integration.feature_repos.universal.entities import customer, driver, location
from tests.integration.feature_repos.universal.feature_views import create_driver_hourly_stats_feature_view, driver_feature_view
from tests.utils.data_source_test_creator import prep_file_source


@pytest.mark.integration
def test_online_retrieval_with_shared_batch_source(environment, universal_data_sources):
    fs = environment.feature_store
    (entities, datasets, data_sources) = universal_data_sources
    driver_entity = driver()
    driver_stats_v1 = FeatureView(name='driver_stats_v1', entities=[driver_entity], schema=[Field(name='avg_daily_trips', dtype=Int32)], source=data_sources.driver)
    driver_stats_v2 = FeatureView(name='driver_stats_v2', entities=[driver_entity], schema=[Field(name='avg_daily_trips', dtype=Int32), Field(name='conv_rate', dtype=Float32)], source=data_sources.driver)
    fs.apply([driver_entity, driver_stats_v1, driver_stats_v2])
    data = pd.DataFrame({'driver_id': [1, 2], 'avg_daily_trips': [4, 5], 'conv_rate': [0.5, 0.3], 'event_timestamp': [pd.to_datetime(1646263500, utc=True, unit='s'), pd.to_datetime(1646263600, utc=True, unit='s')], 'created': [pd.to_datetime(1646263500, unit='s'), pd.to_datetime(1646263600, unit='s')]})
    fs.write_to_online_store('driver_stats_v1', data.drop('conv_rate', axis=1))
    fs.write_to_online_store('driver_stats_v2', data)
    with pytest.raises(KeyError):
        fs.get_online_features(features=['driver_stats_v1:conv_rate'], entity_rows=[{'driver_id': 1}, {'driver_id': 2}])
