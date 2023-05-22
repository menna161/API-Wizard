import dataclasses
import importlib
import json
import os
import tempfile
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Type, Union
import pandas as pd
import pytest
import yaml
from feast import FeatureStore, FeatureView, OnDemandFeatureView, driver_test_data
from feast.constants import FULL_REPO_CONFIGS_MODULE_ENV_NAME
from feast.data_source import DataSource
from feast.errors import FeastModuleImportError
from feast.infra.feature_servers.base_config import FeatureLoggingConfig
from feast.infra.feature_servers.local_process.config import LocalFeatureServerConfig
from feast.repo_config import RegistryConfig, RepoConfig
from tests.integration.feature_repos.integration_test_repo_config import IntegrationTestRepoConfig, RegistryLocation
from tests.integration.feature_repos.universal.data_source_creator import DataSourceCreator
from tests.integration.feature_repos.universal.data_sources.bigquery import BigQueryDataSourceCreator
from tests.integration.feature_repos.universal.data_sources.file import FileDataSourceCreator
from tests.integration.feature_repos.universal.data_sources.redshift import RedshiftDataSourceCreator
from tests.integration.feature_repos.universal.data_sources.snowflake import SnowflakeDataSourceCreator
from tests.integration.feature_repos.universal.feature_views import conv_rate_plus_100_feature_view, create_conv_rate_request_source, create_customer_daily_profile_feature_view, create_driver_hourly_stats_batch_feature_view, create_driver_hourly_stats_feature_view, create_field_mapping_feature_view, create_global_stats_feature_view, create_location_stats_feature_view, create_order_feature_view, create_pushable_feature_view
from tests.integration.feature_repos.universal.online_store.bigtable import BigtableOnlineStoreCreator
from tests.integration.feature_repos.universal.online_store.datastore import DatastoreOnlineStoreCreator
from tests.integration.feature_repos.universal.online_store.dynamodb import DynamoDBOnlineStoreCreator
from tests.integration.feature_repos.universal.online_store.redis import RedisOnlineStoreCreator
from tests.integration.feature_repos.universal.online_store_creator import OnlineStoreCreator
from feast.infra.feature_servers.aws_lambda.config import AwsLambdaFeatureServerConfig


def construct_universal_datasets(entities: UniversalEntities, start_time: datetime, end_time: datetime) -> UniversalDatasets:
    customer_df = driver_test_data.create_customer_daily_profile_df(entities.customer_vals, start_time, end_time)
    driver_df = driver_test_data.create_driver_hourly_stats_df(entities.driver_vals, start_time, end_time)
    location_df = driver_test_data.create_location_stats_df(entities.location_vals, start_time, end_time)
    orders_df = driver_test_data.create_orders_df(customers=entities.customer_vals, drivers=entities.driver_vals, locations=entities.location_vals, start_date=start_time, end_date=end_time, order_count=20)
    global_df = driver_test_data.create_global_daily_stats_df(start_time, end_time)
    field_mapping_df = driver_test_data.create_field_mapping_df(start_time, end_time)
    entity_df = orders_df[['customer_id', 'driver_id', 'order_id', 'origin_id', 'destination_id', 'event_timestamp']]
    return UniversalDatasets(customer_df=customer_df, driver_df=driver_df, location_df=location_df, orders_df=orders_df, global_df=global_df, field_mapping_df=field_mapping_df, entity_df=entity_df)
