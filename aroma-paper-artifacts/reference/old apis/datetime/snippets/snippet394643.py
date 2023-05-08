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
@pytest.mark.parametrize('full_feature_names', [True, False], ids=(lambda v: str(v)))
def test_online_retrieval_with_event_timestamps(environment, universal_data_sources, full_feature_names):
    fs = environment.feature_store
    (entities, datasets, data_sources) = universal_data_sources
    feature_views = construct_universal_feature_views(data_sources)
    fs.apply([driver(), feature_views.driver, feature_views.global_fv])
    data = {'driver_id': [1, 2], 'conv_rate': [0.5, 0.3], 'acc_rate': [0.6, 0.4], 'avg_daily_trips': [4, 5], 'event_timestamp': [pd.to_datetime(1646263500, utc=True, unit='s'), pd.to_datetime(1646263600, utc=True, unit='s')], 'created': [pd.to_datetime(1646263500, unit='s'), pd.to_datetime(1646263600, unit='s')]}
    df_ingest = pd.DataFrame(data)
    fs.write_to_online_store('driver_stats', df_ingest)
    response = fs.get_online_features(features=['driver_stats:avg_daily_trips', 'driver_stats:acc_rate', 'driver_stats:conv_rate'], entity_rows=[{'driver_id': 1}, {'driver_id': 2}])
    df = response.to_df(True)
    assertpy.assert_that(len(df)).is_equal_to(2)
    assertpy.assert_that(df['driver_id'].iloc[0]).is_equal_to(1)
    assertpy.assert_that(df['driver_id'].iloc[1]).is_equal_to(2)
    assertpy.assert_that(df[('avg_daily_trips' + TIMESTAMP_POSTFIX)].iloc[0]).is_equal_to(1646263500)
    assertpy.assert_that(df[('avg_daily_trips' + TIMESTAMP_POSTFIX)].iloc[1]).is_equal_to(1646263600)
    assertpy.assert_that(df[('acc_rate' + TIMESTAMP_POSTFIX)].iloc[0]).is_equal_to(1646263500)
    assertpy.assert_that(df[('acc_rate' + TIMESTAMP_POSTFIX)].iloc[1]).is_equal_to(1646263600)
    assertpy.assert_that(df[('conv_rate' + TIMESTAMP_POSTFIX)].iloc[0]).is_equal_to(1646263500)
    assertpy.assert_that(df[('conv_rate' + TIMESTAMP_POSTFIX)].iloc[1]).is_equal_to(1646263600)
