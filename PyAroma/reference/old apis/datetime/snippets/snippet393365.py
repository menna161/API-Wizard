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


def _check_offline_and_online_features(fs: FeatureStore, fv: FeatureView, driver_id: int, event_timestamp: datetime, expected_value: Optional[float], full_feature_names: bool, check_offline_store: bool=True) -> None:
    response_dict = fs.get_online_features([f'{fv.name}:value'], [{'driver_id': driver_id}], full_feature_names=full_feature_names).to_dict()
    if (not response_dict[f'{fv.name}__value'][0]):
        time.sleep(10)
        response_dict = fs.get_online_features([f'{fv.name}:value'], [{'driver_id': driver_id}], full_feature_names=full_feature_names).to_dict()
    if full_feature_names:
        if expected_value:
            assert response_dict[f'{fv.name}__value'][0], f'Response: {response_dict}'
            assert (abs((response_dict[f'{fv.name}__value'][0] - expected_value)) < 1e-06), f'Response: {response_dict}, Expected: {expected_value}'
        else:
            assert (response_dict[f'{fv.name}__value'][0] is None)
    elif expected_value:
        assert response_dict['value'][0], f'Response: {response_dict}'
        assert (abs((response_dict['value'][0] - expected_value)) < 1e-06), f'Response: {response_dict}, Expected: {expected_value}'
    else:
        assert (response_dict['value'][0] is None)
    if check_offline_store:
        df = fs.get_historical_features(entity_df=pd.DataFrame.from_dict({'driver_id': [driver_id], 'event_timestamp': [event_timestamp]}), features=[f'{fv.name}:value'], full_feature_names=full_feature_names).to_df()
        if full_feature_names:
            if expected_value:
                assert (abs((df.to_dict(orient='list')[f'{fv.name}__value'][0] - expected_value)) < 1e-06)
            else:
                assert ((not df.to_dict(orient='list')[f'{fv.name}__value']) or math.isnan(df.to_dict(orient='list')[f'{fv.name}__value'][0]))
        elif expected_value:
            assert (abs((df.to_dict(orient='list')['value'][0] - expected_value)) < 1e-06)
        else:
            assert ((not df.to_dict(orient='list')['value']) or math.isnan(df.to_dict(orient='list')['value'][0]))
