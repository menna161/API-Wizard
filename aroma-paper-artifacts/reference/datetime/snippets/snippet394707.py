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
def test_e2e_validation_via_cli(environment, universal_data_sources):
    runner = CliRunner()
    store = environment.feature_store
    (_, datasets, data_sources) = universal_data_sources
    feature_views = construct_universal_feature_views(data_sources)
    feature_service = FeatureService(name='test_service', features=[feature_views.customer[['current_balance', 'avg_passenger_count', 'lifetime_trip_count']]], logging_config=LoggingConfig(destination=environment.data_source_creator.create_logged_features_destination()))
    store.apply([customer(), feature_service, feature_views.customer])
    entity_df = datasets.entity_df.drop(columns=['order_id', 'origin_id', 'destination_id', 'driver_id'])
    retrieval_job = store.get_historical_features(entity_df=entity_df, features=store.get_feature_service(feature_service.name), full_feature_names=True)
    logs_df = prepare_logs(retrieval_job.to_df(), feature_service, store)
    saved_dataset = store.create_saved_dataset(from_=retrieval_job, name='reference_for_validating_logged_features', storage=environment.data_source_creator.create_saved_dataset_destination(), allow_overwrite=True)
    reference = saved_dataset.as_reference(name='test_reference', profiler=configurable_profiler)
    schema = FeatureServiceLoggingSource(feature_service=feature_service, project=store.project).get_schema(store._registry)
    store.write_logged_features(pa.Table.from_pandas(logs_df, schema=schema), source=feature_service)
    with runner.local_repo(example_repo_py='', offline_store='file') as local_repo:
        local_repo.apply([customer(), feature_views.customer, feature_service, reference])
        local_repo._registry.apply_saved_dataset(saved_dataset, local_repo.project)
        validate_args = ['validate', '--feature-service', feature_service.name, '--reference', reference.name, (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat(), datetime.datetime.now().isoformat()]
        p = runner.run(validate_args, cwd=local_repo.repo_path)
        assert (p.returncode == 0), p.stderr.decode()
        assert ('Validation successful' in p.stdout.decode()), p.stderr.decode()
        shutil.rmtree(saved_dataset.storage.file_options.uri)
        invalid_data = pd.DataFrame(data={'customer_id': [0], 'current_balance': [0], 'avg_passenger_count': [0], 'lifetime_trip_count': [0], 'event_timestamp': [(make_tzaware(datetime.datetime.utcnow()) - datetime.timedelta(hours=1))]})
        invalid_logs = prepare_logs(invalid_data, feature_service, store)
        store.write_logged_features(pa.Table.from_pandas(invalid_logs, schema=schema), source=feature_service)
        p = runner.run(validate_args, cwd=local_repo.repo_path)
        assert (p.returncode == 1), p.stdout.decode()
        assert ('Validation failed' in p.stdout.decode()), p.stderr.decode()
