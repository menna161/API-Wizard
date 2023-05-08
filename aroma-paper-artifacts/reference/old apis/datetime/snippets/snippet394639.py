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
@pytest.mark.universal_online_stores
def test_write_to_online_store(environment, universal_data_sources):
    fs = environment.feature_store
    (entities, datasets, data_sources) = universal_data_sources
    driver_hourly_stats = create_driver_hourly_stats_feature_view(data_sources.driver)
    driver_entity = driver()
    fs.apply([driver_hourly_stats, driver_entity])
    data = {'driver_id': [123], 'conv_rate': [0.85], 'acc_rate': [0.91], 'avg_daily_trips': [14], 'event_timestamp': [pd.Timestamp(datetime.datetime.utcnow()).round('ms')], 'created': [pd.Timestamp(datetime.datetime.utcnow()).round('ms')]}
    df_data = pd.DataFrame(data)
    fs.write_to_online_store('driver_stats', df_data)
    df = fs.get_online_features(features=['driver_stats:avg_daily_trips', 'driver_stats:acc_rate', 'driver_stats:conv_rate'], entity_rows=[{'driver_id': 123}]).to_df()
    assertpy.assert_that(df['avg_daily_trips'].iloc[0]).is_equal_to(14)
    assertpy.assert_that(df['acc_rate'].iloc[0]).is_close_to(0.91, 1e-06)
    assertpy.assert_that(df['conv_rate'].iloc[0]).is_close_to(0.85, 1e-06)
