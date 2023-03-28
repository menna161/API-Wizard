import random
import time
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import pytest
from feast.entity import Entity
from feast.errors import RequestDataNotFoundInEntityDfException
from feast.feature_service import FeatureService
from feast.feature_view import FeatureView
from feast.field import Field
from feast.infra.offline_stores.offline_utils import DEFAULT_ENTITY_DF_EVENT_TIMESTAMP_COL
from feast.types import Float32, Int32
from tests.integration.feature_repos.repo_configuration import construct_universal_feature_views, table_name_from_data_source
from tests.integration.feature_repos.universal.data_sources.snowflake import SnowflakeDataSourceCreator
from tests.integration.feature_repos.universal.entities import customer, driver, location
from tests.utils.feature_records import assert_feature_service_correctness, assert_feature_service_entity_mapping_correctness, get_expected_training_df, get_response_feature_name, validate_dataframes


@pytest.mark.integration
@pytest.mark.universal_offline_stores
def test_historical_features_from_bigquery_sources_containing_backfills(environment):
    store = environment.feature_store
    now = datetime.now().replace(microsecond=0, second=0, minute=0)
    tomorrow = (now + timedelta(days=1))
    day_after_tomorrow = (now + timedelta(days=2))
    entity_df = pd.DataFrame(data=[{'driver_id': 1001, 'event_timestamp': day_after_tomorrow}, {'driver_id': 1002, 'event_timestamp': day_after_tomorrow}])
    driver_stats_df = pd.DataFrame(data=[{'driver_id': 1001, 'avg_daily_trips': 10, 'event_timestamp': now, 'created': now}, {'driver_id': 1001, 'avg_daily_trips': 20, 'event_timestamp': now, 'created': tomorrow}, {'driver_id': 1002, 'avg_daily_trips': 30, 'event_timestamp': now, 'created': tomorrow}, {'driver_id': 1002, 'avg_daily_trips': 40, 'event_timestamp': tomorrow, 'created': now}])
    expected_df = pd.DataFrame(data=[{'driver_id': 1001, 'event_timestamp': day_after_tomorrow, 'avg_daily_trips': 20}, {'driver_id': 1002, 'event_timestamp': day_after_tomorrow, 'avg_daily_trips': 40}])
    driver_stats_data_source = environment.data_source_creator.create_data_source(df=driver_stats_df, destination_name=f'test_driver_stats_{int(time.time_ns())}_{random.randint(1000, 9999)}', timestamp_field='event_timestamp', created_timestamp_column='created')
    driver = Entity(name='driver', join_keys=['driver_id'])
    driver_fv = FeatureView(name='driver_stats', entities=[driver], schema=[Field(name='avg_daily_trips', dtype=Int32)], source=driver_stats_data_source)
    store.apply([driver, driver_fv])
    offline_job = store.get_historical_features(entity_df=entity_df, features=['driver_stats:avg_daily_trips'], full_feature_names=False)
    start_time = datetime.utcnow()
    actual_df = offline_job.to_df()
    print(f'actual_df shape: {actual_df.shape}')
    end_time = datetime.utcnow()
    print(str(f'''Time to execute job_from_df.to_df() = '{(end_time - start_time)}'
'''))
    assert (sorted(expected_df.columns) == sorted(actual_df.columns))
    validate_dataframes(expected_df, actual_df, sort_by=['driver_id'])
