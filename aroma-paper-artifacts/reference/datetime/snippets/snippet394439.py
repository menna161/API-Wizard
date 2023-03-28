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


def test_e2e_local() -> None:
    '\n    Tests the end-to-end workflow of apply, materialize, and online retrieval.\n\n    This test runs against several types of repos:\n    1. A repo with a normal FV and an entity-less FV.\n    2. A repo using the SDK from version 0.19.0.\n    3. A repo with a FV with a ttl of 0.\n    '
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as data_dir:
        end_date = datetime.now().replace(microsecond=0, second=0, minute=0)
        start_date = (end_date - timedelta(days=15))
        driver_entities = [1001, 1002, 1003, 1004, 1005]
        driver_df = create_driver_hourly_stats_df(driver_entities, start_date, end_date)
        driver_stats_path = os.path.join(data_dir, 'driver_stats.parquet')
        driver_df.to_parquet(path=driver_stats_path, allow_truncated_timestamps=True)
        global_df = create_global_daily_stats_df(start_date, end_date)
        global_stats_path = os.path.join(data_dir, 'global_stats.parquet')
        global_df.to_parquet(path=global_stats_path, allow_truncated_timestamps=True)
        with runner.local_repo(get_example_repo('example_feature_repo_2.py').replace('%PARQUET_PATH%', driver_stats_path).replace('%PARQUET_PATH_GLOBAL%', global_stats_path), 'file') as store:
            _test_materialize_and_online_retrieval(runner, store, start_date, end_date, driver_df)
        with runner.local_repo(get_example_repo('example_feature_repo_with_bfvs.py').replace('%PARQUET_PATH%', driver_stats_path).replace('%PARQUET_PATH_GLOBAL%', global_stats_path), 'file') as store:
            _test_materialize_and_online_retrieval(runner, store, start_date, end_date, driver_df)
        with runner.local_repo(get_example_repo('example_feature_repo_with_ttl_0.py').replace('%PARQUET_PATH%', driver_stats_path).replace('%PARQUET_PATH_GLOBAL%', global_stats_path), 'file') as store:
            _test_materialize_and_online_retrieval(runner, store, start_date, end_date, driver_df)
        with runner.local_repo(get_example_repo('example_feature_repo_with_entity_join_key.py').replace('%PARQUET_PATH%', driver_stats_path), 'file') as store:
            assert (store.repo_path is not None)
            (returncode, output) = runner.run_with_output(['materialize', start_date.isoformat(), (end_date - timedelta(days=7)).isoformat()], cwd=Path(store.repo_path))
            assert (returncode != 0)
            assert ('feast.errors.FeastJoinKeysDuringMaterialization' in str(output))
