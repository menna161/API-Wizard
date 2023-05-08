import math
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional
import pandas as pd
import pytest
import yaml
from pytz import utc
from feast import FeatureStore, FeatureView, FileSource, RepoConfig
from feast.data_format import ParquetFormat
from feast.entity import Entity
from feast.field import Field
from feast.infra.registry.registry import Registry
from feast.types import Array, Bytes, Int64, String
from tests.integration.feature_repos.integration_test_repo_config import IntegrationTestRepoConfig
from tests.integration.feature_repos.universal.data_source_creator import DataSourceCreator
from tests.integration.feature_repos.universal.data_sources.bigquery import BigQueryDataSourceCreator
from tests.integration.feature_repos.universal.data_sources.file import FileDataSourceCreator, FileParquetDatasetSourceCreator
from tests.integration.feature_repos.universal.data_sources.redshift import RedshiftDataSourceCreator


def validate_offline_online_store_consistency(fs: FeatureStore, fv: FeatureView, split_dt: datetime) -> None:
    now = datetime.utcnow()
    full_feature_names = True
    check_offline_store: bool = True
    start_date = (now - timedelta(hours=5)).replace(tzinfo=utc)
    end_date = split_dt
    fs.materialize(feature_views=[fv.name], start_date=start_date, end_date=end_date)
    time.sleep(10)
    _check_offline_and_online_features(fs=fs, fv=fv, driver_id=1, event_timestamp=end_date, expected_value=0.3, full_feature_names=full_feature_names, check_offline_store=check_offline_store)
    _check_offline_and_online_features(fs=fs, fv=fv, driver_id=2, event_timestamp=end_date, expected_value=None, full_feature_names=full_feature_names, check_offline_store=check_offline_store)
    _check_offline_and_online_features(fs=fs, fv=fv, driver_id=3, event_timestamp=end_date, expected_value=4, full_feature_names=full_feature_names, check_offline_store=check_offline_store)
    fs.materialize_incremental(feature_views=[fv.name], end_date=now)
    _check_offline_and_online_features(fs=fs, fv=fv, driver_id=3, event_timestamp=now, expected_value=5, full_feature_names=full_feature_names, check_offline_store=check_offline_store)
