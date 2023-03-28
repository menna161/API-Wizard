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


def __post_init__(self):
    self.end_date = datetime.utcnow().replace(microsecond=0, second=0, minute=0)
    self.start_date: datetime = (self.end_date - timedelta(days=3))
