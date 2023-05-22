import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from textwrap import dedent
from tests.utils.cli_repo_creator import CliRunner


def test_repo_init() -> None:
    '\n    This test simply makes sure that you can run `feast apply && feast materialize` on\n    the repo created by "feast init" without errors.\n    '
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        result = runner.run(['init', 'my_project'], cwd=temp_path)
        repo_path = ((temp_path / 'my_project') / 'feature_repo')
        assert (result.returncode == 0)
        result = runner.run(['apply'], cwd=repo_path)
        assert (result.returncode == 0)
        end_date = datetime.utcnow()
        start_date = (end_date - timedelta(days=100))
        result = runner.run(['materialize', start_date.isoformat(), end_date.isoformat()], cwd=repo_path)
        assert (result.returncode == 0)
