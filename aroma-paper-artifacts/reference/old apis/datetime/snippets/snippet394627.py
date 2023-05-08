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
@pytest.mark.parametrize('full_feature_names', [True, False], ids=(lambda v: f'full:{v}'))
def test_historical_features(environment, universal_data_sources, full_feature_names):
    store = environment.feature_store
    (entities, datasets, data_sources) = universal_data_sources
    feature_views = construct_universal_feature_views(data_sources)
    entity_df_with_request_data = datasets.entity_df.copy(deep=True)
    entity_df_with_request_data['val_to_add'] = [i for i in range(len(entity_df_with_request_data))]
    entity_df_with_request_data['driver_age'] = [(i + 100) for i in range(len(entity_df_with_request_data))]
    feature_service = FeatureService(name='convrate_plus100', features=[feature_views.driver[['conv_rate']], feature_views.driver_odfv])
    feature_service_entity_mapping = FeatureService(name='entity_mapping', features=[feature_views.location.with_name('origin').with_join_key_map({'location_id': 'origin_id'}), feature_views.location.with_name('destination').with_join_key_map({'location_id': 'destination_id'})])
    store.apply([driver(), customer(), location(), feature_service, feature_service_entity_mapping, *feature_views.values()])
    event_timestamp = (DEFAULT_ENTITY_DF_EVENT_TIMESTAMP_COL if (DEFAULT_ENTITY_DF_EVENT_TIMESTAMP_COL in datasets.orders_df.columns) else 'e_ts')
    full_expected_df = get_expected_training_df(datasets.customer_df, feature_views.customer, datasets.driver_df, feature_views.driver, datasets.orders_df, feature_views.order, datasets.location_df, feature_views.location, datasets.global_df, feature_views.global_fv, datasets.field_mapping_df, feature_views.field_mapping, entity_df_with_request_data, event_timestamp, full_feature_names)
    expected_df = full_expected_df.drop(columns=['origin__temperature', 'destination__temperature'])
    job_from_df = store.get_historical_features(entity_df=entity_df_with_request_data, features=['driver_stats:conv_rate', 'driver_stats:avg_daily_trips', 'customer_profile:current_balance', 'customer_profile:avg_passenger_count', 'customer_profile:lifetime_trip_count', 'conv_rate_plus_100:conv_rate_plus_100', 'conv_rate_plus_100:conv_rate_plus_100_rounded', 'conv_rate_plus_100:conv_rate_plus_val_to_add', 'order:order_is_success', 'global_stats:num_rides', 'global_stats:avg_ride_length', 'field_mapping:feature_name'], full_feature_names=full_feature_names)
    if job_from_df.supports_remote_storage_export():
        files = job_from_df.to_remote_storage()
        print(files)
        assert (len(files) > 0)
    start_time = datetime.utcnow()
    actual_df_from_df_entities = job_from_df.to_df()
    print(f'actual_df_from_df_entities shape: {actual_df_from_df_entities.shape}')
    end_time = datetime.utcnow()
    print(str(f'''Time to execute job_from_df.to_df() = '{(end_time - start_time)}'
'''))
    assert (sorted(expected_df.columns) == sorted(actual_df_from_df_entities.columns))
    validate_dataframes(expected_df, actual_df_from_df_entities, sort_by=[event_timestamp, 'order_id', 'driver_id', 'customer_id'], event_timestamp_column=event_timestamp, timestamp_precision=timedelta(milliseconds=1))
    assert_feature_service_correctness(store, feature_service, full_feature_names, entity_df_with_request_data, expected_df, event_timestamp)
    assert_feature_service_entity_mapping_correctness(store, feature_service_entity_mapping, full_feature_names, entity_df_with_request_data, full_expected_df, event_timestamp)
    table_from_df_entities: pd.DataFrame = job_from_df.to_arrow().to_pandas()
    validate_dataframes(expected_df, table_from_df_entities, sort_by=[event_timestamp, 'order_id', 'driver_id', 'customer_id'], event_timestamp_column=event_timestamp, timestamp_precision=timedelta(milliseconds=1))
