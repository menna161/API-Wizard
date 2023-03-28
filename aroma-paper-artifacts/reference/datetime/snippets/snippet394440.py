import os
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
from feast import Entity, FeatureView, Field, FileSource
from feast.driver_test_data import create_driver_hourly_stats_df, create_global_daily_stats_df
from feast.feature_store import FeatureStore
from feast.types import Float32, String
from tests.utils.basic_read_write_test import basic_rw_test
from tests.utils.cli_repo_creator import CliRunner, get_example_repo
from tests.utils.feature_records import validate_online_features


def _test_materialize_and_online_retrieval(runner: CliRunner, store: FeatureStore, start_date: datetime, end_date: datetime, driver_df: pd.DataFrame):
    assert (store.repo_path is not None)
    r = runner.run(['materialize', start_date.isoformat(), (end_date - timedelta(days=7)).isoformat()], cwd=Path(store.repo_path))
    assert (r.returncode == 0), f'''stdout: {r.stdout}
 stderr: {r.stderr}'''
    validate_online_features(store, driver_df, (end_date - timedelta(days=7)))
    r = runner.run(['materialize-incremental', end_date.isoformat()], cwd=Path(store.repo_path))
    assert (r.returncode == 0), f'''stdout: {r.stdout}
 stderr: {r.stderr}'''
    validate_online_features(store, driver_df, end_date)
