import threading
import time
from datetime import datetime
from typing import List
import grpc
import pandas as pd
import pytest
import pytz
import requests
from feast.embedded_go.online_features_service import EmbeddedOnlineFeatureServer
from feast.feast_object import FeastObject
from feast.feature_logging import LoggingConfig
from feast.feature_service import FeatureService
from feast.infra.feature_servers.base_config import FeatureLoggingConfig
from feast.protos.feast.serving.ServingService_pb2 import FieldStatus, GetOnlineFeaturesRequest, GetOnlineFeaturesResponse
from feast.protos.feast.serving.ServingService_pb2_grpc import ServingServiceStub
from feast.protos.feast.types.Value_pb2 import RepeatedValue
from feast.type_map import python_values_to_proto_values
from feast.value_type import ValueType
from feast.wait import wait_retry_backoff
from tests.integration.feature_repos.repo_configuration import construct_universal_feature_views
from tests.integration.feature_repos.universal.entities import customer, driver, location
from tests.utils.http_server import check_port_open, free_port
from tests.utils.test_log_creator import generate_expected_logs, get_latest_rows


@pytest.mark.integration
@pytest.mark.goserver
@pytest.mark.universal_offline_stores
@pytest.mark.parametrize('full_feature_names', [True, False], ids=(lambda v: str(v)))
def test_feature_logging(grpc_client, environment, universal_data_sources, full_feature_names):
    fs = environment.feature_store
    feature_service = fs.get_feature_service('driver_features')
    log_start_date = datetime.now().astimezone(pytz.UTC)
    driver_ids = list(range(5001, 5011))
    for driver_id in driver_ids:
        grpc_client.GetOnlineFeatures(GetOnlineFeaturesRequest(feature_service='driver_features', entities={'driver_id': RepeatedValue(val=python_values_to_proto_values([driver_id], feature_type=ValueType.INT64))}, full_feature_names=full_feature_names))
        time.sleep(0.1)
    (_, datasets, _) = universal_data_sources
    latest_rows = get_latest_rows(datasets.driver_df, 'driver_id', driver_ids)
    feature_view = fs.get_feature_view('driver_stats')
    features = [feature.name for proj in feature_service.feature_view_projections for feature in proj.features]
    expected_logs = generate_expected_logs(latest_rows, feature_view, features, ['driver_id'], 'event_timestamp')

    def retrieve():
        retrieval_job = fs._get_provider().retrieve_feature_service_logs(feature_service=feature_service, start_date=log_start_date, end_date=datetime.now().astimezone(pytz.UTC), config=fs.config, registry=fs._registry)
        try:
            df = retrieval_job.to_df()
        except Exception:
            return (None, False)
        return (df, (df.shape[0] == len(driver_ids)))
    persisted_logs = wait_retry_backoff(retrieve, timeout_secs=60, timeout_msg='Logs retrieval failed')
    persisted_logs = persisted_logs.sort_values(by='driver_id').reset_index(drop=True)
    persisted_logs = persisted_logs[expected_logs.columns]
    pd.testing.assert_frame_equal(expected_logs, persisted_logs, check_dtype=False)
