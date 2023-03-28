import datetime
import pandas as pd
import pyarrow as pa
import pytest
from feast.feature_logging import LOG_DATE_FIELD, LOG_TIMESTAMP_FIELD, REQUEST_ID_FIELD, FeatureServiceLoggingSource, LoggingConfig
from feast.feature_service import FeatureService
from feast.wait import wait_retry_backoff
from tests.integration.feature_repos.repo_configuration import construct_universal_feature_views
from tests.integration.feature_repos.universal.entities import customer, driver, location
from tests.integration.feature_repos.universal.feature_views import conv_rate_plus_100
from tests.utils.test_log_creator import prepare_logs, to_logs_dataset


def retrieve():
    retrieval_job = store._get_provider().retrieve_feature_service_logs(feature_service=feature_service, start_date=logs_df[LOG_TIMESTAMP_FIELD].min(), end_date=(logs_df[LOG_TIMESTAMP_FIELD].max() + datetime.timedelta(seconds=1)), config=store.config, registry=store._registry)
    try:
        df = retrieval_job.to_df()
    except Exception:
        return (None, False)
    return (df, (df.shape[0] == logs_df.shape[0]))
