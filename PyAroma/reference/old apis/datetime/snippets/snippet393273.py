import base64
import json
import logging
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import click
import pkg_resources
import yaml
from colorama import Fore, Style
from dateutil import parser
from pygments import formatters, highlight, lexers
from feast import utils
from feast.constants import DEFAULT_FEATURE_TRANSFORMATION_SERVER_PORT, FEATURE_STORE_YAML_ENV_NAME
from feast.errors import FeastObjectNotFoundException, FeastProviderLoginError
from feast.feature_store import FeatureStore
from feast.feature_view import FeatureView
from feast.on_demand_feature_view import OnDemandFeatureView
from feast.repo_config import load_repo_config
from feast.repo_operations import apply_total, cli_check_repo, generate_project_name, init_repo, plan, registry_dump, teardown
from feast.repo_upgrade import RepoUpgrader
from feast.utils import maybe_local_tz
from tabulate import tabulate
from tabulate import tabulate
from tabulate import tabulate
from tabulate import tabulate
from tabulate import tabulate


@cli.command('materialize-incremental')
@click.argument('end_ts')
@click.option('--views', '-v', help='Feature views to incrementally materialize', multiple=True)
@click.pass_context
def materialize_incremental_command(ctx: click.Context, end_ts: str, views: List[str]):
    "\n    Run an incremental materialization job to ingest new data into the online store. Feast will read\n    all data from the previously ingested point to END_TS from the offline store and write it to the\n    online store. If you don't specify feature view names using --views, all registered Feature\n    Views will be incrementally materialized.\n\n    END_TS should be in ISO 8601 format, e.g. '2021-07-16T19:20:01'\n    "
    repo = ctx.obj['CHDIR']
    fs_yaml_file = ctx.obj['FS_YAML_FILE']
    cli_check_repo(repo, fs_yaml_file)
    store = FeatureStore(repo_path=str(repo), fs_yaml_file=fs_yaml_file)
    store.materialize_incremental(feature_views=(None if (not views) else views), end_date=utils.make_tzaware(datetime.fromisoformat(end_ts)))
