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
@pytest.mark.universal_online_stores(only=['redis'])
def test_write_to_online_store_event_check(environment):
    if (os.getenv('FEAST_IS_LOCAL_TEST', 'False') == 'True'):
        return
    fs = environment.feature_store
    now = pd.Timestamp(datetime.datetime.utcnow()).round('ms')
    hour_ago = pd.Timestamp((datetime.datetime.utcnow() - timedelta(hours=1))).round('ms')
    latest = pd.Timestamp((datetime.datetime.utcnow() + timedelta(seconds=1))).round('ms')
    data = {'id': [123, 567, 890], 'string_col': ['OLD_FEATURE', 'LATEST_VALUE2', 'LATEST_VALUE3'], 'ts_1': [hour_ago, now, now]}
    dataframe_source = pd.DataFrame(data)
    with prep_file_source(df=dataframe_source, timestamp_field='ts_1') as file_source:
        e = Entity(name='id')
        fv1 = FeatureView(name='feature_view_123', schema=[Field(name='string_col', dtype=String)], entities=[e], source=file_source, ttl=timedelta(minutes=5))
        fs.apply([fv1, e])
        data = {'id': [123], 'string_col': ['hi_123'], 'ts_1': [now]}
        df_data = pd.DataFrame(data)
        fs.write_to_online_store('feature_view_123', df_data)
        df = fs.get_online_features(features=['feature_view_123:string_col'], entity_rows=[{'id': 123}]).to_df()
        assert (df['string_col'].iloc[0] == 'hi_123')
        data = {'id': [123, 567, 890], 'string_col': ['bye_321', 'hello_123', 'greetings_321'], 'ts_1': [hour_ago, hour_ago, hour_ago]}
        df_data = pd.DataFrame(data)
        fs.write_to_online_store('feature_view_123', df_data)
        df = fs.get_online_features(features=['feature_view_123:string_col'], entity_rows=[{'id': 123}, {'id': 567}, {'id': 890}]).to_df()
        assert (df['string_col'].iloc[0] == 'hi_123')
        assert (df['string_col'].iloc[1] == 'hello_123')
        assert (df['string_col'].iloc[2] == 'greetings_321')
        data = {'id': [123], 'string_col': ['LATEST_VALUE'], 'ts_1': [latest]}
        df_data = pd.DataFrame(data)
        fs.write_to_online_store('feature_view_123', df_data)
        df = fs.get_online_features(features=['feature_view_123:string_col'], entity_rows=[{'id': 123}, {'id': 567}, {'id': 890}]).to_df()
        assert (df['string_col'].iloc[0] == 'LATEST_VALUE')
        assert (df['string_col'].iloc[1] == 'hello_123')
        assert (df['string_col'].iloc[2] == 'greetings_321')
        fs.materialize(start_date=(datetime.datetime.now() - timedelta(hours=12)), end_date=datetime.datetime.utcnow())
        df = fs.get_online_features(features=['feature_view_123:string_col'], entity_rows=[{'id': 123}, {'id': 567}, {'id': 890}]).to_df()
        assert (df['string_col'].iloc[0] == 'LATEST_VALUE')
        assert (df['string_col'].iloc[1] == 'LATEST_VALUE2')
        assert (df['string_col'].iloc[2] == 'LATEST_VALUE3')
