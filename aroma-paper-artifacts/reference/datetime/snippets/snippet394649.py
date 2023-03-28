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


def get_latest_feature_values_from_dataframes(driver_df, customer_df, orders_df, entity_row, global_df=None, location_df=None, origin_df=None, destination_df=None):
    latest_driver_row = get_latest_row(entity_row, driver_df, 'driver_id', 'driver_id')
    latest_customer_row = get_latest_row(entity_row, customer_df, 'customer_id', 'customer_id')
    latest_location_row = get_latest_row(entity_row, location_df, 'location_id', 'location_id')
    order_rows = orders_df[((orders_df['driver_id'] == entity_row['driver_id']) & (orders_df['customer_id'] == entity_row['customer_id']))]
    timestamps = order_rows[['event_timestamp']]
    timestamps['event_timestamp'] = pd.to_datetime(timestamps['event_timestamp'], utc=True)
    max_index = timestamps['event_timestamp'].idxmax()
    latest_orders_row = order_rows.loc[max_index]
    if (global_df is not None):
        latest_global_row = global_df.loc[global_df['event_timestamp'].idxmax()].to_dict()
    if (origin_df is not None):
        latest_location_aliased_row = get_latest_feature_values_for_location_df(entity_row, origin_df, destination_df)
    request_data_features = entity_row.copy()
    request_data_features.pop('driver_id')
    request_data_features.pop('customer_id')
    if (global_df is not None):
        return {**latest_customer_row, **latest_driver_row, **latest_orders_row, **latest_global_row, **latest_location_row, **request_data_features}
    if (origin_df is not None):
        request_data_features.pop('origin_id')
        request_data_features.pop('destination_id')
        return {**latest_customer_row, **latest_driver_row, **latest_orders_row, **latest_location_row, **latest_location_aliased_row, **request_data_features}
    return {**latest_customer_row, **latest_driver_row, **latest_orders_row, **latest_location_row, **request_data_features}
