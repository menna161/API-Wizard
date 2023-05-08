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


def validate():
    '\n        Return Tuple[succeed, completed]\n        Succeed will be True if no ValidateFailed exception was raised\n        '
    try:
        store.validate_logged_features(feature_service, start=logs_df[LOG_TIMESTAMP_FIELD].min(), end=(logs_df[LOG_TIMESTAMP_FIELD].max() + datetime.timedelta(seconds=1)), reference=reference_dataset.as_reference(name='ref', profiler=profiler_with_feature_metadata))
    except ValidationFailed:
        return (False, True)
    except Exception:
        return (False, False)
    return (True, True)
