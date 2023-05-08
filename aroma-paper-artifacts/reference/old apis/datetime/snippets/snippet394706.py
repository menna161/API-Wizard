import datetime
import shutil
import pandas as pd
import pyarrow as pa
import pytest
from great_expectations.core import ExpectationSuite
from great_expectations.dataset import PandasDataset
from feast import FeatureService
from feast.dqm.errors import ValidationFailed
from feast.dqm.profilers.ge_profiler import ge_profiler
from feast.feature_logging import LOG_TIMESTAMP_FIELD, FeatureServiceLoggingSource, LoggingConfig
from feast.protos.feast.serving.ServingService_pb2 import FieldStatus
from feast.utils import make_tzaware
from feast.wait import wait_retry_backoff
from tests.integration.feature_repos.repo_configuration import construct_universal_feature_views
from tests.integration.feature_repos.universal.entities import customer, driver, location
from tests.utils.cli_repo_creator import CliRunner
from tests.utils.test_log_creator import prepare_logs
from great_expectations.profile.user_configurable_profiler import UserConfigurableProfiler
from great_expectations.profile.user_configurable_profiler import UserConfigurableProfiler


@pytest.mark.integration
@pytest.mark.universal_offline_stores
def test_logged_features_validation(environment, universal_data_sources):
    store = environment.feature_store
    (_, datasets, data_sources) = universal_data_sources
    feature_views = construct_universal_feature_views(data_sources)
    feature_service = FeatureService(name='test_service', features=[feature_views.customer[['current_balance', 'avg_passenger_count', 'lifetime_trip_count']], feature_views.order[['order_is_success']], feature_views.global_fv[['num_rides', 'avg_ride_length']]], logging_config=LoggingConfig(destination=environment.data_source_creator.create_logged_features_destination()))
    store.apply([driver(), customer(), location(), feature_service, *feature_views.values()])
    entity_df = datasets.entity_df.drop(columns=['order_id', 'origin_id', 'destination_id'])
    for i in range(5):
        entity_df = pd.concat([entity_df, pd.DataFrame.from_records([{'customer_id': (2000 + i), 'driver_id': (6000 + i), 'event_timestamp': datetime.datetime.now()}])])
    store_fs = store.get_feature_service(feature_service.name)
    reference_dataset = store.create_saved_dataset(from_=store.get_historical_features(entity_df=entity_df, features=store_fs, full_feature_names=True), name='reference_for_validating_logged_features', storage=environment.data_source_creator.create_saved_dataset_destination(), allow_overwrite=True)
    log_source_df = store.get_historical_features(entity_df=entity_df, features=store_fs, full_feature_names=False).to_df()
    logs_df = prepare_logs(log_source_df, feature_service, store)
    schema = FeatureServiceLoggingSource(feature_service=feature_service, project=store.project).get_schema(store._registry)
    store.write_logged_features(pa.Table.from_pandas(logs_df, schema=schema), source=feature_service)

    def validate():
        '\n        Return Tuple[succeed, completed]\n        Succeed will be True if no ValidateFailed exception was raised\n        '
        try:
            store.validate_logged_features(feature_service, start=logs_df[LOG_TIMESTAMP_FIELD].min(), end=(logs_df[LOG_TIMESTAMP_FIELD].max() + datetime.timedelta(seconds=1)), reference=reference_dataset.as_reference(name='ref', profiler=profiler_with_feature_metadata))
        except ValidationFailed:
            return (False, True)
        except Exception:
            return (False, False)
        return (True, True)
    success = wait_retry_backoff(validate, timeout_secs=30)
    assert success, 'Validation failed (unexpectedly)'
