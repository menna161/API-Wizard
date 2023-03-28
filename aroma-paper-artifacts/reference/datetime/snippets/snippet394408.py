import tempfile
from pathlib import Path
from textwrap import dedent
from tests.utils.cli_repo_creator import CliRunner, get_example_repo


def test_cli_apply_imported_featureview_with_duplication() -> None:
    '\n    Tests that applying feature views with duplicated names is not possible, even if one of the\n    duplicated feature views is imported from another file.\n    '
    with tempfile.TemporaryDirectory() as repo_dir_name, tempfile.TemporaryDirectory() as data_dir_name:
        runner = CliRunner()
        repo_path = Path(repo_dir_name)
        data_path = Path(data_dir_name)
        repo_config = (repo_path / 'feature_store.yaml')
        repo_config.write_text(dedent(f'''
        project: foo
        registry: {(data_path / 'registry.db')}
        provider: local
        online_store:
            path: {(data_path / 'online_store.db')}
        '''))
        repo_example = (repo_path / 'example.py')
        repo_example.write_text(get_example_repo('example_feature_repo_with_driver_stats_feature_view.py'))
        repo_example_2 = (repo_path / 'example_2.py')
        repo_example_2.write_text("from datetime import timedelta\nfrom example import driver, driver_hourly_stats, driver_hourly_stats_view\nfrom feast import FeatureService, FeatureView\na_feature_service = FeatureService(\n   name='driver_locations_service',\n   features=[driver_hourly_stats_view],\n)\ndriver_hourly_stats_view_2 = FeatureView(\n   name='driver_hourly_stats',\n   entities=[driver],\n   ttl=timedelta(days=1),\n   online=True,\n   source=driver_hourly_stats,\n   tags={'dummy': 'true'})\n")
        (rc, output) = runner.run_with_output(['apply'], cwd=repo_path)
        assert (rc != 0)
        assert (b'More than one feature view with name driver_hourly_stats found.' in output)
