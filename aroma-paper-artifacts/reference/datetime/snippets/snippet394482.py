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


def retrieve():
    retrieval_job = fs._get_provider().retrieve_feature_service_logs(feature_service=feature_service, start_date=log_start_date, end_date=datetime.now().astimezone(pytz.UTC), config=fs.config, registry=fs._registry)
    try:
        df = retrieval_job.to_df()
    except Exception:
        return (None, False)
    return (df, (df.shape[0] == len(driver_ids)))
