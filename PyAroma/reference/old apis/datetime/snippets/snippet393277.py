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


@cli.command('validate')
@click.option('--feature-service', '-f', help='Specify a feature service name')
@click.option('--reference', '-r', help='Specify a validation reference name')
@click.option('--no-profile-cache', is_flag=True, help='Do not store cached profile in registry')
@click.argument('start_ts')
@click.argument('end_ts')
@click.pass_context
def validate(ctx: click.Context, feature_service: str, reference: str, start_ts: str, end_ts: str, no_profile_cache):
    "\n    Perform validation of logged features (produced by a given feature service) against provided reference.\n\n    START_TS and END_TS should be in ISO 8601 format, e.g. '2021-07-16T19:20:01'\n    "
    repo = ctx.obj['CHDIR']
    fs_yaml_file = ctx.obj['FS_YAML_FILE']
    cli_check_repo(repo, fs_yaml_file)
    store = FeatureStore(repo_path=str(repo), fs_yaml_file=fs_yaml_file)
    feature_service = store.get_feature_service(name=feature_service)
    reference = store.get_validation_reference(reference)
    result = store.validate_logged_features(source=feature_service, reference=reference, start=maybe_local_tz(datetime.fromisoformat(start_ts)), end=maybe_local_tz(datetime.fromisoformat(end_ts)), throw_exception=False, cache_profile=(not no_profile_cache))
    if (not result):
        print(f'{(Style.BRIGHT + Fore.GREEN)}Validation successful!{Style.RESET_ALL}')
        return
    errors = [e.to_dict() for e in result.report.errors]
    formatted_json = json.dumps(errors, indent=4)
    colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
    print(f'{(Style.BRIGHT + Fore.RED)}Validation failed!{Style.RESET_ALL}')
    print(colorful_json)
    exit(1)
